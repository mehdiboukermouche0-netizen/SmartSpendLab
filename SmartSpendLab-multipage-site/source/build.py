#!/usr/bin/env python3
"""SmartSpendLab static site generator.
Edit the CONFIG block, run `python3 build.py`, upload the /site folder to your host."""
import json, os, re, shutil, html, math
from content1 import EXTRA as EX1, NEW as NEW1, META as META1
from content2 import NEW as NEW2, META as META2
from tools_content import TOOLS

# ---------------- CONFIG ----------------
SITE = 'https://smartspendlab.com'      # your final domain, no trailing slash
NAME = 'SmartSpendLab'
EMAIL = 'hello@smartspendlab.com'
DATE = '2026-10-22'                     # publish / last-updated date
ADSENSE_CLIENT = ''                     # e.g. 'ca-pub-1234567890123456' (leave empty until approved)
AD_SLOT_ARTICLE = ''                    # optional ad unit ids from AdSense
AD_SLOT_TOOL = ''
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'site')
SRC = os.path.dirname(os.path.abspath(__file__))
# ----------------------------------------

e = html.escape
ICONS = {
 'pie': '<circle cx="12" cy="12" r="9"/><path d="M12 3v9h9"/>',
 'trend': '<path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/>',
 'mountain': '<path d="M3 20l6-10 4 6 3-4 5 8z"/>',
 'coin': '<circle cx="12" cy="12" r="9"/><path d="M12 7v10M9.5 9.8c0-1 1-1.6 2.5-1.6s2.5.7 2.5 1.7c0 2.3-5 1.2-5 3.6 0 1 1.1 1.7 2.5 1.7s2.5-.6 2.5-1.5"/>',
 'bolt': '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
 'shield': '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
 'target': '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>',
 'check': '<path d="M5 12.5l4.5 4.5L19 7"/>',
}
def icon(k): return f'<svg viewBox="0 0 24 24" aria-hidden="true">{ICONS[k]}</svg>'
CAT_ICON = {'Budgeting': 'pie', 'Saving': 'coin', 'Debt': 'mountain', 'Income': 'bolt', 'Investing': 'trend'}
CAT_DESC = {
 'Budgeting': 'Methods for planning where your money goes.',
 'Saving': 'Emergency funds, savings accounts and spending less.',
 'Debt': 'Strategies for paying down what you owe.',
 'Income': 'Ways to earn more around your main job.',
 'Investing': 'Compounding and habits for long-term growth.',
}
CATS = ['Budgeting', 'Saving', 'Debt', 'Income', 'Investing']

# ---------------- data ----------------
ARTS = json.load(open(os.path.join(SRC, 'articles.json'), encoding='utf8'))
META = {**META1, **META2}
TOOLMAP = {t['id']: t for t in TOOLS}
def wc(h): return len(re.sub(r'<[^>]+>', ' ', h).split())
def fixlinks(h):
    def r(m):
        k = m.group(1)
        if k in TOOLMAP: return f'href="/tools/{k}/"'
        if any(a['id'] == k for a in ARTS): return f'href="/articles/{k}/"'
        if k == 'calculators': return 'href="/tools/"'
        if k == 'articles': return 'href="/articles/"'
        return m.group(0)
    return re.sub(r'href="#([a-z0-9-]+)"', r, h)
for a in ARTS:
    if a['id'] in NEW1: a['body'] = NEW1[a['id']]
    elif a['id'] in NEW2: a['body'] = NEW2[a['id']]
    if a['id'] in EX1: a['body'] = a['body'] + '\n' + EX1[a['id']]
    a['body'] = fixlinks(a['body'])
    a['words'] = wc(a['body'])
    a['min'] = max(3, round(a['words'] / 200))
    a['meta'] = META[a['id']]
ART = {a['id']: a for a in ARTS}
TOOL_FOR = {'Budgeting': ['50-30-20-budget-calculator'], 'Saving': ['50-30-20-budget-calculator', 'compound-interest-calculator'],
            'Debt': ['debt-payoff-calculator'], 'Income': ['50-30-20-budget-calculator', 'compound-interest-calculator'],
            'Investing': ['compound-interest-calculator', '50-30-20-budget-calculator']}
TOOL_FOR_ID = {'how-to-negotiate-your-bills': ['debt-payoff-calculator', '50-30-20-budget-calculator'],
               'beginner-guide-to-emergency-funds': ['50-30-20-budget-calculator', 'debt-payoff-calculator']}

# ---------------- html helpers ----------------
def ttl(t): return t if len(t) > 44 else f'{t} | {NAME}'
def date_h(d=DATE): return 'October 22, 2026'

