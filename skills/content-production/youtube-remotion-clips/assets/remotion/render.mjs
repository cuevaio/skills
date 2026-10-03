import path from 'node:path';
import fs from 'node:fs';
import {bundle} from '@remotion/bundler';
import {getCompositions, renderMedia, renderStill} from '@remotion/renderer';
import clips from './clips.json' with {type:'json'};

const serveUrl = await bundle({entryPoint:path.resolve('src/index.jsx')});
const compositions = await getCompositions(serveUrl);
const only = process.argv.find(a=>a.startsWith('--only='))?.slice(7);
for (const composition of compositions.filter(c=>!only||c.id===only)) {
  fs.mkdirSync('../review',{recursive:true});
  const common = {serveUrl,composition,chromiumOptions:{disableWebSecurity:false},logLevel:'warn'};
  fs.mkdirSync('../covers',{recursive:true});
  fs.mkdirSync('../clips',{recursive:true});
  await renderStill({...common,frame:0,output:`../covers/${composition.id}.png`});
  for (const seconds of [1,8,Math.max(0,Math.floor(composition.durationInFrames/30)-2)]) {
    const previewFrame = Math.min(composition.durationInFrames-1,seconds*30);
    await renderStill({...common,frame:previewFrame,output:`../review/${composition.id}-${seconds}s.png`});
  }
  const clip = clips.find(c=>c.id===composition.id);
  for (const [index,visual] of clip.cutaways.entries()) {
    const time = visual.at + Math.min(1,visual.duration/2);
    await renderStill({...common,frame:Math.round(time*30),output:`../review/${composition.id}-${visual.layout}-${index}.png`});
  }
  if(process.argv.includes('--stills-only'))continue;
  console.log(`Rendering ${composition.id}: ${composition.durationInFrames} frames`);
  let last = -1;
  await renderMedia({...common,codec:'h264',crf:18,pixelFormat:'yuv420p',audioCodec:'aac',audioBitrate:'192k',concurrency:4,outputLocation:`../clips/${composition.id}.mp4`,
    onProgress:({progress})=>{const n=Math.floor(progress*10);if(n>last){console.log(`${composition.id}: ${n*10}%`);last=n;}}});
}
