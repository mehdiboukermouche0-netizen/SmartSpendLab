(function(){
  'use strict';
  var root=document.getElementById('calc');
  if(!root||!window.SSL)return;
  var SSL=window.SSL,tool=root.getAttribute('data-tool');
  var $=function(i){return document.getElementById(i)};
  var esc=function(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})};

  function curSelect(){
    return '<label class="f" for="cur">Currency</label><select id="cur">'+SSL.currencies.map(function(c){return '<option'+(c==SSL.cur?' selected':'')+'>'+c+'</option>'}).join('')+'</select>';
  }
  function field(id,label,min,max,step,val){
    return '<label class="f" for="'+id+'n">'+label+'</label><div class="slide"><input type="range" id="'+id+'" data-pair="'+id+'n" min="'+min+'" max="'+max+'" step="'+step+'" value="'+val+'" aria-label="'+esc(label.replace(/<[^>]+>/g,''))+' slider"><input type="number" id="'+id+'n" data-pair="'+id+'" min="'+min+'" step="'+step+'" value="'+val+'" inputmode="decimal"></div>';
  }
  var cs=function(){return '<span class="cs">'+esc(SSL.sym())+'</span>'};
  function syncSym(){[].forEach.call(root.querySelectorAll('.cs'),function(e){e.textContent=SSL.sym()})}
  function wire(render){
    root.addEventListener('input',function(e){
      var t=e.target,p=t.getAttribute('data-pair');
      if(p){var o=$(p);if(o)o.value=t.value}
      if(t.id=='cur')return;
      render();
    });
    root.addEventListener('change',function(e){
      if(e.target.id=='cur'){SSL.cur=e.target.value;syncSym();render()}
    });
    render();
  }
  var yrs=function(n){return Math.floor(n/12)+' yrs '+(n%12)+' mo'};

  /* ---------- 50/30/20 ---------- */
  function budget(){
    var P={std:[50,30,20],high:[60,20,20],save:[40,30,30]};
    root.innerHTML='<div class="calc"><div>'+curSelect()+field('b1','Monthly take-home pay ('+cs()+')',500,20000,100,3500)+
      '<label class="f" for="bp">Split (needs / wants / savings)</label><select id="bp"><option value="std">50 / 30 / 20 \u2013 standard</option><option value="high">60 / 20 / 20 \u2013 higher living costs</option><option value="save">40 / 30 / 30 \u2013 save faster</option></select></div>'+
      '<div class="out" aria-live="polite"><div id="bsplit"></div><div id="brows" class="rows"></div></div></div>';
    wire(function(){
      var x=SSL.num('b1n'),s=P[$('bp').value],L=[['#10d9a0','Needs'],['#4f8cff','Wants'],['#f5c451','Savings and debt']];
      $('bsplit').innerHTML='<div class="muted small">Each month you can plan for</div><div class="split" role="img" aria-label="Split bar: needs '+s[0]+'%, wants '+s[1]+'%, savings '+s[2]+'%">'+L.map(function(l,i){return '<i style="width:'+s[i]+'%;background:'+l[0]+'"></i>'}).join('')+'</div>';
      $('brows').innerHTML=L.map(function(l,i){return '<div class="rowline"><span><i class="dot" style="background:'+l[0]+'"></i>'+l[1]+' ('+s[i]+'%)</span><b>'+SSL.fmt(x*s[i]/100)+'</b></div>'}).join('')+
        '<div class="rowline"><span>Savings and debt per year</span><b style="color:var(--em)">'+SSL.fmt(x*s[2]/100*12)+'</b></div>';
    });
  }

  /* ---------- compound interest ---------- */
  function compound(){
    root.innerHTML='<div class="calc"><div>'+curSelect()+field('c1','Initial deposit ('+cs()+')',0,100000,500,2000)+field('c2','Monthly contribution ('+cs()+')',0,5000,25,250)+field('c3','Annual interest rate (%)',0,15,.5,6)+field('c4','Years',1,40,1,20)+'</div>'+
      '<div class="out" aria-live="polite"><div class="rowline"><span>Total contributed</span><b id="co"></b></div><div class="rowline"><span>Interest earned</span><b id="ci" style="color:var(--gold)"></b></div><div class="muted small" style="margin-top:14px">Estimated final balance</div><div class="big" id="cb"></div><div id="cc"></div></div></div>'+
      '<details class="tbl"><summary>Year-by-year table</summary><div class="ov"><table><thead><tr><th>Year</th><th>Contributed</th><th>Interest</th><th>Balance</th></tr></thead><tbody id="ct"></tbody></table></div></details>';
    wire(function(){
      var p=SSL.num('c1n'),m=SSL.num('c2n'),r=SSL.num('c3n')/1200,y=Math.max(1,Math.min(80,Math.round(SSL.num('c4n')))),b=p,ser=[],i;
      for(i=1;i<=y*12;i++){b=b*(1+r)+m;if(i%12==0)ser.push([p+m*i,b])}
      var tot=p+m*y*12;
      $('co').textContent=SSL.fmt(tot);$('ci').textContent=SSL.fmt(b-tot);$('cb').textContent=SSL.fmt(b);
      var mx=Math.max.apply(null,ser.map(function(q){return q[1]}))||1,bw=560/ser.length,s='';
      ser.forEach(function(q,k){var h1=q[0]/mx*190,h2=Math.max(0,q[1]-q[0])/mx*190,x=20+k*bw;
        s+='<rect x="'+(x+1).toFixed(1)+'" y="'+(210-h1).toFixed(1)+'" width="'+Math.max(1,bw-2).toFixed(1)+'" height="'+h1.toFixed(1)+'" fill="#4f8cff" rx="1.5"/><rect x="'+(x+1).toFixed(1)+'" y="'+(210-h1-h2).toFixed(1)+'" width="'+Math.max(1,bw-2).toFixed(1)+'" height="'+h2.toFixed(1)+'" fill="#10d9a0" rx="1.5"/>'});
      $('cc').innerHTML='<svg class="chart" viewBox="0 0 600 240" role="img" aria-label="Stacked bars of contributions and interest over '+y+' years, ending at '+SSL.fmt(b)+'"><line x1="20" y1="210" x2="580" y2="210" stroke="#25314a"/>'+s+
        '<text x="20" y="232" fill="#9aa8c2" font-size="11">Year 1</text><text x="580" y="232" fill="#9aa8c2" font-size="11" text-anchor="end">Year '+y+'</text><circle cx="30" cy="10" r="4" fill="#4f8cff"/><text x="40" y="14" fill="#9aa8c2" font-size="11">Contributions</text><circle cx="130" cy="10" r="4" fill="#10d9a0"/><text x="140" y="14" fill="#9aa8c2" font-size="11">Interest</text></svg>';
      $('ct').innerHTML=ser.map(function(q,k){return '<tr><td>'+(k+1)+'</td><td>'+SSL.fmt(q[0])+'</td><td>'+SSL.fmt(q[1]-q[0])+'</td><td>'+SSL.fmt(q[1])+'</td></tr>'}).join('');
    });
  }

  /* ---------- debt payoff ---------- */
  function sim(D,extra,mode,roll){
    var bal=D.map(function(d){return d.b}),tm=D.reduce(function(a,d){return a+d.m},0),
        tot=function(){return bal.reduce(function(a,b){return a+b},0)},
        int=0,n=0,done=D.map(function(d){return d.b>0?0:-1}),i,
        ord=D.map(function(d,i){return i}).sort(function(a,b){return mode=='av'?D[b].r-D[a].r:D[a].b-D[b].b});
    while(tot()>.5&&n<1200){
      n++;var paid=0;
      for(i=0;i<D.length;i++)if(bal[i]>0){var it=bal[i]*D[i].r/1200;int+=it;bal[i]+=it;var p=Math.min(D[i].m,bal[i]);bal[i]-=p;paid+=p}
      if(roll){var rem=tm+extra-paid;ord.forEach(function(k){if(rem>0&&bal[k]>0){var p=Math.min(rem,bal[k]);bal[k]-=p;rem-=p}})}
      for(i=0;i<D.length;i++)if(bal[i]<=.5&&bal[i]>-1&&done[i]===0){done[i]=n;bal[i]=0}
    }
    return{n:n,int:int,ok:tot()<=.5,done:done,ord:ord};
  }
  function debt(){
    var d=[['Credit card',4500,22,120],['Car loan',9000,7,260],['Student loan',14000,5,180],['',0,0,0],['',0,0,0]],r='';
    d.forEach(function(x,i){r+='<div class="drow"><input id="dn'+i+'" type="text" value="'+esc(x[0])+'" placeholder="Debt '+(i+1)+'" aria-label="Debt '+(i+1)+' name"><input id="db'+i+'" type="number" min="0" value="'+x[1]+'" aria-label="Debt '+(i+1)+' balance"><input id="dr'+i+'" type="number" min="0" step=".5" value="'+x[2]+'" aria-label="Debt '+(i+1)+' APR percent"><input id="dm'+i+'" type="number" min="0" value="'+x[3]+'" aria-label="Debt '+(i+1)+' minimum payment"></div>'});
    root.innerHTML='<div class="calc"><div>'+curSelect()+'<div class="debts"><div class="drow dhead"><span>Debt</span><span>Balance</span><span>APR %</span><span>Minimum</span></div>'+r+'</div>'+field('de','Extra monthly payment ('+cs()+')',0,2000,25,300)+
      '<div class="seg" role="group" aria-label="Payoff method"><button type="button" id="m1" aria-pressed="true">Avalanche (highest rate first)</button><button type="button" id="m2" aria-pressed="false">Snowball (smallest balance first)</button></div></div>'+
      '<div class="out" aria-live="polite"><div class="rowline"><span>Debt-free in</span><b id="dt"></b></div><div class="rowline"><span>Total interest</span><b id="di"></b></div><div class="rowline"><span>Interest saved vs minimums only</span><b id="ds" style="color:var(--em)"></b></div><p id="dw" class="warn small" hidden></p><div id="dc"></div><div class="ov"><table><thead><tr><th>Payoff order</th><th>Cleared in</th></tr></thead><tbody id="dl"></tbody></table></div></div></div>';
    var mode='av';
    var render=function(){
      var D=[],names=[];
      for(var i=0;i<5;i++){D.push({b:Math.max(0,SSL.num('db'+i)),r:Math.max(0,SSL.num('dr'+i)),m:Math.max(0,SSL.num('dm'+i))});names.push($('dn'+i).value.trim()||'Debt '+(i+1))}
      var extra=Math.max(0,SSL.num('den')),a=sim(D,extra,mode,true),b=sim(D,0,mode,false),w=$('dw');
      if(!D.some(function(x){return x.b>0})){$('dt').textContent='\u2013';$('di').textContent='\u2013';$('ds').textContent='\u2013';$('dc').innerHTML='';$('dl').innerHTML='';w.hidden=false;w.textContent='Enter at least one debt balance to see a plan.';return}
      w.hidden=true;
      $('dt').textContent=a.ok?yrs(a.n):'Not within 100 years';
      $('di').textContent=SSL.fmt(a.int);
      if(!a.ok){w.hidden=false;w.textContent='Your payments do not cover the monthly interest. Increase the extra payment or the minimums.'}
      $('ds').textContent=(a.ok&&b.ok)?SSL.fmt(Math.max(0,b.int-a.int)):(a.ok?'Minimums alone never clear it':'\u2013');
      var base=b.ok?b.n:a.n,N=Math.max(a.n,base,1),tot0=D.reduce(function(s,x){return s+x.b},0)||1;
      var curve=function(rr,c){
        var bal=D.map(function(x){return x.b}),pts=[tot0],n=0,i,tm=D.reduce(function(s,x){return s+x.m},0),
            ord=D.map(function(x,i){return i}).sort(function(p,q){return mode=='av'?D[q].r-D[p].r:D[p].b-D[q].b});
        while(n<N&&pts[n]>.5){n++;var paid=0;
          for(i=0;i<D.length;i++)if(bal[i]>0){var it=bal[i]*D[i].r/1200;bal[i]+=it;var p=Math.min(D[i].m,bal[i]);bal[i]-=p;paid+=p}
          if(rr){var rem=tm+extra-paid;ord.forEach(function(k){if(rem>0&&bal[k]>0){var p=Math.min(rem,bal[k]);bal[k]-=p;rem-=p}})}
          pts.push(bal.reduce(function(s,x){return s+x},0))}
        return '<polyline fill="none" stroke="'+c+'" stroke-width="2.5" points="'+pts.map(function(y,i){return(20+i/N*560).toFixed(1)+','+(200-Math.min(1.2,y/tot0)*180).toFixed(1)}).join(' ')+'"/>'};
      $('dc').innerHTML='<svg class="chart" viewBox="0 0 600 240" role="img" aria-label="Remaining debt over time: your plan versus minimum payments only"><line x1="20" y1="200" x2="580" y2="200" stroke="#25314a"/>'+curve(false,'#9aa8c2')+curve(true,'#10d9a0')+'<text x="20" y="226" fill="#9aa8c2" font-size="11">Now</text><text x="580" y="226" fill="#9aa8c2" font-size="11" text-anchor="end">'+N+' months</text><text x="20" y="14" fill="#10d9a0" font-size="11">\u25CF Your plan</text><text x="120" y="14" fill="#9aa8c2" font-size="11">\u25CF Minimums only</text></svg>';
      $('dl').innerHTML=a.ord.filter(function(k){return D[k].b>0}).sort(function(p,q){return (a.done[p]||9999)-(a.done[q]||9999)}).map(function(k){return '<tr><td>'+esc(names[k])+'</td><td>'+(a.done[k]>0?yrs(a.done[k]):'\u2013')+'</td></tr>'}).join('');
    };
    root.addEventListener('click',function(e){
      var t=e.target.closest('button');if(!t||(t.id!='m1'&&t.id!='m2'))return;
      mode=t.id=='m1'?'av':'sn';$('m1').setAttribute('aria-pressed',mode=='av');$('m2').setAttribute('aria-pressed',mode=='sn');render();
    });
    wire(render);
  }

  ({'50-30-20-budget-calculator':budget,'compound-interest-calculator':compound,'debt-payoff-calculator':debt})[tool]();
})();