LOGO = ('<svg viewBox="0 0 100 100" aria-hidden="true"><defs><linearGradient id="lgG" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#10d9a0"/><stop offset="1" stop-color="#4f8cff"/></linearGradient></defs>'
        '<circle cx="50" cy="50" r="46" fill="#0B0F19" stroke="url(#lgG)" stroke-width="3"/><circle cx="50" cy="50" r="33" fill="none" stroke="#25314a" stroke-width="1.5" stroke-dasharray="3 4"/>'
        '<g class="orbit" font-size="12" font-weight="800" text-anchor="middle" fill="#f5c451"><text x="50" y="14">$</text><text x="84" y="40">€</text><text x="72" y="86">£</text><text x="28" y="86">¥</text><text x="16" y="40">₿</text></g>'
        '<text x="50" y="62" font-size="34" font-weight="800" text-anchor="middle" fill="url(#lgG)">$</text></svg>')
STATIC_LOGO = LOGO.replace('class="orbit" ', '').replace('lgG', 'lgS')

def head(title, desc, path, jsonld=(), otype='website', noindex=False):
    url = SITE + path
    ld = ''.join(f'<script type="application/ld+json">{json.dumps(j, ensure_ascii=False, separators=(",", ":"))}</script>' for j in jsonld)
    ads = f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT}" crossorigin="anonymous"></script>' if ADSENSE_CLIENT else ''
    robots = 'noindex,follow' if noindex else 'index,follow,max-image-preview:large,max-snippet:-1'
    return f'''<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#0B0F19">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta property="og:site_name" content="{NAME}">
<meta property="og:type" content="{otype}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/og-image.png">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{SITE}/assets/og-image.png">
<link rel="stylesheet" href="/assets/style.css">
{ld}{ads}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<canvas id="bg" aria-hidden="true"></canvas><div class="glow" aria-hidden="true"></div>
'''

def header(cur):
    def a(href, label, key):
        c = ' aria-current="page"' if key == cur else ''
        return f'<a href="{href}"{c}>{label}</a>'
    return f'''<header class="site"><div class="wrap"><div class="bar">
<a class="brand" href="/" aria-label="{NAME} home">{LOGO}<span>SmartSpend<b>Lab</b></span></a>
<nav class="main" aria-label="Main">{a('/', 'Home', 'home')}{a('/tools/', 'Tools', 'tools')}{a('/articles/', 'Articles', 'articles')}{a('/about/', 'About', 'about')}</nav>
<select id="lg" aria-label="Language"><option>English</option></select>
<a class="btn sm" href="/tools/">Use Calculators</a>
</div></div></header>
<main id="main">
'''

def footer(scripts=''):
    top = ''.join(f'<li><a href="/articles/{a["id"]}/">{e(a["t"])}</a></li>' for a in ARTS[:4])
    tl = ''.join(f'<li><a href="/tools/{t["id"]}/">{e(t["name"])}</a></li>' for t in TOOLS)
    return f'''</main>
<footer class="site"><div class="wrap">
<div class="fgrid">
<div><div class="brand" style="margin-bottom:12px">{STATIC_LOGO}<span>SmartSpend<b>Lab</b></span></div><p>Free calculators and plain-English guides that help you budget, save and pay down debt. Your numbers never leave your device.</p></div>
<div><h3>Tools</h3><ul>{tl}</ul></div>
<div><h3>Guides</h3><ul>{top}<li><a href="/articles/">All articles</a></li></ul></div>
<div><h3>Company</h3><ul><li><a href="/about/">About</a></li><li><a href="/contact/">Contact</a></li><li><a href="/privacy-policy/">Privacy Policy</a></li><li><a href="/terms/">Terms of Service</a></li><li><a href="/disclaimer/">Financial Disclaimer</a></li><li><a href="/disclaimer/#affiliate">Affiliate Disclosure</a></li></ul></div>
</div>
<div class="legal"><p><b>Educational content only, not professional financial advice.</b> Calculators give estimates based on the numbers you enter. Some links may earn us a commission at no cost to you.</p>
<p>© 2026 {NAME}</p></div>
</div></footer>
<script src="/assets/site.js" defer></script>
{scripts}<script src="/assets/i18n.js" defer></script>
</body>
</html>
'''

def crumbs(items):
    out = []
    for i, (n, u) in enumerate(items):
        out.append(f'<a href="{u}">{e(n)}</a>' if u else f'<span aria-current="page">{e(n)}</span>')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + ' / '.join(out) + '</nav>'

def crumb_ld(items):
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': SITE + (u or '')} for i, (n, u) in enumerate(items)]}

def ad(slot):
    if not (ADSENSE_CLIENT and slot): return ''
    return f'<div class="ad-slot"><ins class="adsbygoogle" style="display:block" data-ad-client="{ADSENSE_CLIENT}" data-ad-slot="{slot}" data-ad-format="auto" data-full-width-responsive="true"></ins><script>(adsbygoogle=window.adsbygoogle||[]).push({{}});</script></div>'

