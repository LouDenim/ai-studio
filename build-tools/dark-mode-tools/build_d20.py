import json
A = json.load(open('/root/homepage-mockups/assets.json'))

BASE_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Jost:wght@300;400;500;600;700;800&display=swap');
:root{--pink:#E7549F;--pink2:#ff7fc0}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
@media (prefers-reduced-motion: reduce){html{scroll-behavior:auto}}
body{font-family:'Jost',sans-serif;background:#0a0a0c;color:#fff;-webkit-font-smoothing:antialiased;overflow-x:hidden}
a{color:inherit;text-decoration:none}
"""

css_d = """
header{position:sticky;top:0;z-index:30;background:#0a0a0c}
.hbar{max-width:1220px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;padding:22px 28px;gap:20px}
.brand{display:flex;align-items:center;gap:14px}
.brand span{font-size:15px;letter-spacing:.16em;font-weight:600;color:var(--pink2)}
nav{display:flex;gap:22px;align-items:center;flex-wrap:wrap}
nav a{font-size:14px;letter-spacing:.06em;color:#d8d8dc;white-space:nowrap}
nav a:hover,nav a.on{color:var(--pink2)}
.langs{display:flex;gap:6px}
.langs a{font-size:11px;letter-spacing:.1em;border:1px solid var(--pink2);color:var(--pink2);padding:5px 11px;border-radius:999px}
.langs a.on{background:var(--pink2);color:#0a0a0c;border-color:var(--pink2)}
.burger{display:none}

.glowwrap{position:relative;padding:0 28px 12px;text-align:center;overflow:hidden}
#dotfx{position:absolute;top:0;left:0;width:100%;height:100%;z-index:0;pointer-events:none}
@media (prefers-reduced-motion: reduce){#dotfx{display:none}}

.masthead{position:relative;z-index:2;display:flex;flex-direction:column;align-items:center;padding:26px 0 0}
.masthead .mlogo{height:136px;filter:brightness(0) invert(1);margin-bottom:2px}
.masthead .mrole{font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:var(--pink2);font-weight:500}

.glowwrap h1{position:relative;z-index:2;font-size:56px;font-weight:700;line-height:1.1;letter-spacing:-.01em;
  max-width:880px;margin:26px auto 0}
.glowwrap h1 span{color:var(--pink2)}

.trustedby{position:relative;z-index:2;margin:20px 0 0;font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:#f0f0f2}

.logostrip{position:relative;z-index:2;max-width:500px;margin:14px auto 0;padding:0 28px;overflow:hidden;
  -webkit-mask-image:linear-gradient(to right,transparent,#000 8%,#000 92%,transparent);
  mask-image:linear-gradient(to right,transparent,#000 8%,#000 92%,transparent)}
.logostrip .track{display:flex;width:max-content;animation:logoscroll 32s linear infinite}
.logostrip .seq{display:flex;align-items:center;gap:50px;padding-right:50px}
.logostrip:hover .track{animation-play-state:paused}
.logostrip img{height:20px;filter:grayscale(1) brightness(0) invert(1);opacity:.5}
.logostrip img.banga{filter:grayscale(1) brightness(1.6) contrast(1.15);opacity:.6;height:24px}
@keyframes logoscroll{from{transform:translateX(0)}to{transform:translateX(-50%)}}
@media (prefers-reduced-motion: reduce){.logostrip .track{animation:none}}

.statement{position:relative;z-index:2;margin:0;padding:40px 28px 0;text-align:center}
.statement p{font-size:19px;font-weight:500;line-height:1.5;color:#f0f0f2;white-space:nowrap;
  position:relative;display:inline-block}
.statement p span{color:var(--pink2)}
.statement .ghost{visibility:hidden}
.statement .typed{position:absolute;left:0;top:0;white-space:nowrap;text-align:left}
.statement .tpre{color:#f0f0f2}
.statement .tpow{color:var(--pink2)}
.statement .caret{display:inline-block;width:2px;height:1em;background:var(--pink2);margin-left:2px;
  vertical-align:-0.12em;animation:blink .85s step-end infinite}
@keyframes blink{50%{opacity:0}}
.statement p span.lit{display:inline-block;transform-origin:left center;animation:powerbloom .9s ease-in-out}
@keyframes powerbloom{
  0%{transform:scale(1);color:var(--pink2);text-shadow:0 0 0 rgba(255,127,192,0)}
  45%{transform:scale(1.07);color:#ffeaf4;
    text-shadow:0 0 6px rgba(255,214,234,.95),0 0 18px rgba(255,127,192,1),0 0 42px rgba(255,84,170,.85),0 0 85px rgba(231,84,159,.55)}
  100%{transform:scale(1);color:var(--pink2);text-shadow:0 0 0 rgba(255,127,192,0)}
}

.boxes{max-width:1180px;margin:22px auto 0;padding:0 28px;display:grid;grid-template-columns:1fr 1fr;column-gap:20px;row-gap:0;position:relative;z-index:2}
.box{position:relative;height:320px;border-radius:20px;overflow:hidden;display:block}
/* desktop: video + models side by side (row 1), sentence full-width below (row 2) */
.boxes .videobox{grid-column:1;grid-row:1}
.boxes .models-box{grid-column:2;grid-row:1}
.boxes .statement{grid-column:1 / -1;grid-row:2}
.box img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform .5s;filter:saturate(1.05)}
.box:hover img{transform:scale(1.05)}
.box::after{content:'';position:absolute;inset:0;background:linear-gradient(to top,rgba(0,0,0,.75),rgba(0,0,0,.05) 55%)}
.box .txt{position:absolute;left:32px;right:32px;bottom:24px;z-index:2}
.box .txt h2{font-size:36px;font-weight:700}
.box .txt p{font-size:14px;font-weight:300;margin-top:6px;color:#d8d8dc}
.box .badge{position:absolute;left:28px;top:22px;z-index:2;display:inline-flex;align-items:center;gap:8px;
  background:rgba(0,0,0,.45);border:1px solid rgba(255,255,255,.25);padding:6px 14px;border-radius:999px;font-size:11.5px;
  letter-spacing:.1em;text-transform:uppercase;backdrop-filter:blur(4px)}
.box .badge .dot{width:7px;height:7px;border-radius:50%;background:var(--pink2)}

.videobox{background:radial-gradient(120% 140% at 30% 20%, #2a2a30 0%, #101014 60%, #0a0a0c 100%)}
/* self-hosted MP4 background: object-fit:cover crops to fill the box at ANY aspect ratio
   (desktop / portrait / landscape), no YouTube chrome, no logo, no captions, no 'More videos' */
.videobox .bgvid{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:1;pointer-events:none;border:0}
.videobox .txt{z-index:3}
.sndbtn{position:absolute;right:14px;bottom:14px;z-index:4;width:40px;height:40px;border-radius:50%;padding:0;
  border:1px solid rgba(255,255,255,.35);background:rgba(0,0,0,.42);backdrop-filter:blur(4px);
  display:flex;align-items:center;justify-content:center;cursor:pointer;transition:.15s}
.sndbtn:hover{border-color:var(--pink2);background:rgba(0,0,0,.6)}
.sndbtn svg{width:19px;height:19px;fill:#fff;display:block}

.toolswrap{position:relative;z-index:2}
.tools{max-width:1180px;margin:40px auto 48px;padding:0 28px;display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
/* statement gap: 44px top (boxes->text) matches 20px+24px=44px bottom (text->tools) */
.tool{border:1px solid rgba(255,255,255,.14);border-radius:14px;padding:22px 20px;transition:.15s;background:rgba(255,255,255,.02)}
.tool:hover{border-color:var(--pink2);transform:translateY(-2px)}
.tool b{font-size:17px}
.tool span{display:block;font-size:13px;color:#a9a9b2;margin-top:6px;font-weight:300}
.tool em{display:block;font-size:12px;letter-spacing:.08em;text-transform:uppercase;margin-top:12px;font-style:normal;color:var(--pink2)}

footer{position:relative;z-index:2;text-align:center;padding:24px 28px 30px;font-size:11px;color:#8a8a92;letter-spacing:.1em;
  text-transform:uppercase}
footer a{color:#c7c7ce}
footer a:hover{color:var(--pink2)}
.social{display:flex;justify-content:center;align-items:center;gap:20px;margin-top:16px}
.social a{color:#8a8a92;display:inline-flex;line-height:0}
.social a:hover{color:var(--pink2)}
.social svg{width:16px;height:16px;fill:currentColor}

.about{position:relative;z-index:2;max-width:640px;margin:0 auto;padding:8px 28px 30px;text-align:center;scroll-margin-top:90px}
.about .ablabel{font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:var(--pink2);font-weight:500;margin-bottom:20px}
.about p{font-size:15.5px;line-height:1.7;color:#c9c9d0;font-weight:300;margin-bottom:15px}
.about p.portlink{margin-top:8px;margin-bottom:0;font-size:14px;letter-spacing:.03em;color:#d8d8dc}
.about p.portlink a{color:var(--pink2)}
.about p.portlink a:hover{text-decoration:underline}

/* ---------- MOBILE + landscape phone: burger menu + single-column stack ---------- */
/* portrait phones (narrow) OR landscape phones (short + landscape) both get the clean stack */
@media (max-width:760px), (max-height:500px) and (orientation:landscape){
  .hbar{padding:16px 20px;position:relative}
  /* collapse the full text nav behind a burger, top-left, aligned with AI STUDIO */
  .burger{display:flex;flex-direction:column;justify-content:center;gap:5px;width:30px;height:26px;cursor:pointer;order:-1;z-index:40}
  .burger span{display:block;width:26px;height:2px;background:#fff;border-radius:2px;transition:transform .25s,opacity .2s}
  .navtoggle:checked ~ .burger span:nth-child(1){transform:translateY(7px) rotate(45deg)}
  .navtoggle:checked ~ .burger span:nth-child(2){opacity:0}
  .navtoggle:checked ~ .burger span:nth-child(3){transform:translateY(-7px) rotate(-45deg)}
  nav{position:absolute;top:100%;left:0;right:0;flex-direction:column;align-items:stretch;gap:0;
    background:#0a0a0c;border-bottom:1px solid rgba(255,255,255,.1);padding:6px 0;display:none;
    box-shadow:0 18px 40px rgba(0,0,0,.55)}
  .navtoggle:checked ~ nav{display:flex}
  nav a{padding:14px 22px;font-size:15px;letter-spacing:.04em;border-bottom:1px solid rgba(255,255,255,.05)}
  nav a:last-child{border-bottom:0}
  .brand{margin-left:auto}
  .brand span{font-size:13px}

  .glowwrap{padding:0 20px 10px}
  .masthead{padding:20px 0 0}
  .masthead .mlogo{height:104px}
  .glowwrap h1{font-size:38px;margin:20px auto 0}
  .trustedby{margin:18px 0 0}
  .logostrip{max-width:100%;margin:12px auto 0}

  /* single column, reordered: video (Portfolio), then the sentence, then Models, then the 3 cards */
  .boxes{grid-template-columns:1fr;column-gap:0;row-gap:16px;margin:18px auto 0}
  .boxes .videobox{grid-column:1;grid-row:1}
  .boxes .statement{grid-column:1;grid-row:2}
  .boxes .models-box{grid-column:1;grid-row:3}
  .box{height:224px}
  .box .txt h2{font-size:30px}
  .statement{padding:2px 20px 2px}
  .statement p{white-space:normal;font-size:17px}
  .tools{grid-template-columns:1fr;margin:26px auto 40px;gap:12px}
  .about{padding:4px 22px 26px}
  .about p{font-size:15px}
}

/* landscape phone: shrink the masthead hard so the whole Portfolio video fits on first view */
@media (max-height:500px) and (orientation:landscape){
  .masthead{padding:8px 0 0}
  .masthead .mlogo{height:46px}
  .masthead .mrole{display:none}
  .glowwrap{padding-bottom:6px}
  .glowwrap h1{font-size:20px;margin:8px auto 0}
  .trustedby,.logostrip{display:none}
  /* 16:9, sized off viewport height so it sits fully on screen under the trimmed masthead */
  .box{height:auto;aspect-ratio:16 / 9;width:min(100%, calc(56vh * 16 / 9));margin-left:auto;margin-right:auto}
}
"""

# --- Hero dot animation (RESTORED: the quiet calibration Lou approved) -----
# Faint resting dot field across the hero, one slow soft-rose trail per side sweeping
# gracefully and passing behind the opaque logo. No halo/bloom (that was the nightclub
# ingredient), no static grid. Dots wrap down the left/right edges (vignette), fade out
# above the headline in the centre; bright glow is softly suppressed over the text zones.
DOTFX_JS = r"""
(function(){
var wrap=document.querySelector('.glowwrap'); if(!wrap) return;
var cv=document.getElementById('dotfx'); if(!cv) return;
var ctx=cv.getContext('2d');
var W=0,H=0,BH=400,fadeStart=240,fadeEnd=420,zones=[];
function measure(){
  var r=wrap.getBoundingClientRect();
  W=Math.round(r.width); H=Math.round(r.height);
  cv.width=W; cv.height=H;
  var mh=wrap.querySelector('.masthead');
  var mb= mh ? (mh.getBoundingClientRect().bottom - r.top) : H*0.34;
  fadeStart=mb+14; fadeEnd=mb+150; BH=fadeEnd;
  zones=[];
  wrap.querySelectorAll('h1,.trustedby,.logostrip,.mrole').forEach(function(el){
    var b=el.getBoundingClientRect();
    zones.push({cx:b.left+b.width/2-r.left, cy:b.top+b.height/2-r.top, rx:b.width/2, ry:b.height/2});
  });
}
measure(); addEventListener('resize',measure);
setTimeout(measure,300); setTimeout(measure,1000);
function rnd(a,b){return a+Math.random()*(b-a);}
/* vertical envelope varies with x: fades out above the headline in the CENTRE,
   but wraps all the way down the hero at the left/right EDGES */
function env(x,y){
  var t=Math.min(1,Math.abs(x-W/2)/(W/2));
  var edge=Math.pow(t,1.6);
  var fe=fadeEnd+(H-fadeEnd)*edge;
  var fs=fadeStart+(H*0.55-fadeStart)*edge;
  if(y<=fs)return 1; if(y>=fe)return 0; return 1-(y-fs)/(fe-fs);
}
function protectGlow(x,y){
  var p=1;
  for(var k=0;k<zones.length;k++){
    var z=zones[k];
    var nx=(x-z.cx)/(z.rx+55), ny=(y-z.cy)/(z.ry+26);
    var d=Math.sqrt(nx*nx+ny*ny);
    var f=Math.min(1,Math.max(0,(d-1)/0.8));
    if(f<p)p=f;
  }
  return p;
}
var SP=32;
function makeSide(side){
  var spin=side==='L'?-1:1;
  var spd=spin*rnd(0.13,0.17);
  var cxF=side==='L'?rnd(0.24,0.31):rnd(0.69,0.76);
  return [0,1].map(function(i){return {
    cxF:cxF, cyF:rnd(0.24,0.36),
    rxF:rnd(0.34,0.44), ryF:rnd(0.34,0.52),
    ang0:i*Math.PI+rnd(-0.15,0.15), angSpd:spd,
    h2Amp:rnd(0.05,0.10), h2Mult:rnd(2.0,2.6)*Math.sign(spd), h2Ph:rnd(0,6.283),
    v2Amp:rnd(0.04,0.08), v2Mult:rnd(1.5,2.0)*Math.sign(spd), v2Ph:rnd(0,6.283),
    t0:performance.now()
  };});
}
var comets=makeSide('R').concat(makeSide('L'));
function pos(c,th){
  var x=W*c.cxF + W*c.rxF*Math.cos(th) + W*c.h2Amp*Math.cos(th*c.h2Mult+c.h2Ph);
  var y=BH*c.cyF + BH*c.ryF*Math.sin(th) + BH*c.v2Amp*Math.sin(th*c.v2Mult+c.v2Ph);
  return [x,y];
}
var TRAIL=30, DTH=0.05, HIT=150;
function draw(now){
  ctx.clearRect(0,0,W,H);
  var trail=[];
  for(var ci=0;ci<comets.length;ci++){
    var c=comets[ci];
    var th=c.ang0+(now-c.t0)/1000*c.angSpd;
    for(var k=0;k<TRAIL;k++){ trail.push({p:pos(c,th-k*DTH), decay:Math.max(0,1-k/TRAIL)}); }
  }
  for(var x=SP/2;x<W;x+=SP){
    for(var y=SP/2;y<H;y+=SP){
      var e=env(x,y); if(e<=0.01) continue;
      var lit=0;
      for(var t=0;t<trail.length;t++){
        var q=trail[t]; if(q.decay<=0) continue;
        var dx=x-q.p[0], dy=y-q.p[1];
        var d=Math.sqrt(dx*dx+dy*dy);
        if(d<HIT){ var v=(1-d/HIT)*q.decay; if(v>lit) lit=v; }
      }
      var glow=lit*protectGlow(x,y);
      /* quiet: faint resting field, soft rose accent, no solid hot blocks */
      var o=(0.12+glow*0.72)*e;
      if(o<=0.012) continue;
      var R=Math.round(140+(246-140)*glow);
      var G=Math.round(140+(122-140)*glow);
      var B=Math.round(150+(184-150)*glow);
      var rad=1.0+glow*2.2;
      ctx.beginPath(); ctx.arc(x,y,rad,0,6.283);
      ctx.fillStyle='rgba('+R+','+G+','+B+','+o.toFixed(3)+')'; ctx.fill();
    }
  }
  requestAnimationFrame(draw);
}
requestAnimationFrame(draw);
})();
"""

# --- Typewriter on the bio statement --------------------------------------
# The sentence types itself out like a prompt being written (slightly irregular rhythm),
# then "super-pouvoirs IA." blooms with a soft pink glow that settles and stays faint.
# Plays once, when the line scrolls into view. Layout never shifts: the full sentence
# is kept invisibly in place (ghost) while the typed copy overlays it, then the original
# markup is restored at the end. Skipped entirely under prefers-reduced-motion / no-JS
# (text is server-rendered, so it is always present).
TYPE_JS = r"""
(function(){
if(matchMedia('(prefers-reduced-motion: reduce)').matches) return;
/* on phones the typed line is nowrap and gets cut ('...years'), then jumps to the wrapped
   version — skip the animation on mobile and just show the full sentence, wrapped, in place */
if(matchMedia('(max-width:760px)').matches) return;
var p=document.querySelector('.statement p'); if(!p) return;
var span=p.querySelector('span'); if(!span) return;
var pre=''; p.childNodes.forEach(function(n){ if(n.nodeType===3) pre+=n.textContent; if(n===span) return; });
pre=p.childNodes[0].nodeType===3?p.childNodes[0].textContent:'';
var pow=span.textContent;
var orig=p.innerHTML;
var done=false;
function run(){
  if(done) return; done=true;
  p.innerHTML='<span class="ghost">'+orig+'</span><span class="typed"><span class="tpre"></span><span class="tpow"></span><span class="caret"></span></span>';
  var tpre=p.querySelector('.tpre'), tpow=p.querySelector('.tpow');
  var i=0, j=0;
  function tick(){
    if(i<pre.length){ tpre.textContent=pre.slice(0,++i); }
    else if(j<pow.length){ tpow.textContent=pow.slice(0,++j); }
    else{
      setTimeout(function(){
        p.innerHTML=orig;
        p.querySelector('span').classList.add('lit');
      },120);
      return;
    }
    setTimeout(tick,30+Math.random()*8);
  }
  setTimeout(tick,180);
}
if('IntersectionObserver' in window){
  var io=new IntersectionObserver(function(es){ es.forEach(function(e){ if(e.isIntersecting){ io.disconnect(); run(); } }); },{threshold:0.9});
  io.observe(p);
}else{ run(); }
})();
"""

PLAY_SVG = '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M8 5.5v13l11-6.5z"/></svg>'

SND_OFF_SVG = '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M16.5 12c0-1.77-1.02-3.29-2.5-4.03v2.21l2.45 2.45c.03-.2.05-.41.05-.63zm2.5 0c0 .94-.2 1.82-.54 2.64l1.51 1.51C20.63 14.91 21 13.5 21 12c0-4.28-2.99-7.86-7-8.77v2.06c2.89.86 5 3.54 5 6.71zM4.27 3 3 4.27 7.73 9H3v6h4l5 5v-6.73l4.25 4.25c-.67.52-1.42.93-2.25 1.18v2.06c1.38-.31 2.63-.95 3.69-1.81L19.73 21 21 19.73 4.27 3zM12 4 9.91 6.09 12 8.18V4z"/></svg>'
SND_ON_SVG = '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"/></svg>'

# Hero sound toggle: video starts muted (browsers require it for autoplay); one tap unmutes.
# preventDefault/stopPropagation so tapping the button never follows the Portfolio link.
SND_JS = ("""
(function(){
var OFF=%s, ON=%s;
document.querySelectorAll('.videobox').forEach(function(box){
  var v=box.querySelector('.bgvid'), b=box.querySelector('.sndbtn'); if(!v||!b) return;
  b.addEventListener('click',function(e){e.preventDefault();e.stopPropagation();
    v.muted=!v.muted;
    if(!v.muted){ v.volume=1; var p=v.play(); if(p&&p.catch){p.catch(function(){});} }
    b.innerHTML=v.muted?OFF:ON;
    b.setAttribute('aria-label', v.muted?'Sound off':'Sound on');
  });
});
})();
""" % (json.dumps(SND_OFF_SVG), json.dumps(SND_ON_SVG)))

IG_SVG = '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 2.2c3.2 0 3.6 0 4.9.1 1.2.1 1.9.2 2.3.4.6.2 1 .5 1.4.9.4.4.7.8.9 1.4.2.4.3 1.1.4 2.3.1 1.3.1 1.7.1 4.9s0 3.6-.1 4.9c-.1 1.2-.2 1.9-.4 2.3-.2.6-.5 1-.9 1.4-.4.4-.8.7-1.4.9-.4.2-1.1.3-2.3.4-1.3.1-1.7.1-4.9.1s-3.6 0-4.9-.1c-1.2-.1-1.9-.2-2.3-.4-.6-.2-1-.5-1.4-.9-.4-.4-.7-.8-.9-1.4-.2-.4-.3-1.1-.4-2.3-.1-1.3-.1-1.7-.1-4.9s0-3.6.1-4.9c.1-1.2.2-1.9.4-2.3.2-.6.5-1 .9-1.4.4-.4.8-.7 1.4-.9.4-.2 1.1-.3 2.3-.4 1.3-.1 1.7-.1 4.9-.1M12 0C8.7 0 8.3 0 7 .1c-1.3.1-2.2.3-3 .6-.8.3-1.5.7-2.2 1.4C1.1 2.8.7 3.5.4 4.3c-.3.8-.5 1.7-.6 3C-.1 8.3-.1 8.7-.1 12s0 3.7.1 5c.1 1.3.3 2.2.6 3 .3.8.7 1.5 1.4 2.2.7.7 1.4 1.1 2.2 1.4.8.3 1.7.5 3 .6 1.3.1 1.7.1 5 .1s3.7 0 5-.1c1.3-.1 2.2-.3 3-.6.8-.3 1.5-.7 2.2-1.4.7-.7 1.1-1.4 1.4-2.2.3-.8.5-1.7.6-3 .1-1.3.1-1.7.1-5s0-3.7-.1-5c-.1-1.3-.3-2.2-.6-3-.3-.8-.7-1.5-1.4-2.2C21.2 1.1 20.5.7 19.7.4c-.8-.3-1.7-.5-3-.6C15.7 0 15.3 0 12 0z"/><path d="M12 5.8A6.2 6.2 0 1 0 18.2 12 6.2 6.2 0 0 0 12 5.8zm0 10.2A4 4 0 1 1 16 12a4 4 0 0 1-4 4z"/><circle cx="18.4" cy="5.6" r="1.4"/></svg>'

LI_SVG = '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M20.45 20.45h-3.56v-5.57c0-1.33-.02-3.03-1.85-3.03-1.85 0-2.14 1.45-2.14 2.94v5.66H9.34V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.45v6.29zM5.34 7.43a2.07 2.07 0 1 1 0-4.13 2.07 2.07 0 0 1 0 4.13zM7.12 20.45H3.56V9h3.56v11.45z"/></svg>'

X_SVG = '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>'

YT_SVG = '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M23.5 6.2a3 3 0 0 0-2.1-2.1C19.4 3.5 12 3.5 12 3.5s-7.4 0-9.4.6A3 3 0 0 0 .5 6.2 31 31 0 0 0 0 12a31 31 0 0 0 .5 5.8 3 3 0 0 0 2.1 2.1c2 .6 9.4.6 9.4.6s7.4 0 9.4-.6a3 3 0 0 0 2.1-2.1A31 31 0 0 0 24 12a31 31 0 0 0-.5-5.8zM9.6 15.5V8.5l6.3 3.5-6.3 3.5z"/></svg>'

FB_SVG = '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M13.5 21v-8.1h2.7l.4-3.2h-3.1V7.7c0-.9.3-1.6 1.6-1.6h1.6V3.3C16.4 3.2 15.3 3 14 3c-2.6 0-4.4 1.6-4.4 4.5v2.2H6.9v3.2h2.7V21h3.9z"/></svg>'
TT_SVG = '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M16.6 5.82c-.86-.9-1.34-2.07-1.34-3.32h-3.02v13.44c0 1.5-1.22 2.72-2.72 2.72-1.5 0-2.72-1.22-2.72-2.72 0-1.5 1.22-2.72 2.72-2.72.28 0 .55.04.8.12V10.3a5.7 5.7 0 0 0-.8-.06 5.74 5.74 0 1 0 5.74 5.74V8.86a8.3 8.3 0 0 0 4.86 1.56V7.4a5.34 5.34 0 0 1-3.52-1.58z"/></svg>'

SOCIAL_HTML = f"""<div class="social">
    <a href="https://www.instagram.com/loudenim" target="_blank" rel="noopener" aria-label="Instagram">{IG_SVG}</a>
    <a href="https://www.linkedin.com/in/loudenim" target="_blank" rel="noopener" aria-label="LinkedIn">{LI_SVG}</a>
    <a href="https://x.com/loudenim" target="_blank" rel="noopener" aria-label="X">{X_SVG}</a>
    <a href="https://www.youtube.com/@loudenim" target="_blank" rel="noopener" aria-label="YouTube">{YT_SVG}</a>
    <a href="https://www.tiktok.com/@loudenim" target="_blank" rel="noopener" aria-label="TikTok">{TT_SVG}</a>
  </div>"""

def body(lang):
    if lang == 'fr':
        nav_home, nav_grille, nav_sim, nav_brief = "Accueil","Grille tarifaire","Simulateur","Brief vidéo"
        nav_portfolio, nav_models = "Portfolio", "Mod&egrave;les"
        nav_about = "&Agrave; propos"
        role = "Directeur artistique IA"
        h1 = "L&rsquo;IA g&eacute;n&eacute;rative pour les <span>marques.</span>"
        bio = "Photographe &eacute;ditorial et pub depuis 25 ans, arm&eacute;e de <span>super-pouvoirs IA.</span>"
        trusted_by = "Ils m&rsquo;ont fait confiance"
        b_models, p_models = "Mod&egrave;les", "32 visages IA, coh&eacute;rents d&rsquo;une image &agrave; l&rsquo;autre."
        badge_v, badge_m = "Vid&eacute;o", "Mod&egrave;le IA"
        portfolio_title, portfolio_sub = "Portfolio", "Vid&eacute;os et images IA, format cin&eacute;ma et vertical."
        portfolio_href = "mockup-travail-d2.html"
        models_href = "mockup-models-d2.html"
        home_href = "mockup-d20.html"
        lang_href = "mockup-d20-en.html"
        grille_href, devis_href, brief_href = "mockup-grille-preview.html", "mockup-devis-preview.html", "mockup-brief-preview.html"
        t1b,t1s,t1e = "Grille tarifaire","Tous les prix, clairs et sans surprise.","Voir les tarifs"
        t2b,t2s,t2e = "Simulateur de devis","Composez votre projet, recevez une estimation en direct.","Estimer mon projet"
        t3b,t3s,t3e = "Brief vid&eacute;o","Le formulaire pour lancer votre projet dans de bonnes conditions.","Remplir le brief"
        about_label = "&Agrave; propos"
        bio_p1 = "Photographe de m&eacute;tier, j&rsquo;ai construit l&rsquo;essentiel de ma carri&egrave;re &agrave; Londres, dans l&rsquo;&eacute;ditorial et la publicit&eacute;."
        bio_p2 = "J&rsquo;ai photographi&eacute; une grande diversit&eacute; de personnalit&eacute;s&nbsp;: des acteurs comme Liv Tyler et Sean Bean, des musiciens comme Robbie Williams, mais aussi des humoristes, des animateurs t&eacute;l&eacute; et des sportifs. C&ocirc;t&eacute; publicit&eacute;, j&rsquo;ai eu la chance de collaborer avec des marques comme H&amp;M, Rimmel London ou L&rsquo;Or&eacute;al, pour n&rsquo;en citer que quelques-unes."
        bio_p3 = "La g&eacute;n&eacute;ration d&rsquo;images et de vid&eacute;os par IA a ouvert de nouveaux horizons. C&rsquo;est un outil de plus dans ma palette cr&eacute;ative, au service de mes clients."
        bio_link = 'D&eacute;couvrez mon portfolio photo sur <a href="https://www.loudenim.com" target="_blank" rel="noopener">loudenim.com</a>'
        title = "LOU DENIM — AI Studio"
        lang_fr_on, lang_en_on = "on", ""
        foot = f'''<div class="footline"><a href="mailto:lou@loudenim.com">lou@loudenim.com</a> &middot; <a href="tel:+590690299544">+590&nbsp;(0)690&nbsp;299&nbsp;544</a> &middot; <a href="https://www.loudenim.com" target="_blank" rel="noopener">Photographie&nbsp;: loudenim.com</a></div>{SOCIAL_HTML}'''
    else:
        nav_home, nav_grille, nav_sim, nav_brief = "Home","Rate card","Simulator","Video brief"
        nav_portfolio, nav_models = "Portfolio", "Models"
        nav_about = "About"
        role = "AI Creative Director"
        h1 = "Generative AI for <span>brands.</span>"
        bio = "Editorial and advertising photographer for 25+ years. Now with <span>AI superpowers.</span>"
        trusted_by = "Trusted by"
        b_models, p_models = "Models", "32 AI faces, consistent from one image to the next."
        badge_v, badge_m = "Video", "AI model"
        portfolio_title, portfolio_sub = "Portfolio", "AI videos and images, cinematic and vertical formats."
        portfolio_href = "mockup-travail-d2-en.html"
        models_href = "mockup-models-d2-en.html"
        home_href = "mockup-d20-en.html"
        lang_href = "mockup-d20.html"
        grille_href, devis_href, brief_href = "mockup-grille-en-preview.html", "mockup-devis-en-preview.html", "mockup-brief-en-preview.html"
        t1b,t1s,t1e = "Rate card","All prices, clear and upfront.","View the rates"
        t2b,t2s,t2e = "Quote simulator","Build your project, get a live estimate.","Estimate my project"
        t3b,t3s,t3e = "Video brief","The form to start your project on solid ground.","Fill in the brief"
        about_label = "About"
        bio_p1 = "I&rsquo;m a photographer by trade and built most of my career in London, UK, in the editorial and advertising industry."
        bio_p2 = "I&rsquo;ve worked with a diverse range of celebrities, from film stars like Liv Tyler and Sean Bean to musicians like Robbie Williams, as well as comedians, TV presenters and sports stars. On the advertising side, I&rsquo;ve had the opportunity to work for brands such as H&amp;M, Rimmel London or L&rsquo;Or&eacute;al, to name a few."
        bio_p3 = "I started experimenting with AI, pushing my craft in new directions. I got hooked straight away. Now it&rsquo;s another tool in my creative kit, one more way to create high-end visuals for my clients."
        bio_link = 'See my photography portfolio at <a href="https://www.loudenim.com" target="_blank" rel="noopener">loudenim.com</a>'
        title = "LOU DENIM — AI Studio"
        lang_fr_on, lang_en_on = "", "on"
        foot = f'''<div class="footline"><a href="mailto:lou@loudenim.com">lou@loudenim.com</a> &middot; <a href="tel:+590690299544">+590&nbsp;(0)690&nbsp;299&nbsp;544</a> &middot; <a href="https://www.loudenim.com" target="_blank" rel="noopener">Photography&nbsp;: loudenim.com</a></div>{SOCIAL_HTML}'''

    return title, f"""
<header><div class="hbar">
  <input type="checkbox" id="navtoggle" class="navtoggle" hidden>
  <label for="navtoggle" class="burger" aria-label="Menu"><span></span><span></span><span></span></label>
  <nav>
    <a class="on" href="{home_href}">{nav_home}</a>
    <a href="{portfolio_href}">{nav_portfolio}</a>
    <a href="{models_href}">{nav_models}</a>
    <a href="{grille_href}">{nav_grille}</a>
    <a href="{devis_href}">{nav_sim}</a>
    <a href="{brief_href}">{nav_brief}</a>
    <a href="#about">{nav_about}</a>
  </nav>
  <div class="brand"><span>AI STUDIO</span>
    <div class="langs"><a class="{lang_en_on}" href="{lang_href if lang_fr_on else home_href}">EN</a><a class="{lang_fr_on}" href="{home_href if lang_fr_on else lang_href}">FR</a></div>
  </div>
</div></header>

<div class="glowwrap">
  <canvas id="dotfx"></canvas>
  <a class="masthead" href="https://www.loudenim.com" target="_blank" rel="noopener" title="loudenim.com">
    <img class="mlogo" src="{A['logo']}">
    <div class="mrole">{role}</div>
  </a>
  <h1>{h1}</h1>
  <div class="trustedby">{trusted_by}</div>
  <div class="logostrip"><div class="track">
    <div class="seq">
      <img src="{A['logo_kfc']}"><img src="{A['logo_milenis']}"><img src="{A['logo_pampryl']}">
      <img src="{A['logo_sosh']}"><img class="banga" src="{A['logo_banga']}"><img src="{A['logo_mcdo']}">
    </div>
    <div class="seq">
      <img src="{A['logo_kfc']}"><img src="{A['logo_milenis']}"><img src="{A['logo_pampryl']}">
      <img src="{A['logo_sosh']}"><img class="banga" src="{A['logo_banga']}"><img src="{A['logo_mcdo']}">
    </div>
  </div></div>
</div>

<div class="boxes">
  <a class="box videobox" href="{portfolio_href}">
    <video class="bgvid" autoplay muted loop playsinline preload="auto" poster="hero-poster.jpg"><source src="hero.mp4" type="video/mp4"></video>
    <button class="sndbtn" type="button" aria-label="Sound off">{SND_OFF_SVG}</button>
    <div class="txt"><h2>{portfolio_title}</h2><p>{portfolio_sub}</p></div>
  </a>
  <div class="statement"><p>{bio}</p></div>
  <a class="box models-box" href="{models_href}">
    <img src="{A['models_face']}">
    <div class="txt"><h2>{b_models}</h2><p>{p_models}</p></div>
  </a>
</div>

<div class="toolswrap">
  <div class="tools">
    <a class="tool" href="{grille_href}"><b>{t1b}</b><span>{t1s}</span><em>{t1e}</em></a>
    <a class="tool" href="{devis_href}"><b>{t2b}</b><span>{t2s}</span><em>{t2e}</em></a>
    <a class="tool" href="{brief_href}"><b>{t3b}</b><span>{t3s}</span><em>{t3e}</em></a>
  </div>
</div>
<section class="about" id="about">
  <div class="ablabel">{about_label}</div>
  <p>{bio_p1}</p>
  <p>{bio_p2}</p>
  <p>{bio_p3}</p>
  <p class="portlink">{bio_link}</p>
</section>
<footer>{foot}</footer>
"""

for lang, fname in [('fr','mockup-d20.html'), ('en','mockup-d20-en.html')]:
    title, b = body(lang)
    html = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>{BASE_CSS}
{css_d}
</style>
</head>
<body>
{b}
<script>{TYPE_JS}</script>
<script>{DOTFX_JS}</script>
<script>{SND_JS}</script>
</body>
</html>"""
    open(f'/root/homepage-mockups/{fname}','w').write(html)
    print("built", fname)
