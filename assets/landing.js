(() => {
const INK='205,196,186';
function drawBell(cv,ink){if(!cv)return;const x=cv.getContext('2d');x.setTransform(1,0,0,1,0,0);x.clearRect(0,0,cv.width,cv.height);x.scale(2,2);x.fillStyle=`rgb(${ink})`;const W=184,H=238;
const dark=(X,Y)=>{const kd=Math.hypot(X,Y-20);if(kd<12&&kd>5.5)return .9;let r=0;if(Y>=30&&Y<48)r=30*Math.sqrt((Y-30)/18);else if(Y>=48&&Y<180)r=30+32*Math.pow((Y-48)/132,1.7);else if(Y>=180&&Y<=198)r=62+26*Math.pow((Y-180)/18,.7);
if(r>0&&Math.abs(X)<r){const nx=X/r;let b=.1+.78*Math.max(0,-.55*nx+.83*Math.sqrt(1-nx*nx))+.3*Math.exp(-Math.pow((nx+.42)/.13,2));let d=1-Math.min(1,b);if(Math.abs(Y-62)<2.2||Math.abs(Y-172)<2.2||Math.abs(Y-190)<1.6)d=Math.min(1,d+.45);if(Y>194)d=Math.min(1,d+.25);return d}
const cd=Math.hypot(X,Y-207);if(cd<9)return .55+.4*(X/9+1)/2;const e=(X/82)**2+((Y-226)/6)**2;if(e<1)return .45*(1-e);return 0};
const cell=5,a=Math.PI/4,co=Math.cos(a),si=Math.sin(a),D=Math.hypot(W,H);
for(let i=-D;i<D;i+=cell)for(let j=-D;j<D;j+=cell){const px=W/2+i*co-j*si,py=H/2+i*si+j*co;if(px<-4||py<-4||px>W+4||py>H+4)continue;const d=dark(px-W/2,py);if(d<.04)continue;x.beginPath();x.arc(px,py,cell*.5*Math.sqrt(d)*1.08,0,7);x.fill()}}

let lenis=null,raf=null;
function setup(){
    const g=window.gsap,ST=window.ScrollTrigger,root=document.querySelector('[data-root]');if(!g||!ST||!root)return;
    g.registerPlugin(ST);const q=g.utils.selector(root);
    const reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    g.context(()=>{
      const label=q('[data-label]')[0];
      const secs=q('[data-sec]');const pickLabel=()=>{const mid=innerHeight/2;for(const s of secs){const r=s.getBoundingClientRect();if(r.top<=mid&&r.bottom>=mid){if(label&&label.textContent!==s.dataset.sec)label.textContent=s.dataset.sec;return}}};g.ticker.add(pickLabel);
      if(reduce){g.set(q('[data-pf]'),{scale:1});g.set(q('[data-poff]'),{opacity:0});g.set(q('[data-pon]'),{opacity:1});g.set(q('[data-cdres]'),{opacity:1});q('[data-cd]')[0].textContent='0';g.set(q('[data-nt]'),{opacity:1});g.set(q('[data-nline]'),{scaleX:1});return}
      g.to(q('[data-prog]'),{scaleX:1,ease:'none',scrollTrigger:{start:0,end:'max',scrub:.3}});
      const nav=q('[data-nav]')[0];
      ST.create({start:0,end:'max',onUpdate:self=>g.to(nav,{yPercent:(self.direction===1&&self.scroll()>120)?-100:0,duration:.18,ease:'power2.out',overwrite:true})});
      // hero intro
      g.from(q('[data-hl]'),{yPercent:115,duration:1.1,ease:'power4.out',stagger:.06,delay:.1});
      g.from(q('[data-hf]'),{y:18,opacity:0,duration:.8,ease:'power3.out',stagger:.09,delay:.45});
      g.from(q('[data-hphone]'),{y:90,opacity:0,duration:1.2,ease:'power3.out',delay:.3});
      g.from(q('[data-hwm]'),{opacity:0,duration:2,ease:'power1.out',delay:.6});
      const hero=q('[data-hero]')[0];
      g.to(q('[data-hword]'),{yPercent:-28,ease:'none',scrollTrigger:{trigger:hero,start:'top top',end:'bottom top',scrub:true}});
      g.to(q('[data-hpar]'),{y:-140,ease:'none',scrollTrigger:{trigger:hero,start:'top top',end:'bottom top',scrub:true}});
      g.to(q('[data-hwm]'),{yPercent:-20,xPercent:-6,ease:'none',scrollTrigger:{trigger:hero,start:'top top',end:'bottom top',scrub:true}});
      g.from(q('[data-fact]'),{y:20,opacity:0,duration:.7,ease:'power3.out',stagger:.08,scrollTrigger:{trigger:q('[data-fact]')[0],start:'top 92%'}});
      // generic reveals
      q('[data-r]').forEach(el=>g.from(el,{y:26,opacity:0,duration:.8,ease:'power3.out',scrollTrigger:{trigger:el,start:'top 88%'}}));
      // the nag, pinned
      const nag=q('[data-nag]')[0],nums=q('[data-nn]'),caps=q('[data-nc]'),ticks=q('[data-nt]'),n=nums.length;
      const tl=g.timeline({defaults:{ease:'power2.inOut'},scrollTrigger:{trigger:nag,start:'top top',end:'+=320%',pin:true,scrub:.6,anticipatePin:1}});
      tl.fromTo(q('[data-nline]'),{scaleX:0},{scaleX:1,ease:'none',duration:n+.6},0);
      for(let i=1;i<n;i++){tl.to(nums[i-1],{yPercent:-28,opacity:0,duration:.5},i).fromTo(nums[i],{yPercent:28,opacity:0},{yPercent:0,opacity:1,duration:.5},i).to(caps[i-1],{opacity:0,duration:.2},i).fromTo(caps[i],{opacity:0},{opacity:1,duration:.25},i+.25).to(ticks[i],{opacity:1,duration:.15},i+.3)}
      tl.to(nums[n-1],{yPercent:-28,opacity:0,duration:.5},n).to(caps[n-1],{opacity:0,duration:.2},n).fromTo(q('[data-ndone]'),{opacity:0,y:30},{opacity:1,y:0,duration:.5},n+.2).to(ticks[n],{opacity:1,duration:.15},n+.3).to({},{duration:.4});
      // five seconds
      g.from(q('[data-cphone]'),{y:80,opacity:0,duration:1,ease:'power3.out',scrollTrigger:{trigger:q('[data-cphone]')[0],start:'top 85%'}});
      q('[data-step]').forEach(st=>{const t2=g.timeline({scrollTrigger:{trigger:st,start:'top 80%'}});t2.from(st,{y:24,opacity:0,duration:.6,ease:'power3.out'});const chips=st.querySelectorAll('[data-chip]');if(chips.length)t2.from(chips,{opacity:0,y:8,duration:.3,stagger:.06,ease:'power2.out'},'-=.3');const sel=st.querySelector('[data-chip][data-sel]')});
      // reliability
      q('[data-perm]').forEach(row=>{const t3=g.timeline({scrollTrigger:{trigger:row,start:'top 74%',toggleActions:'play none none reverse'}});const f=row.querySelector('[data-pf]'),off=row.querySelector('[data-poff]'),on=row.querySelector('[data-pon]');t3.from(row,{opacity:.25,duration:.3});if(f)t3.to(f,{scale:1,duration:.18,ease:'power2.out'},.1).to(off,{opacity:0,duration:.12},.1).to(on,{opacity:1,duration:.12},.18)});
      const cd=q('[data-cd]')[0],o={v:10};
      g.timeline({scrollTrigger:{trigger:cd,start:'top 80%',end:'top 25%',scrub:.4}}).to(o,{v:0,ease:'none',duration:1,onUpdate:()=>{cd.textContent=String(Math.ceil(o.v))}}).to(q('[data-cdres]'),{opacity:1,duration:.15});
      // horizontal gallery
      const gal=q('[data-gal]')[0],track=q('[data-track]')[0];
      const dist=()=>Math.max(0,track.scrollWidth-gal.clientWidth);
      g.to(track,{x:()=>-dist(),ease:'none',scrollTrigger:{trigger:gal,start:'top top',end:()=>'+='+dist(),pin:true,scrub:.5,invalidateOnRefresh:true,anticipatePin:1}});
      // no list
      q('[data-no]').forEach(l=>{g.fromTo(l.children[0],{opacity:.12},{opacity:1,ease:'none',scrollTrigger:{trigger:l,start:'top 85%',end:'top 50%',scrub:true}});g.to(l.querySelector('[data-noline]'),{scaleX:1,ease:'none',scrollTrigger:{trigger:l,start:'top 85%',end:'top 45%',scrub:true}})});
      // pricing
      g.from(q('[data-plan]'),{y:50,opacity:0,duration:.8,ease:'power3.out',stagger:.1,scrollTrigger:{trigger:q('[data-plan]')[0],start:'top 85%'}});
      g.to(q('[data-pwm]'),{yPercent:30,ease:'none',scrollTrigger:{trigger:q('[data-pwm]')[0].parentNode,start:'top bottom',end:'bottom top',scrub:true}});
      g.fromTo(q('[data-bell]'),{clipPath:'inset(0% 0% 100% 0%)'},{clipPath:'inset(0% 0% 0% 0%)',ease:'none',scrollTrigger:{trigger:q('[data-bell]')[0],start:'top 90%',end:'top 40%',scrub:true}});
      // marquee with scroll velocity
      const mq=q('[data-mq]')[0];const mt=g.to(mq,{xPercent:-50,repeat:-1,duration:40,ease:'none'});
      ST.create({trigger:mq,start:'top bottom',end:'bottom top',onUpdate:self=>{const v=self.getVelocity();g.to(mt,{timeScale:(v<0?-1:1)*(1+Math.min(Math.abs(v)/250,6)),duration:.2,overwrite:true});g.to(mt,{timeScale:v<0?-1:1,duration:1.2,delay:.2,ease:'power2.out'})}});
      // footer
      g.from(q('[data-fw]'),{yPercent:110,duration:1,ease:'power4.out',stagger:.1,scrollTrigger:{trigger:q('[data-fw]')[0],start:'top 88%'}});
      g.fromTo(q('[data-fwm]'),{xPercent:8},{xPercent:-8,ease:'none',scrollTrigger:{trigger:q('[data-fwm]')[0].parentNode,start:'top bottom',end:'bottom bottom',scrub:true}});
    },root);
    if(!reduce&&window.Lenis){lenis=new window.Lenis({lerp:.1,smoothWheel:true});lenis.on('scroll',ST.update);raf=t=>lenis&&lenis.raf(t*1000);g.ticker.add(raf);g.ticker.lagSmoothing(0);
      root.querySelectorAll('a[href^="#"]').forEach(a=>a.onclick=e=>{const id=a.getAttribute('href').slice(1);const el=id&&document.getElementById(id);if(el){e.preventDefault();lenis.scrollTo(el,{offset:0,duration:1.4})}})}
    setTimeout(()=>{ST.refresh();if(window.scrollY<120)g.set(root.querySelector('[data-nav]'),{yPercent:0})},300);
  
}
drawBell(document.querySelector('[data-bell]'),INK);
if(!window.gsap||!window.ScrollTrigger)return;
(document.fonts?document.fonts.ready:Promise.resolve()).then(setup);
})();