def tool_card(t):
    return f'<a class="card" href="/tools/{t["id"]}/"><span class="ico">{icon(t["icon"])}</span><h3>{e(t["name"])}</h3><p>{e(t["short"])}</p><span class="more">Open calculator</span></a>'

def art_card(a, data=False):
    d = f' data-cat="{a["c"].lower()}"' if data else ''
    return (f'<a class="card" href="/articles/{a["id"]}/"{d}><span class="ico">{icon(CAT_ICON[a["c"]])}</span>'
            f'<div class="meta" style="margin-top:14px"><span class="tag">{a["c"]}</span><span>{a["min"]} min read</span></div>'
            f'<h3 style="margin-top:6px">{e(a["t"])}</h3><p>{e(a["d"])}</p></a>')

def write(path, content):
    fp = os.path.join(OUT, path.strip('/'), 'index.html') if not path.endswith('.html') else os.path.join(OUT, path.strip('/'))
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, 'w', encoding='utf8').write(content)

URLS = []
def reg(path): URLS.append(path)

# ---------------- reset output ----------------
if os.path.exists(OUT): shutil.rmtree(OUT)
os.makedirs(os.path.join(OUT, 'assets'))
for f in ['style.css', 'site.js', 'calc.js', 'i18n.js']:
    shutil.copy(os.path.join(SRC, 'assets', f), os.path.join(OUT, 'assets', f))
