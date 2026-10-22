(function(){
  'use strict';
  var $=function(i){return document.getElementById(i)};
  var CURS=['USD','EUR','GBP','CAD','AUD','CHF','INR','JPY','BRL','TRY','PHP','KRW'];
  var cur='USD';
  try{var s=localStorage.getItem('sscur');if(s&&CURS.indexOf(s)>-1)cur=s}catch(e){}
  var SSL=window.SSL={
    currencies:CURS,
    get cur(){return cur},
    set cur(c){cur=c;try{localStorage.setItem('sscur',c)}catch(e){}},
    fmt:function(n){
      if(!isFinite(n))return '\u2013';
      try{return new Intl.NumberFormat('en-US',{style:'currency',currency:cur,maximumFractionDigits:0}).format(n)}catch(e){return Math.round(n).toLocaleString('en-US')}
    },
    sym:function(){
      try{return new Intl.NumberFormat('en-US',{style:'currency',currency:cur,maximumFractionDigits:0}).formatToParts(0).filter(function(p){return p.type=='currency'})[0].value}catch(e){return cur}
    },
    num:function(id){var el=$(id);return el?(parseFloat(el.value)||0):0}
  };

  /* ---- slider + number pairing (any element with data-pair) ---- */
  document.addEventListener('input',function(e){
    var t=e.target,p=t.getAttribute&&t.getAttribute('data-pair');
    if(!p)return;
    var o=$(p);if(o)o.value=t.value;
  });

  /* ---- home demo ---- */
  var hi=$('hi');
  if(hi){
    var draw=function(){
      var x=SSL.num('hin'),L=[['#10d9a0','Needs (50%)',.5],['#4f8cff','Wants (30%)',.3],['#f5c451','Savings (20%)',.2]];
      $('hl').innerHTML=L.map(function(r){return '<div class="rowline"><span><i class="dot" style="background:'+r[0]+'"></i>'+r[1]+'</span><b>'+SSL.fmt(x*r[2])+'</b></div>'}).join('');
    };
    document.addEventListener('input',function(e){if(e.target.id=='hi'||e.target.id=='hin')draw()});
    draw();
  }

  /* ---- articles page filter ---- */
  var list=$('artlist');
  if(list){
    var cards=[].slice.call(list.querySelectorAll('[data-cat]')),cat='all',q='';
    var apply=function(){
      var shown=0;
      cards.forEach(function(c){
        var ok=(cat=='all'||c.getAttribute('data-cat')==cat)&&(!q||c.textContent.toLowerCase().indexOf(q)>-1);
        c.hidden=!ok;if(ok)shown++;
      });
      $('none').hidden=shown>0;
      [].forEach.call(document.querySelectorAll('.chips button'),function(b){b.setAttribute('aria-pressed',b.getAttribute('data-cat')==cat?'true':'false')});
    };
    document.querySelector('.chips').addEventListener('click',function(e){
      var b=e.target.closest('button');if(!b)return;
      cat=b.getAttribute('data-cat');
      try{history.replaceState(null,'',cat=='all'?location.pathname:'#'+cat)}catch(x){}
      apply();
    });
    $('sq').addEventListener('input',function(){q=this.value.trim().toLowerCase();apply()});
    var h=(location.hash||'').slice(1).toLowerCase();
    if(h&&document.querySelector('.chips button[data-cat="'+h+'"]'))cat=h;
    apply();
  }

  /* ---- background: low-power currency glyphs ---- */
  var c=$('bg');
  if(c&&c.getContext){
    var rm=matchMedia('(prefers-reduced-motion:reduce)').matches,
        sd=navigator.connection&&navigator.connection.saveData,
        small=innerWidth<700;
    if(!sd){
      var x=c.getContext('2d'),S=['$','\u20AC','\u00A3','\u00A5','\u20BF','\u20B9'],C=['#10d9a0','#4f8cff','#f5c451','#a78bfa'],P=[],W,H,raf=0;
      var rs=function(){W=c.width=innerWidth;H=c.height=innerHeight};rs();addEventListener('resize',rs);
      var mk=function(init){return{x:Math.random()*W,y:init?Math.random()*H:H+30,s:S[Math.random()*S.length|0],z:14+Math.random()*24,v:.2+Math.random()*.55,d:Math.random()*6,c:C[Math.random()*C.length|0],a:Math.random()*6.28}};
      var n=rm?10:small?10:24;for(var i=0;i<n;i++)P.push(mk(1));
      var frame=function(t){
        x.clearRect(0,0,W,H);
        P.forEach(function(p,i){
          if(!rm){p.y-=p.v;p.x+=Math.sin(t/1800+p.d)*.3}
          if(p.y<-40)P[i]=mk(0);
          x.globalAlpha=.14+.16*(.5+.5*Math.sin(t/900+p.a));x.shadowColor=p.c;x.shadowBlur=small?0:14;x.fillStyle=p.c;x.font='700 '+p.z+'px sans-serif';x.fillText(p.s,p.x,p.y);
        });
        x.globalAlpha=1;
        if(!rm)raf=requestAnimationFrame(frame);
      };
      var start=function(){cancelAnimationFrame(raf);raf=requestAnimationFrame(frame)};
      document.addEventListener('visibilitychange',function(){if(document.hidden)cancelAnimationFrame(raf);else if(!rm)start()});
      start();
    }
  }
})();
