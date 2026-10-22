var LG=['en','es','fr','de','ar','pt','zh','ja','hi'],LN={en:'English',es:'Español',fr:'Français',de:'Deutsch',ar:'العربية',pt:'Português',zh:'中文',ja:'日本語',hi:'हिन्दी'},D={},lang='en';
[['Home','Inicio','Accueil','Start','الرئيسية','Início','首页','ホーム','होम'],
['Calculators','Calculadoras','Calculateurs','Rechner','الحاسبات','Calculadoras','计算器','計算ツール','कैलकुलेटर'],
['Articles','Artículos','Articles','Artikel','المقالات','Artigos','文章','記事','लेख'],
['About','Acerca de','À propos','Über uns','من نحن','Sobre','关于我们','私たちについて','हमारे बारे में'],
['Use Calculators','Usar calculadoras','Utiliser les calculateurs','Rechner nutzen','استخدم الحاسبات','Usar calculadoras','使用计算器','計算ツールを使う','कैलकुलेटर इस्तेमाल करें'],
['Master Your Money with','Domina tu dinero con','Maîtrisez votre argent avec','Meistere dein Geld mit','أتقن إدارة أموالك مع','Domine seu dinheiro com','掌控你的财务，借助','お金を使いこなす、','अपने पैसे पर नियंत्रण पाएं,'],
['Free Interactive Tools','Herramientas interactivas gratuitas','Outils interactifs gratuits','kostenlose interaktive Tools','أدوات تفاعلية مجانية','ferramentas interativas gratuitas','免费互动工具','無料のインタラクティブツール','मुफ़्त इंटरैक्टिव टूल्स'],
['Budget smarter, grow your savings and crush debt with simple calculators and plain-English guides. No sign-up, no jargon.','Presupuesta mejor, aumenta tus ahorros y elimina deudas con calculadoras sencillas y guías claras. Sin registro, sin jerga.','Budgétisez mieux, épargnez plus et réduisez vos dettes grâce à des calculateurs simples et des guides clairs. Sans inscription, sans jargon.','Plane klüger, spare mehr und werde Schulden los – mit einfachen Rechnern und verständlichen Ratgebern. Ohne Anmeldung, ohne Fachchinesisch.','خطّط لميزانيتك بذكاء، ونمِّ مدخراتك، وتخلّص من الديون بحاسبات بسيطة وأدلة واضحة. بلا تسجيل وبلا مصطلحات معقدة.','Faça um orçamento melhor, aumente suas economias e quite dívidas com calculadoras simples e guias claros. Sem cadastro, sem jargão.','用简单的计算器和通俗易懂的指南，更聪明地做预算、增加储蓄、还清债务。无需注册，没有术语。','シンプルな計算ツールと分かりやすいガイドで、予算管理、貯蓄、借金返済をもっとスマートに。登録不要、専門用語なし。','सरल कैलकुलेटर और आसान गाइड से बेहतर बजट बनाएं, बचत बढ़ाएं और कर्ज़ चुकाएं। न साइन-अप, न मुश्किल शब्द।'],
['Read Guides','Leer guías','Lire les guides','Ratgeber lesen','اقرأ الأدلة','Ler guias','阅读指南','ガイドを読む','गाइड पढ़ें'],
['Plan Debt Payoff','Planear pago de deudas','Planifier le remboursement','Schuldenabbau planen','خطّط لسداد الديون','Planejar quitação','规划还债','返済を計画','कर्ज़ चुकाने की योजना'],
['Live tools showcase','Herramientas en vivo','Outils en direct','Tools live ausprobieren','جرّب الأدوات مباشرة','Ferramentas ao vivo','在线工具展示','ライブツール','लाइव टूल्स'],
['Browse by topic','Explorar por tema','Parcourir par thème','Nach Thema stöbern','تصفّح حسب الموضوع','Explorar por tema','按主题浏览','トピック別に見る','विषय के अनुसार देखें'],
['Latest articles','Últimos artículos','Derniers articles','Neueste Artikel','أحدث المقالات','Últimos artigos','最新文章','最新記事','नवीनतम लेख'],
['Get Free Weekly Financial Tips','Recibe consejos financieros semanales gratis','Recevez des conseils financiers hebdomadaires gratuits','Kostenlose wöchentliche Finanztipps erhalten','احصل على نصائح مالية أسبوعية مجانية','Receba dicas financeiras semanais grátis','免费获取每周理财小贴士','毎週の無料マネーのヒントを受け取る','हर हफ़्ते मुफ़्त वित्तीय सुझाव पाएं'],
['Subscribe free','Suscribirme gratis','S’abonner gratuitement','Kostenlos abonnieren','اشترك مجاناً','Inscrever-se grátis','免费订阅','無料で登録','मुफ़्त सब्सक्राइब करें'],
['Privacy Policy','Política de privacidad','Politique de confidentialité','Datenschutz','سياسة الخصوصية','Política de privacidade','隐私政策','プライバシーポリシー','गोपनीयता नीति'],
['Financial Disclaimer','Aviso financiero','Avertissement financier','Finanzieller Haftungsausschluss','إخلاء المسؤولية المالية','Aviso financeiro','财务免责声明','金融に関する免責事項','वित्तीय अस्वीकरण'],
['Contact','Contacto','Contact','Kontakt','اتصل بنا','Contato','联系我们','お問い合わせ','संपर्क'],
['Terms of Service','Términos del servicio','Conditions d’utilisation','Nutzungsbedingungen','شروط الخدمة','Termos de serviço','服务条款','利用規約','सेवा की शर्तें'],
['Affiliate Disclosure','Divulgación de afiliados','Mention d’affiliation','Affiliate-Hinweis','الإفصاح عن الروابط التابعة','Divulgação de afiliados','联盟披露','アフィリエイト開示','एफ़िलिएट प्रकटीकरण'],
['Educational content only, not professional financial advice.','Solo contenido educativo, no asesoramiento financiero profesional.','Contenu éducatif uniquement, pas un conseil financier professionnel.','Nur Bildungsinhalte, keine professionelle Finanzberatung.','محتوى تعليمي فقط وليس استشارة مالية احترافية.','Apenas conteúdo educativo, não é aconselhamento financeiro profissional.','仅供教育参考，不构成专业财务建议。','教育目的のコンテンツであり、専門的な金融アドバイスではありません。','केवल शैक्षिक सामग्री, पेशेवर वित्तीय सलाह नहीं।'],
['Search articles…','Buscar artículos…','Rechercher des articles…','Artikel suchen…','ابحث في المقالات…','Pesquisar artigos…','搜索文章…','記事を検索…','लेख खोजें…']
].forEach(function(r){D[r[0]]=r});
/* extra strings for the multi-page site (Tools) */
D['Tools']=['Tools','Herramientas','Outils','Tools','أدوات','Ferramentas','工具','ツール','टूल्स'];
(function(){
  try{lang=localStorage.getItem('sslang')||'en'}catch(e){}
  if(LG.indexOf(lang)<0)lang='en';
  var sel=document.getElementById('lg');
  if(sel){sel.innerHTML=LG.map(function(c){return '<option value="'+c+'"'+(c==lang?' selected':'')+'>'+LN[c]+'</option>'}).join('')}
  function tr(){
    var i=LG.indexOf(lang),w=document.createTreeWalker(document.body,4),n,k,r;
    document.documentElement.dir=lang=='ar'?'rtl':'ltr';
    if(lang=='en'&&!window.__trUsed)return;
    window.__trUsed=true;
    while(n=w.nextNode()){
      var p=n.parentNode.tagName;if(p=='SCRIPT'||p=='STYLE'||p=='TEXTAREA'||p=='NOSCRIPT')continue;
      if(n._o===undefined)n._o=n.nodeValue;
      k=n._o.trim();r=D[k];
      if(r)n.nodeValue=n._o.replace(k,function(){return r[i]});
    }
    var s=document.getElementById('sq');if(s&&D['Search articles…'])s.placeholder=D['Search articles…'][i];
    document.documentElement.lang=lang;
  }
  if(sel)sel.addEventListener('change',function(){lang=this.value;try{localStorage.setItem('sslang',lang)}catch(e){}tr()});
  tr();
})();