open(os.path.join(OUT, 'favicon.svg'), 'w', encoding='utf8').write(STATIC_LOGO.replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" '))
shutil.copy(os.path.join(OUT, 'favicon.svg'), os.path.join(OUT, 'assets', 'logo.svg'))

ORG = {'@type': 'Organization', 'name': NAME, 'url': SITE + '/', 'logo': SITE + '/assets/logo.svg', 'email': EMAIL}

# ---------------- home ----------------
def home():
    tools = ''.join(tool_card(t) for t in TOOLS)
    latest = ''.join(art_card(a) for a in ARTS[:6])
    topics = ''.join(f'<a class="card" href="/articles/#{c.lower()}"><span class="ico">{icon(CAT_ICON[c])}</span><h3>{c}</h3><p>{CAT_DESC[c]} {sum(1 for a in ARTS if a["c"] == c)} guides.</p></a>' for c in CATS)
    ld = [{'@context': 'https://schema.org', '@graph': [ORG, {'@type': 'WebSite', 'name': NAME, 'url': SITE + '/', 'description': 'Free budget, compound interest and debt payoff calculators plus plain-English money guides.', 'publisher': {'@type': 'Organization', 'name': NAME}}]}]
    h = head('SmartSpendLab – Free Budget, Savings & Debt Calculators', 'Free budget, compound interest and debt payoff calculators plus plain-English money guides. No sign-up, and your numbers never leave your device.', '/', ld)
    h += header('home')
    h += f'''<div class="wrap"><section class="hero"><div class="hero-grid">
<div>
<h1><span>Master Your Money with</span> <span>Free Interactive Tools</span></h1>
<p class="lead">Budget smarter, grow your savings and crush debt with simple calculators and plain-English guides. No sign-up, no jargon.</p>
<div class="cta"><a class="btn" href="/tools/">Use Calculators</a><a class="btn ghost" href="/articles/">Read Guides</a><a class="btn ghost" href="/tools/debt-payoff-calculator/">Plan Debt Payoff</a></div>
<ul class="facts"><li>{icon('check')}Free to use</li><li>{icon('check')}Runs in your browser</li><li>{icon('check')}No account needed</li><li>{icon('check')}Written in plain English</li></ul>
</div>
<div class="panel demo"><h2>Where should your pay go?</h2><p class="muted small" style="margin:0">Drag the slider to see a 50/30/20 split.</p>
<label class="f" for="hin">Monthly take-home pay</label>
<div class="slide"><input type="range" id="hi" data-pair="hin" min="500" max="15000" step="100" value="3500" aria-label="Monthly take-home pay slider"><input type="number" id="hin" data-pair="hi" min="0" step="100" value="3500" inputmode="decimal"></div>
<div id="hl" class="rows"></div>
<p style="margin:16px 0 0"><a class="btn sm" href="/tools/50-30-20-budget-calculator/">Open the full budget calculator</a></p></div>
</div></section></div>
<div class="wrap"><section class="block"><div class="head"><div><h2>Calculators you can use right now</h2><p>Each tool has its own page with a step-by-step explanation, a worked example and answers to common questions.</p></div><a class="btn ghost sm" href="/tools/">See all tools</a></div>
<div class="grid g3">{tools}</div></section></div>
<div class="wrap"><section class="block" style="padding-top:8px"><div class="head"><h2>Why people use SmartSpendLab</h2></div>
<div class="cols">
<div><h3>Private by design</h3><p>Every calculation runs inside your browser. The balances, incomes and debts you type in are never sent to our servers or stored by us.</p></div>
<div><h3>Explained, not just calculated</h3><p>A number alone does not change habits. Each tool comes with the reasoning, the formula and a worked example, so you know why the result looks the way it does.</p></div>
<div><h3>Honest about limits</h3><p>Calculators give estimates, not promises. We say clearly what each one leaves out, and we never present education as personal financial advice.</p></div>
</div></section></div>
<div class="wrap"><section class="block"><div class="head"><div><h2>Latest articles</h2><p>Practical guides for people who want a clear next step with their money.</p></div><a class="btn ghost sm" href="/articles/">All articles</a></div>
<div class="grid g3">{latest}</div></section></div>
<div class="wrap"><section class="block"><div class="head"><h2>Browse by topic</h2></div><div class="grid g3">{topics}</div></section></div>
<div class="wrap"><section class="block"><div class="panel" style="display:grid;gap:12px;max-width:820px"><h2 style="margin-bottom:0">Independent, educational and free</h2>
<p class="muted" style="margin:0">SmartSpendLab is an independent education project. We write about everyday money decisions, such as budgeting, saving, debt and compounding, and build calculators to test the numbers yourself. We are not financial advisers and nothing on the site is personal advice. The site is supported by advertising, and we explain how in our <a href="/about/">About page</a> and <a href="/disclaimer/">disclaimer</a>.</p></div></section></div>
'''
    h += footer()
    write('/', h); reg('/')
home()

# ---------------- tools ----------------
def tools_index():
    path = '/tools/'
    ld = [crumb_ld([('Home', '/'), ('Tools', None)]), {'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': 'Free money calculators', 'url': SITE + path}]
    h = head(ttl('Free Money Calculators and Planning Tools'), 'Free budget, compound interest and debt payoff calculators. Each tool has its own page with instructions, a worked example and FAQs.', path, ld)
    h += header('tools')
    h += f'''<div class="wrap"><div class="ph">{crumbs([('Home', '/'), ('Tools', None)])}<h1>Free money calculators</h1>
<p class="lead">Three focused tools for the decisions that matter most: how to split your income, how savings grow and how fast you can clear debt. Everything runs in your browser.</p></div>
<div class="grid g3">{''.join(tool_card(t) for t in TOOLS)}</div>
<section class="block"><div class="prose"><h2>How our calculators work</h2>
<p>We build tools to answer one question each, and we keep the inputs simple. You choose a currency, enter your numbers and see the result update instantly. Nothing is submitted to a server, so your personal figures stay on your device. Only your language and currency choices are remembered in your browser to save you from picking them again.</p>
<p>Calculators are estimates. They rely on the assumptions you enter, such as a steady interest rate, and they leave out things like taxes, fees and inflation. Each tool page explains what is included and what is not. For the reasoning behind the numbers, pair a calculator with the matching guide on our <a href="/articles/">articles page</a>.</p>
<h2>Which tool should I start with?</h2>
<ul><li>If you are not sure where your money goes, start with the <a href="/tools/50-30-20-budget-calculator/">50/30/20 budget calculator</a>.</li><li>If you want to see what regular saving can become, try the <a href="/tools/compound-interest-calculator/">compound interest calculator</a>.</li><li>If you owe money on cards or loans, use the <a href="/tools/debt-payoff-calculator/">debt payoff planner</a> to compare the avalanche and snowball methods.</li></ul></div></section></div>
'''
    h += footer()
    write(path, h); reg(path)

def tool_page(t):
    path = f'/tools/{t["id"]}/'
    rel = [ART[i] for i in t['articles']]
    ld = [crumb_ld([('Home', '/'), ('Tools', '/tools/'), (t['name'], None)]),
          {'@context': 'https://schema.org', '@type': 'WebApplication', 'name': t['name'], 'url': SITE + path, 'description': t['meta'], 'applicationCategory': 'FinanceApplication', 'operatingSystem': 'Any', 'browserRequirements': 'Requires JavaScript', 'inLanguage': 'en', 'isAccessibleForFree': True, 'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'USD'}, 'publisher': ORG}]
    faq = ''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in t['faq'])
    h = head(t['title'], t['meta'], path, ld)
    h += header('tools')
    h += f'''<div class="wrap"><div class="ph">{crumbs([('Home', '/'), ('Tools', '/tools/'), (t['name'], None)])}<h1>{e(t['h1'])}</h1><p class="lead">{e(t['lead'])}</p></div>
<div class="panel"><div id="calc" data-tool="{t['id']}"><noscript><p class="warn">This calculator needs JavaScript. Please enable it in your browser to use the tool.</p></noscript></div>
<p class="muted small" style="margin:18px 0 0">Estimates for education only, not financial advice. Your numbers stay in your browser.</p></div>
{ad(AD_SLOT_TOOL)}
<div class="layout" style="padding-top:48px"><div class="prose">{t['body']}
<h2>Frequently asked questions</h2><div class="faq">{faq}</div>
<div class="note">Educational content only, not professional financial advice.</div></div>
<aside class="side"><h3>Read next</h3><ul class="linklist">{''.join(f'<li><a href="/articles/{a["id"]}/">{e(a["t"])}</a></li>' for a in rel)}</ul>
<h3 style="margin-top:28px">More tools</h3><ul class="linklist">{''.join(f'<li><a href="/tools/{x["id"]}/">{e(x["name"])}</a></li>' for x in TOOLS if x['id'] != t['id'])}</ul></aside></div></div>
'''
    h += footer('<script src="/assets/calc.js" defer></script>\n')
    write(path, h); reg(path)

tools_index()
for t in TOOLS: tool_page(t)

# ---------------- articles ----------------
def articles_index():
    path = '/articles/'
    ld = [crumb_ld([('Home', '/'), ('Articles', None)]), {'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': 'Money guides', 'url': SITE + path,
          'mainEntity': {'@type': 'ItemList', 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'url': f'{SITE}/articles/{a["id"]}/', 'name': a['t']} for i, a in enumerate(ARTS)]}}]
    h = head(ttl('Money Guides: Budgeting, Saving, Debt and Investing'), 'Plain-English guides on budgeting, saving, debt, side income and investing. Practical steps, worked examples and honest limits, free to read.', path, ld)
    h += header('articles')
    chips = '<button type="button" data-cat="all" aria-pressed="true">All</button>' + ''.join(f'<button type="button" data-cat="{c.lower()}" aria-pressed="false">{c}</button>' for c in CATS)
    h += f'''<div class="wrap"><div class="ph">{crumbs([('Home', '/'), ('Articles', None)])}<h1>Money guides</h1>
<p class="lead">Clear, honest and actionable guides on budgeting, saving, debt, side income and investing. Each one ends with a next step you can take today, often with a calculator to test your own numbers.</p></div>
<div class="tools-row"><div class="chips" role="group" aria-label="Filter by topic">{chips}</div><input id="sq" type="search" placeholder="Search articles…" aria-label="Search articles"></div>
<div class="grid g3" id="artlist">{''.join(art_card(a, True) for a in ARTS)}</div>
<p id="none" class="empty" hidden>No articles match your search.</p>
<section class="block"><div class="prose"><h2>How we write these guides</h2><p>Every guide starts with a real question people ask about money. We explain the idea in plain language, show a worked example with numbers you can check yourself, and describe the common mistakes. Where rules differ by country, we say so rather than guess. We aim to be useful first and are clear that content here is educational and not personal financial advice. Read more on our <a href="/about/">About page</a>.</p></div></section></div>
'''
    h += footer()
    write(path, h); reg(path)

