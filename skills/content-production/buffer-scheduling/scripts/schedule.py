#!/usr/bin/env python3
"""Validate or schedule a JSON post plan with a durable attempt ledger."""
import argparse
import json
import subprocess
from datetime import datetime
from pathlib import Path


def cli(args, payload=None):
    result = subprocess.run(['buffer', *args, '--output', 'json', '--quiet'], input=json.dumps(payload) if payload is not None else None, text=True, capture_output=True)
    try:
        data = json.loads(result.stdout)
    except ValueError:
        raise RuntimeError('Buffer returned no JSON. Inspect the attempt before retrying. CLI stderr: ' + result.stderr[:2000])
    if result.returncode or isinstance(data, dict) and 'error' in data:
        raise RuntimeError(json.dumps(data))
    return data


def existing_posts(org, channel_ids=None):
    posts, cursor = [], None
    query = {'organizationId': org}
    if channel_ids:
        query['filter'] = {'channelIds': sorted(set(channel_ids))}
    while True:
        args = ['posts', 'list', '--input', '-', '--limit', '100', '--fields', 'items.{id,text,status,dueAt,channelId,assets.source},pageInfo']
        if cursor:
            args += ['--after', cursor]
        page = cli(args, query)
        posts.extend(page['items'])
        if not page['pageInfo']['hasNextPage']:
            return posts
        cursor = page['pageInfo']['endCursor']


def matching(post, payload):
    return post['channelId'] == payload['channelId'] and post['text'] == payload['text'] and post.get('dueAt') and (payload['mode'] == 'addToQueue' or datetime.fromisoformat(post['dueAt'].replace('Z', '+00:00')) == datetime.fromisoformat(payload['dueAt'])) and any(a.get('source') == payload['assets'][0]['video']['url'] for a in post.get('assets', []))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan', type=Path, required=True)
    parser.add_argument('--media', type=Path, help='JSON mapping local absolute paths to stable public video URLs')
    parser.add_argument('--ledger', type=Path, required=True)
    parser.add_argument('--execute', action='store_true', help='Create scheduled posts. Omit to validate locally.')
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text())
    media = json.loads(args.media.read_text()) if args.media else {}
    records = [json.loads(line) for line in args.ledger.read_text().splitlines()] if args.ledger.exists() else []
    last = {r['key']: r for r in records}
    keys = [p['key'] for p in plan['posts']]
    assert len(keys) == len(set(keys)), 'Duplicate plan keys'
    payloads = []
    for post in plan['posts']:
        mode = post.get('mode', 'customScheduled')
        if mode == 'customScheduled':
            due = datetime.fromisoformat(post['dueAt'])
            assert due.tzinfo, 'dueAt must have a timezone'
        assert Path(post['clip']['path']).is_file(), 'Missing master'
        url = media.get(post['clip']['path'])
        if args.execute and not url:
            raise RuntimeError('Missing public video URL for ' + post['clip']['path'])
        assert not url or url.startswith('https://'), 'Media must use HTTPS'
        payload = {'channelId': post['channelId'], 'text': post['text'], 'schedulingType': post.get('schedulingType', 'automatic'), 'mode': mode, 'assets': [{'video': {'url': url or 'https://example.invalid/validation-only.mp4'}}]}
        if mode == 'customScheduled':
            payload['dueAt'] = post['dueAt']
        if post.get('metadata'):
            payload['metadata'] = post['metadata']
        if post.get('videoMetadata'):
            payload['assets'][0]['video']['metadata'] = post['videoMetadata']
        if post['service'] == 'instagram':
            payload.setdefault('metadata', {}).setdefault('instagram', {})
            payload['metadata']['instagram'].setdefault('type', 'reel')
            payload['metadata']['instagram'].setdefault('shouldShareToFeed', True)
            payload['assets'][0]['video'].setdefault('metadata', {}).setdefault('thumbnailOffset', 0)
        if post['service'] == 'youtube':
            youtube = payload.get('metadata', {}).get('youtube', {})
            if not all(youtube.get(field) for field in ('title', 'categoryId', 'privacy')):
                raise RuntimeError('YouTube requires title, categoryId and explicit privacy: ' + post['key'])
        cli(['posts', 'create', '--input', '-', '--dry-run'], payload)
        payloads.append((post, payload))
    if not args.execute:
        print(json.dumps({'validated': len(payloads), 'mediaResolved': sum(p['clip']['path'] in media for p in plan['posts']), 'created': 0}))
        return
    # Complete validation before the first external mutation.
    for url in set(media[p['clip']['path']] for p in plan['posts']):
        result = subprocess.run(['curl', '-fsSI', '--max-time', '30', url], capture_output=True, text=True)
        headers = result.stdout.lower()
        if result.returncode or 'content-type: video/' not in headers:
            raise RuntimeError('URL does not serve public video: ' + url)
    remote = existing_posts(plan['organizationId'], [post['channelId'] for post in plan['posts']])
    args.ledger.parent.mkdir(parents=True, exist_ok=True)
    def record(entry):
        with args.ledger.open('a') as f:
            f.write(json.dumps(entry) + '\n')
            f.flush()
            import os
            os.fsync(f.fileno())
        last[entry['key']] = entry
    for post, payload in payloads:
        prior = last.get(post['key'])
        if prior and prior['state'] == 'confirmed':
            if prior['payload'] != payload:
                raise RuntimeError('Confirmed post payload changed: ' + post['key'])
            continue
        matches = [p for p in remote if matching(p, payload)]
        if len(matches) > 1:
            raise RuntimeError('Multiple matching posts. Inspect ' + post['key'])
        if matches:
            if matches[0]['status'] not in ['scheduled', 'sending', 'sent']:
                raise RuntimeError('Matching post is not scheduled: ' + json.dumps(matches[0]))
            record({'key': post['key'], 'state': 'confirmed', 'postId': matches[0]['id'], 'payload': payload, 'reconciled': True})
            continue
        if prior and prior['state'] not in ['confirmed', 'not_created']:
            raise RuntimeError('Previous attempt is unresolved. Inspect full history before retrying ' + post['key'])
        if payload['mode'] == 'customScheduled' and datetime.fromisoformat(payload['dueAt']) <= datetime.now().astimezone():
            raise RuntimeError('Publication time is in the past: ' + post['key'])
        record({'key': post['key'], 'state': 'attempting', 'payload': payload, 'attemptedAt': datetime.now().astimezone().isoformat()})
        result = cli(['posts', 'create', '--input', '-', '--fields', 'post.id,post.text,post.status,post.dueAt,post.channelId,post.assets.source'], payload)
        result_post = result.get('post', {})
        if not result_post.get('id'):
            raise RuntimeError('Uncertain create result. Inspect before retrying: ' + json.dumps(result))
        verified = result_post
        if verified.get('status') != 'scheduled' or not matching(verified, payload):
            raise RuntimeError('Created post differs from plan: ' + json.dumps(verified))
        record({'key': post['key'], 'state': 'confirmed', 'postId': verified['id'], 'dueAt': verified['dueAt'], 'payload': payload})
        print(json.dumps({'key': post['key'], 'postId': verified['id'], 'status': verified['status'], 'dueAt': verified['dueAt']}), flush=True)
    print(json.dumps({'confirmed': sum(r['state'] == 'confirmed' for r in last.values())}))

if __name__ == '__main__':
    main()
