import React, {useEffect, useState} from 'react';
import {AbsoluteFill, Audio, Composition, OffthreadVideo, Img, staticFile, useCurrentFrame, useVideoConfig, registerRoot, delayRender, continueRender, cancelRender} from 'remotion';
import clips from '../clips.json';
import style from '../style.json';

function Clip({clip}) {
  const [fontHandle] = useState(() => delayRender('Load Space Grotesk'));
  useEffect(() => {
    const font = new FontFace(style.font.family, `url(${staticFile(style.font.file)})`, {weight:'300 700'});
    font.load().then(loaded => {document.fonts.add(loaded); continueRender(fontHandle);}).catch(cancelRender);
  }, [fontHandle]);
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const time = frame / fps;
  const caption = clip.captions.find(c => time >= c.start && time < c.end);
  const cutaway = clip.cutaways.find(c => time >= c.at && time < c.at+c.duration);
  const split = cutaway?.layout === 'split';
  const visualZoom = cutaway ? 1 + style.visuals.pushScale*(time-cutaway.visualStart)/(cutaway.visualEnd-cutaway.visualStart) : 1;
  const segmentIndex = clip.segments.findIndex(s => time < s.outputEnd);
  const segment = clip.segments[Math.max(0,segmentIndex)];
  // Alternate punch crops at actual edits, adding an extra hard cut to long uninterrupted shots.
  const beat = Math.floor((time-segment.outputStart)/style.editing.longShotReframeSeconds);
  const tight = (Math.max(0,segmentIndex)+beat)%2 === 1;
  const zoom = tight ? style.editing.punchScale : 1;
  return <AbsoluteFill style={{background:'#f7faf9',overflow:'hidden',fontFamily:style.font.family}}>
    {clip.soundEffect && <Audio src={staticFile(clip.soundEffect.media)} volume={clip.soundEffect.volume}/>}
    <OffthreadVideo src={staticFile(clip.media)} style={{width:'100%',height:'100%',objectFit:'cover',transform:`scale(${zoom})`,transformOrigin:'50% 32%'}}/>
    {cutaway && <div style={{position:'absolute',left:0,right:0,top:split?style.visuals.splitY:0,bottom:0,overflow:'hidden'}}>
      <Img src={staticFile(cutaway.image)} style={{width:'100%',height:'100%',objectFit:'cover',objectPosition:cutaway.objectPosition,transform:`scale(${visualZoom})`}}/>
    </div>}
    {split && <div style={{position:'absolute',left:0,right:0,top:0,height:style.visuals.splitY,overflow:'hidden'}}>
      <OffthreadVideo muted src={staticFile(clip.splitMedia)} style={{width:'100%',height:'100%',objectFit:'cover',objectPosition:'50% 38%',transform:`scale(${tight?1.04:1})`,transformOrigin:'50% 30%'}}/>
    </div>}
    {caption && <div style={{position:'absolute',left:style.captions.left,right:style.captions.right,bottom:style.captions.bottom,display:'flex',justifyContent:'center',pointerEvents:'none'}}>
      <div style={{maxWidth:style.captions.maxWidth,color:style.captions.color,background:style.captions.background,padding:style.captions.padding,borderRadius:style.captions.borderRadius,fontSize:style.captions.fontSize,lineHeight:style.captions.lineHeight,fontWeight:style.captions.fontWeight,letterSpacing:style.captions.letterSpacing,textAlign:'center',boxShadow:'0 7px 28px rgba(0,0,0,0.15)'}}>
        {caption.words.map((word,i) => <React.Fragment key={i}>
          {i > 0 && !/^[,.;!?]/.test(word.word.trim()) ? ' ' : ''}
          <span style={{color:style.captions.highlightActiveWord && time>=word.start && time<word.end ? clip.color : style.captions.color}}>{word.word.trim()}</span>
        </React.Fragment>)}
      </div>
    </div>}
    {frame === 0 && clip.cover && <AbsoluteFill>
      <div style={{position:'absolute',left:0,right:0,top:0,height:style.visuals.splitY,overflow:'hidden'}}>
        <Img src={staticFile(clip.cover.camera)} style={{width:'100%',height:'100%',objectFit:'cover',objectPosition:'50% 38%'}}/>
      </div>
      <div style={{position:'absolute',left:0,right:0,top:style.visuals.splitY,bottom:0,overflow:'hidden'}}>
        <Img src={staticFile(clip.cover.image)} style={{width:'100%',height:'100%',objectFit:'cover',objectPosition:clip.cover.objectPosition}}/>
      </div>
      <div style={{position:'absolute',left:style.captions.left,right:style.captions.right,top:style.visuals.splitY,transform:'translateY(-50%)',display:'flex',justifyContent:'center'}}>
        <div style={{maxWidth:950,padding:style.cover.padding,borderRadius:style.cover.borderRadius,background:style.cover.background,color:'#ffffff',fontSize:style.cover.fontSize,fontWeight:style.cover.fontWeight,lineHeight:style.cover.lineHeight,letterSpacing:style.cover.letterSpacing,textAlign:'center',textWrap:'balance',boxShadow:'0 7px 28px rgba(0,0,0,0.2)'}}>{clip.title}</div>
      </div>
    </AbsoluteFill>}
  </AbsoluteFill>;
}
function Root() {
  return clips.map(clip=><Composition key={clip.id} id={clip.id} component={Clip} width={style.canvas.width} height={style.canvas.height} fps={style.canvas.fps} durationInFrames={Math.round(clip.duration*style.canvas.fps)} defaultProps={{clip}}/>);
}
registerRoot(Root);