def article_page(a):
    path = f'/articles/{a["id"]}/'
    tools = [TOOLMAP[i] for i in TOOL_FOR_ID.get(a['id'], TOOL_FOR[a['c']])]
    same = [x for x in ARTS if x['c'] == a['c'] and x['id'] != a['id']]
    other = [x for x in ARTS if x['c'] != a['c']]
    rel = (same + other)[:3]
    ld = [crumb_ld([('Home', '/'), ('Articles', '/articles/'), (a['t'], None)]),
          {'@context': 'https://schema.org', '@type': 'Article', 'headline': a['t'][:110], 'description': a['meta'], 'datePublished': DATE, 'dateModified': DATE, 'inLanguage': 'en', 'articleSection': a['c'],
           'wordCount': a['words'], 'image': SITE + '/assets/og-image.png', 'mainEntityOfPage': {'@type': 'WebPage', '@id': SITE + path},
           'author': {'@type': 'Organization', 'name': NAME + ' Editorial Team', 'url': SITE + '/about/'}, 'publisher': ORG}]
    SHORT={'how-to-negotiate-your-bills':'How to Negotiate Your Utility and Internet Bills'}
    h = head(ttl(SHORT.get(a['id'],a['t'])), a['meta'], path, ld, otype='article')
    h += header('articles')
    body = a['body']
    # place a single ad after the first two blocks if configured
    h += f'''<div class="wrap"><div class="ph" style="max-width:820px">{crumbs([('Home', '/'), ('Articles', '/articles/'), (a['c'], '/articles/#' + a['c'].lower())])}<span class="tag">{a['c']}</span><h1 style="margin-top:6px">{e(a['t'])}</h1><p class="lead">{e(a['d'])}</p>
<div class="byline"><span>By {NAME} Editorial Team</span><span>Updated <time datetime="{DATE}">{date_h()}</time></span><span>{a['min']} min read</span></div></div>
<div class="layout"><article class="prose serif">{body}{ad(AD_SLOT_ARTICLE)}
<div class="note">Educational content only, not professional financial advice. Figures are illustrative. Rules, rates and products vary by country and change over time.</div></article>
<aside class="side"><h3>Try the tools</h3><ul class="linklist">{''.join(f'<li><a href="/tools/{t["id"]}/">{e(t["name"])}</a></li>' for t in tools)}</ul>
<h3 style="margin-top:28px">Keep reading</h3><ul class="linklist">{''.join(f'<li><a href="/articles/{r["id"]}/">{e(r["t"])}</a></li>' for r in rel)}</ul></aside></div>
<section class="related"><div class="head"><h2>Related articles</h2><a class="btn ghost sm" href="/articles/">All articles</a></div><div class="grid g3">{''.join(art_card(r) for r in rel)}</div></section></div>
'''
    h += footer()
    write(path, h); reg(path)

articles_index()
for a in ARTS: article_page(a)

# ---------------- legal / company pages ----------------
def simple(path, title, desc, h1, body, cur='', lead='', noindex=False, extra_scripts=''):
    items = [('Home', '/'), (h1, None)]
    h = head(ttl(title), desc, path, [crumb_ld(items)], noindex=noindex)
    h += header(cur)
    h += f'<div class="wrap" style="max-width:860px"><div class="ph">{crumbs(items)}<h1>{e(h1)}</h1>{f"<p class=lead>{lead}</p>" if lead else ""}</div><div class="prose" style="padding-bottom:56px">{body}</div></div>\n'
    h += footer(extra_scripts)
    write(path, h); reg(path)

simple('/about/', 'About SmartSpendLab', 'SmartSpendLab is an independent educational finance site with free calculators and plain-English money guides. Learn how we work and how the site is funded.', 'About SmartSpendLab',
'''<p>SmartSpendLab builds free tools and plain-English guides that help people take control of their everyday money. We focus on the decisions that most households face: how to split an income, how to save, how to pay off debt and how small, regular amounts grow over time.</p>
<h2>What we do</h2>
<p>We publish two kinds of content. <a href="/tools/">Calculators</a> let you test your own numbers privately in the browser. <a href="/articles/">Guides</a> explain the reasoning behind the numbers, with worked examples, common mistakes and next steps. Each calculator links to the guides that explain it, and each guide links to the tools it relies on.</p>
<h2>How we create content</h2>
<ul><li>We start from a real, common question about money.</li><li>We explain it in plain language and show the arithmetic so you can check it.</li><li>We state assumptions clearly and say where rules differ between countries.</li><li>We avoid promises about returns and avoid recommending specific financial products.</li><li>We review and update pages when we find mistakes. If you spot one, please <a href="/contact/">tell us</a>.</li></ul>
<h2>Editorial independence</h2>
<p>Content is written independently. Advertisers and partners do not decide what we write or recommend.</p>
<h2>How the site is funded</h2>
<p>SmartSpendLab is free to use. It is supported by advertising and may include affiliate links in the future. If we earn a commission from a link, we will label it clearly. See our <a href="/disclaimer/#affiliate">affiliate disclosure</a>.</p>
<h2>Privacy</h2>
<p>The numbers you type into our calculators are processed in your browser and are not sent to us. Read our <a href="/privacy-policy/">Privacy Policy</a> for details about cookies, advertising and your rights.</p>
<div class="note"><b>Educational content only, not professional financial advice.</b> We are not licensed financial advisers, accountants, tax professionals or lawyers.</div>''', 'about')

simple('/contact/', 'Contact SmartSpendLab', 'Contact SmartSpendLab with questions, corrections or partnership ideas. We reply within two business days.', 'Contact us',
f'''<p>Questions, corrections or partnership ideas? Email us at <a href="mailto:{EMAIL}">{EMAIL}</a> or use the form below. We aim to reply within two business days. We cannot give personal financial advice.</p>
<div class="panel"><form id="cf" class="formgrid"><label class="f" for="cn">Name</label><input type="text" id="cn" required autocomplete="name"><label class="f" for="ce">Email</label><input type="email" id="ce" required autocomplete="email"><label class="f" for="cm">Message</label><textarea id="cm" rows="6" required></textarea>
<p style="margin:16px 0 0"><button class="btn" type="submit">Send message</button></p><p id="cok" class="muted small" role="status"></p></form></div>
<p class="muted small">The form opens your email app with the message ready to send. Your message is not stored on this website.</p>''', 'contact',
extra_scripts='<script>document.getElementById("cf").addEventListener("submit",function(ev){ev.preventDefault();var g=function(i){return document.getElementById(i).value};location.href="mailto:'+EMAIL+'?subject="+encodeURIComponent("Message from "+g("cn"))+"&body="+encodeURIComponent(g("cm")+"\\n\\nReply to: "+g("ce"));document.getElementById("cok").textContent="Opening your email app\u2026"});</script>\n')

simple('/privacy-policy/', 'Privacy Policy', 'How SmartSpendLab handles your data, cookies and advertising, and your rights under GDPR and CCPA.', 'Privacy Policy',
f'''<p class="muted">Last updated: {date_h()}</p>
<p>{NAME} (“we”, “us”) respects your privacy. This policy explains what information we collect, how we use it and the choices you have, including your rights under the EU and UK GDPR and the California Consumer Privacy Act (CCPA).</p>
<h2>Information we collect</h2>
<ul><li><b>Calculator inputs.</b> Numbers you enter into our calculators are processed in your browser. They are not sent to our servers and we cannot see them.</li><li><b>Preferences.</b> Your language and currency choices are saved in your browser’s local storage so we can remember them. They stay on your device.</li><li><b>Messages.</b> If you email us, we receive your name, email address and message, and we use them only to reply.</li><li><b>Technical data.</b> Our hosting provider may keep standard server logs, such as IP address, browser type and pages requested, for security and reliability.</li></ul>
<h2>Cookies and advertising</h2>
<p>We use Google AdSense to show ads. Third-party vendors, including Google, use cookies to serve ads based on a user’s prior visits to this and other websites. Google’s use of advertising cookies enables it and its partners to serve ads based on your visit to our site and other sites on the internet. You can opt out of personalised advertising by visiting <a href="https://adssettings.google.com" rel="noopener">Google Ads Settings</a> or <a href="https://www.aboutads.info" rel="noopener">aboutads.info</a>. You can also read <a href="https://policies.google.com/technologies/partner-sites" rel="noopener">how Google uses information from sites that use its services</a>. You can control cookies in your browser settings. Where required, such as in the European Economic Area and the United Kingdom, we ask for your consent before personalised ads are shown.</p>
<h2>How we use information</h2>
<p>We use information to operate and secure the site, reply to your messages, understand how the site is used and show advertising. We do not sell your personal information for money.</p>
<h2>Your GDPR rights (EU and UK)</h2>
<p>If you are in the EU or UK, you may ask to access, correct, delete, restrict or port your personal data, object to processing and withdraw consent at any time. Our legal bases are consent, legitimate interests such as keeping the site secure, and legal obligations. You may also lodge a complaint with your local data protection authority.</p>
<h2>Your CCPA rights (California)</h2>
<p>California residents may request to know what personal information we collect, request deletion, and opt out of the sale or sharing of personal information. We do not discriminate against people who exercise these rights.</p>
<h2>Retention</h2>
<p>We keep emails for as long as needed to respond and for a reasonable period afterwards. Local preferences stay in your browser until you clear them.</p>
<h2>Children</h2>
<p>This site is not directed to children under 13 (or 16 where local law requires), and we do not knowingly collect their personal information.</p>
<h2>Changes to this policy</h2>
<p>We may update this policy and will change the date above when we do.</p>
<h2>Contact</h2>
<p>For privacy questions or requests, email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>''')

simple('/terms/', 'Terms of Service', 'The terms for using SmartSpendLab: educational purpose, no financial advice, acceptable use, intellectual property and limits of liability.', 'Terms of Service',
f'''<p class="muted">Last updated: {date_h()}</p>
<p>By using {NAME} you agree to these terms. If you do not agree, please do not use the site.</p>
<h2>Educational purpose</h2>
<p>All content and calculators are provided for general educational purposes only. They are not financial, investment, tax or legal advice and do not create an adviser-client relationship. Please consult a qualified professional before making financial decisions.</p>
<h2>Accuracy</h2>
<p>We work to keep information accurate and up to date, but we cannot guarantee it is complete or error-free. Calculator results are estimates based on the numbers and assumptions you enter. Actual results will differ.</p>
<h2>Acceptable use</h2>
<p>You agree not to misuse the site, attempt to disrupt it, scrape it in a way that harms performance or use it for unlawful purposes.</p>
<h2>Intellectual property</h2>
<p>The text, design and code of this site belong to {NAME} unless stated otherwise. You may link to our pages and quote short excerpts with attribution. Please do not republish whole articles without permission.</p>
<h2>Third-party links and ads</h2>
<p>The site may display ads or link to other sites. We do not control and are not responsible for third-party content, products or services.</p>
<h2>Limitation of liability</h2>
<p>To the fullest extent permitted by law, {NAME} is not liable for any loss or damage arising from your use of, or reliance on, the site, its content or its tools. The site is provided “as is” without warranties of any kind.</p>
<h2>Changes</h2>
<p>We may update these terms from time to time. Continued use of the site means you accept the updated terms.</p>
<h2>Contact</h2>
<p>Questions about these terms? Email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>''')

simple('/disclaimer/', 'Financial Disclaimer and Affiliate Disclosure', 'SmartSpendLab provides educational content only. Read our financial disclaimer, limitation of liability and affiliate and advertising disclosure.', 'Financial Disclaimer',
'''<div class="note"><b>Educational content only, not professional financial advice.</b></div>
<p>SmartSpendLab provides general information for educational purposes. We are not licensed financial advisers, accountants, tax professionals or lawyers, and nothing here is personalised advice. Consult a qualified professional before making financial decisions.</p>
<h2>No guarantees</h2>
<p>Calculators produce estimates from the numbers you enter and assumptions such as steady returns. Actual results will differ. Investing involves risk, including loss of principal, and past performance does not guarantee future results.</p>
<h2 id="affiliate">Affiliate and advertising disclosure</h2>
<p>This site displays advertising, including ads served by Google AdSense, and may include affiliate links. If you click an affiliate link and make a purchase, we may earn a commission at no extra cost to you. We will label affiliate links clearly. Advertising and commissions never decide what we write or recommend.</p>
<h2>Limitation of liability</h2>
<p>Use this site at your own risk. To the fullest extent permitted by law, SmartSpendLab is not liable for any loss arising from your use of the content or tools. Laws and products vary by country, so check the rules that apply where you live.</p>''')

# 404 (not in sitemap)
h = head('Page not found | ' + NAME, 'The page you were looking for could not be found.', '/404.html', noindex=True) + header('')
h += '<div class="wrap" style="max-width:760px"><div class="ph"><h1>Page not found</h1><p class="lead">That page does not exist or has moved. Try one of these instead.</p><div class="cta" style="margin-top:20px"><a class="btn" href="/tools/">Browse tools</a><a class="btn ghost" href="/articles/">Read articles</a><a class="btn ghost" href="/">Go home</a></div></div></div>\n' + footer()
open(os.path.join(OUT, '404.html'), 'w', encoding='utf8').write(h)

# ---------------- seo files ----------------
sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u in URLS: sm.append(f'<url><loc>{SITE}{u}</loc><lastmod>{DATE}</lastmod></url>')
sm.append('</urlset>')
open(os.path.join(OUT, 'sitemap.xml'), 'w', encoding='utf8').write('\n'.join(sm) + '\n')
open(os.path.join(OUT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n')
pub = ADSENSE_CLIENT.replace('ca-', '') if ADSENSE_CLIENT else ''
open(os.path.join(OUT, 'ads.txt'), 'w').write(f'google.com, {pub}, DIRECT, f08c47fec0942fa0\n' if pub else '# Add your AdSense line here once approved, e.g.\n# google.com, pub-0000000000000000, DIRECT, f08c47fec0942fa0\n')

# OG image
try:
    from PIL import Image, ImageDraw, ImageFont
    im = Image.new('RGB', (1200, 630), (11, 15, 25)); d = ImageDraw.Draw(im)
    for r, c in [(520, (14, 34, 40)), (360, (13, 40, 46)), (200, (12, 52, 56))]:
        d.ellipse((190 - r // 2, 120 - r // 2, 190 + r // 2, 120 + r // 2), fill=c)
    fb = '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'; fs = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    d.ellipse((80, 220, 200, 340), outline=(16, 217, 160), width=5)
    d.text((140, 280), '$', font=ImageFont.truetype(fb, 78), fill=(16, 217, 160), anchor='mm')
    d.text((230, 270), 'SmartSpendLab', font=ImageFont.truetype(fb, 92), fill=(232, 237, 247), anchor='lm')
    d.text((84, 430), 'Free budget, savings and debt calculators', font=ImageFont.truetype(fs, 44), fill=(199, 209, 228))
    d.text((84, 492), 'Plain-English guides. Your numbers stay in your browser.', font=ImageFont.truetype(fs, 30), fill=(154, 168, 194))
    im.save(os.path.join(OUT, 'assets', 'og-image.png'), optimize=True)
except Exception as ex:
    print('OG image skipped:', ex)

print(f'Built {len(URLS)} indexable pages into {OUT}')
for a in ARTS: print(f'  {a["words"]:5d} words  {a["id"]}')
