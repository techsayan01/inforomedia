"""
Article templates — one per article type.

Each entry exposes:
  structure        : HTML scaffold the writer fills in
  writer_rules     : extra instructions appended to the writer prompt
  editor_checklist : list of must-have elements Priya checks

Shared reusable HTML components are defined at the top.
"""

# ── Shared components ─────────────────────────────────────────────────────────

_STAT_CALLOUT = """<div style="background:#e8f4fd;border-left:4px solid #0056b3;padding:16px 20px;border-radius:6px;margin:20px 0;">
  <span style="font-size:2em;font-weight:700;color:#0056b3;">[KEY STAT OR FIGURE]</span>
  <p style="margin:6px 0 0;color:#333;font-size:0.95em;">[One-line label explaining the stat]</p>
</div>"""

_SUMMARY_BOX = """<div style="background:#f8f9fa;padding:16px 20px;border-left:4px solid #007bff;border-radius:6px;margin-bottom:20px;">
  <h3 style="margin-top:0;">15 Sec Read</h3>
  <ul>
    <li>[Core news — what happened]</li>
    <li>[Why it matters — the implication]</li>
    <li>[Impact — who wins, who loses, or what changes]</li>
  </ul>
</div>"""

_WINNER_LOSER = """<div style="display:flex;gap:16px;margin-bottom:24px;">
  <div style="flex:1;background:#d4edda;border-left:4px solid #28a745;padding:14px;border-radius:6px;">
    <strong style="color:#155724;">Winner</strong>
    <p style="margin:6px 0 0;color:#155724;">[Entity that benefits most — one punchy sentence]</p>
  </div>
  <div style="flex:1;background:#f8d7da;border-left:4px solid #dc3545;padding:14px;border-radius:6px;">
    <strong style="color:#721c24;">Loser</strong>
    <p style="margin:6px 0 0;color:#721c24;">[Entity most exposed — one punchy sentence]</p>
  </div>
</div>"""

_BOTTOM_LINE = """<h2>The Bottom Line</h2>
<div style="background:#e9ecef;padding:20px;border-radius:8px;margin:30px 0;">
  <p style="margin:0;"><strong>[Single most important takeaway ~80 words. Include the focus keyword here.]</strong></p>
</div>"""

_FAQ = """<h3>Frequently Asked Questions</h3>
<h4>[Question 1 relevant to this story?]</h4>
<p>[Genuine answer, 40–60 words — not filler.]</p>
<h4>[Question 2?]</h4>
<p>[Genuine answer, 40–60 words.]</p>
<h4>[Question 3?]</h4>
<p>[Genuine answer, 40–60 words.]</p>"""

_ACTION_CHECKLIST = """<div style="background:#fff3cd;border-left:4px solid #ffc107;padding:16px 20px;border-radius:6px;margin:20px 0;">
  <strong>What Finance Leaders Should Do Now</strong>
  <ul style="margin:8px 0 0;">
    <li>[Specific action item 1]</li>
    <li>[Specific action item 2]</li>
    <li>[Specific action item 3]</li>
  </ul>
</div>"""


# ── Template definitions ──────────────────────────────────────────────────────

TEMPLATES: dict[str, dict] = {

    # ── 1. Breaking News ──────────────────────────────────────────────────────
    "breaking_news": {
        "structure": f"""[HOOK] One punchy opening sentence with the focus keyword. No heading above this.

{_SUMMARY_BOX}

{_WINNER_LOSER}

<h2>What Happened</h2>
2 paragraphs (~150 words total). Facts first — who, what, when, where.

<h2>Why It Matters for Finance Professionals</h2>
2 paragraphs (~200 words). Use <strong> on every key metric, dollar figure, percentage, company name.

<h2>Key Facts and Data Points</h2>
Bullet list of 5–7 concrete facts, numbers, or quotes from the source.

{_STAT_CALLOUT}

<h2>Industry Context</h2>
2 paragraphs (~150 words). How does this fit the bigger picture?

<h2>What Finance Leaders Should Watch</h2>
2 paragraphs (~150 words). Forward-looking, practical.

<h2>Global Market Angles</h2>
<h3>Asia</h3>
~60 words. India (RBI, SEBI, HDFC, Paytm), China (PBOC, Alipay), Japan (FSA, SoftBank), Singapore (MAS).
<h3>Europe</h3>
~60 words. ECB, FCA, Bundesbank, Deutsche Bank, Revolut, Klarna, DORA/MiCA.
<h3>United States</h3>
~60 words. Fed, SEC, OCC, Goldman Sachs, JPMorgan, Stripe, Nasdaq.

<h2>The Contrarian Take</h2>
~80 words starting with exactly: "Here's what nobody's saying about this:"

{_BOTTOM_LINE}

{_FAQ}""",

        "writer_rules": (
            "Use <strong> on every key metric, percentage, dollar figure, and company name. "
            "The Contrarian Take MUST start with 'Here\\'s what nobody\\'s saying about this:'. "
            "Global Market Angles must cover Asia, Europe, and US sub-sections."
        ),

        "editor_checklist": [
            "15 Sec Read summary box present at top",
            "Winner/Loser two-column box present",
            "Global Market Angles has Asia, Europe, US sub-sections",
            "Contrarian Take starts with 'Here's what nobody's saying about this:'",
            "At least one stat callout box with a highlighted figure",
            "FAQ has 3 genuine answers (40-60 words each)",
        ],
    },

    # ── 2. Data Insights ─────────────────────────────────────────────────────
    "data_insights": {
        "structure": f"""[HOOK] One punchy sentence that leads with the most surprising data point and includes the focus keyword.

{_SUMMARY_BOX}

<h2>The Headline Number</h2>
{_STAT_CALLOUT}
1 paragraph putting this figure in context — why this number is surprising or significant.

<h2>5 Key Findings</h2>
For each finding, use a stat callout then 1-2 sentences of commentary:
<h3>Finding 1: [Title]</h3>
{_STAT_CALLOUT}
[1-2 sentences of analysis]
<h3>Finding 2: [Title]</h3>
[stat callout + commentary]
<h3>Finding 3: [Title]</h3>
[stat callout + commentary]
<h3>Finding 4: [Title]</h3>
[stat callout + commentary]
<h3>Finding 5: [Title]</h3>
[stat callout + commentary]

<h2>What the Data Really Says</h2>
2 paragraphs (~200 words). Go beyond the headline — what's the underlying trend?

<h2>Methodology Note</h2>
<div style="background:#f8f9fa;border:1px solid #dee2e6;padding:14px 18px;border-radius:6px;font-size:0.9em;color:#555;">
  <strong>About this data:</strong> [Source, sample size, date range, methodology — be precise. If the source doesn't provide it, say so.]
</div>

<h2>Implications for CFOs and Finance Leaders</h2>
Bullet list of 4-5 specific, actionable implications.

{_ACTION_CHECKLIST}

{_BOTTOM_LINE}

{_FAQ}""",

        "writer_rules": (
            "Every key finding MUST have a stat callout div with a bold highlighted figure. "
            "Do NOT fabricate statistics — only use numbers from the source material. "
            "The Methodology Note must accurately reflect what the source says about data collection. "
            "Bold (<strong>) every percentage, dollar figure, and company name."
        ),

        "editor_checklist": [
            "15 Sec Read summary box present",
            "Hero stat callout box with a highlighted headline figure",
            "5 Key Findings with individual stat callouts",
            "Methodology Note section present",
            "Action checklist for finance leaders",
            "No fabricated statistics",
        ],
    },

    # ── 3. Earnings ──────────────────────────────────────────────────────────
    "earnings": {
        "structure": f"""[HOOK] Lead with the most important number — beat or miss — and include the focus keyword.

{_SUMMARY_BOX}

<h2>At a Glance</h2>
<div style="overflow-x:auto;margin:20px 0;">
<table style="width:100%;border-collapse:collapse;font-size:0.95em;">
  <thead>
    <tr style="background:#0056b3;color:#fff;">
      <th style="padding:10px 14px;text-align:left;">Metric</th>
      <th style="padding:10px 14px;text-align:right;">Reported</th>
      <th style="padding:10px 14px;text-align:right;">Estimate</th>
      <th style="padding:10px 14px;text-align:right;">YoY Change</th>
    </tr>
  </thead>
  <tbody>
    <tr style="border-bottom:1px solid #dee2e6;">
      <td style="padding:10px 14px;">Revenue</td>
      <td style="padding:10px 14px;text-align:right;"><strong>[value]</strong></td>
      <td style="padding:10px 14px;text-align:right;">[estimate]</td>
      <td style="padding:10px 14px;text-align:right;">[+/-X%]</td>
    </tr>
    <tr style="border-bottom:1px solid #dee2e6;background:#f8f9fa;">
      <td style="padding:10px 14px;">Net Income / EPS</td>
      <td style="padding:10px 14px;text-align:right;"><strong>[value]</strong></td>
      <td style="padding:10px 14px;text-align:right;">[estimate]</td>
      <td style="padding:10px 14px;text-align:right;">[+/-X%]</td>
    </tr>
    <tr style="border-bottom:1px solid #dee2e6;">
      <td style="padding:10px 14px;">Operating Margin</td>
      <td style="padding:10px 14px;text-align:right;"><strong>[value]</strong></td>
      <td style="padding:10px 14px;text-align:right;">[estimate]</td>
      <td style="padding:10px 14px;text-align:right;">[+/-X%]</td>
    </tr>
    <tr>
      <td style="padding:10px 14px;">[Key segment metric]</td>
      <td style="padding:10px 14px;text-align:right;"><strong>[value]</strong></td>
      <td style="padding:10px 14px;text-align:right;">[estimate]</td>
      <td style="padding:10px 14px;text-align:right;">[+/-X%]</td>
    </tr>
  </tbody>
</table>
</div>

<div style="display:inline-block;padding:8px 16px;border-radius:20px;font-weight:700;font-size:1em;margin-bottom:20px;background:[#d4edda if beat else #f8d7da];color:[#155724 if beat else #721c24];">
  [BEAT / MISS / IN LINE] — [one sentence verdict]
</div>

<h2>What Drove the Numbers</h2>
2 paragraphs (~150 words). Which business lines outperformed or underperformed?

<h2>Management Commentary</h2>
<blockquote style="border-left:4px solid #adb5bd;padding-left:15px;font-style:italic;color:#495057;margin:20px 0;">
  "[Direct quote from CEO/CFO if available, otherwise paraphrase the key forward guidance]"
</blockquote>
1 paragraph interpreting what management is really signalling.

<h2>Analyst Reaction</h2>
Bullet list of 3-4 analyst/market reactions if available, or Jordan's assessment of likely reactions.

<h2>What It Means for the Sector</h2>
2 paragraphs (~150 words). Implications for competitors, suppliers, investors.

<h2>Forward Outlook</h2>
{_STAT_CALLOUT}
2 paragraphs on guidance: what management is guiding to and whether the market will believe it.

{_BOTTOM_LINE}

{_FAQ}""",

        "writer_rules": (
            "Populate the At-a-Glance table ONLY with figures from the source — leave cells as 'N/A' if data isn't available. "
            "Do NOT invent analyst quotes. The Beat/Miss badge colour must match the actual result. "
            "Bold every financial figure. Include a stat callout for the forward guidance number."
        ),

        "editor_checklist": [
            "At-a-Glance metrics table present with revenue and at least 3 rows",
            "Beat/Miss verdict badge present",
            "Management Commentary section with a quote or paraphrase",
            "Forward Outlook section present",
            "No fabricated analyst quotes",
            "All financial figures in bold",
        ],
    },

    # ── 4. Product Launch ────────────────────────────────────────────────────
    "product_launch": {
        "structure": f"""[HOOK] One punchy sentence that names the product, the company, and why it matters. Include the focus keyword.

{_SUMMARY_BOX}

<h2>What It Does</h2>
<div style="background:#f0f7ff;border:1px solid #b8daff;padding:18px 22px;border-radius:8px;margin-bottom:20px;">
  <h3 style="margin-top:0;color:#004085;">[Product Name]</h3>
  <p style="margin:0;">[2-3 sentence plain-English description. What problem does it solve? Who is it for?]</p>
</div>

<h2>Key Features</h2>
Bullet list of 5-6 concrete features — be specific, no marketing fluff.

<h2>Pricing and Availability</h2>
<div style="background:#e8f4fd;border-left:4px solid #0056b3;padding:16px 20px;border-radius:6px;margin:20px 0;">
  <strong style="font-size:1.1em;color:#0056b3;">[Price point or pricing model]</strong>
  <p style="margin:6px 0 0;color:#333;">[Availability: regions, launch date, access model]</p>
</div>

<h2>Who It's For</h2>
2 paragraphs. Primary use cases and target buyer profile. Be specific — "mid-market CFOs running SAP" beats "finance teams".

<h2>How It Stacks Up</h2>
<div style="overflow-x:auto;margin:20px 0;">
<table style="width:100%;border-collapse:collapse;font-size:0.9em;">
  <thead>
    <tr style="background:#0056b3;color:#fff;">
      <th style="padding:10px 14px;text-align:left;">Feature</th>
      <th style="padding:10px 14px;text-align:center;">[This Product]</th>
      <th style="padding:10px 14px;text-align:center;">[Competitor 1]</th>
      <th style="padding:10px 14px;text-align:center;">[Competitor 2]</th>
    </tr>
  </thead>
  <tbody>
    <tr style="border-bottom:1px solid #dee2e6;">
      <td style="padding:10px 14px;">[Feature 1]</td>
      <td style="padding:10px 14px;text-align:center;">Yes</td>
      <td style="padding:10px 14px;text-align:center;">[Yes/No/Partial]</td>
      <td style="padding:10px 14px;text-align:center;">[Yes/No/Partial]</td>
    </tr>
    <tr style="border-bottom:1px solid #dee2e6;background:#f8f9fa;">
      <td style="padding:10px 14px;">[Feature 2]</td>
      <td style="padding:10px 14px;text-align:center;">Yes</td>
      <td style="padding:10px 14px;text-align:center;">[Yes/No/Partial]</td>
      <td style="padding:10px 14px;text-align:center;">[Yes/No/Partial]</td>
    </tr>
    <tr>
      <td style="padding:10px 14px;">[Feature 3]</td>
      <td style="padding:10px 14px;text-align:center;">Yes</td>
      <td style="padding:10px 14px;text-align:center;">[Yes/No/Partial]</td>
      <td style="padding:10px 14px;text-align:center;">[Yes/No/Partial]</td>
    </tr>
  </tbody>
</table>
</div>

<h2>Jordan's Verdict</h2>
<blockquote style="border-left:4px solid #007bff;padding-left:18px;font-style:italic;color:#333;margin:20px 0;font-size:1.05em;">
  [2-3 sentences in Jordan Blake's voice — opinionated, specific, answers "does this actually matter?"]
</blockquote>

{_BOTTOM_LINE}

{_FAQ}""",

        "writer_rules": (
            "The product description box must clearly explain what the product does in plain English. "
            "The comparison table must only include real competitors — do not fabricate feature comparisons. "
            "Jordan's Verdict must be opinionated and specific, not generic praise. "
            "Pricing callout must reflect the actual pricing from the source."
        ),

        "editor_checklist": [
            "What It Does box present with product name and plain-English description",
            "Key Features bullet list (5-6 items)",
            "Pricing and availability callout present",
            "Competitor comparison table present",
            "Jordan's Verdict blockquote present and opinionated",
            "No fabricated feature comparisons",
        ],
    },

    # ── 5. Funding ───────────────────────────────────────────────────────────
    "funding": {
        "structure": f"""[HOOK] Lead with the dollar amount, the company, and what it signals. Include the focus keyword.

{_SUMMARY_BOX}

<h2>The Deal at a Glance</h2>
<div style="background:#f0f7ff;border:1px solid #b8daff;padding:18px 22px;border-radius:8px;margin-bottom:24px;">
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">
    <div><strong style="color:#004085;">Amount Raised</strong><br><span style="font-size:1.5em;font-weight:700;">[$ amount]</span></div>
    <div><strong style="color:#004085;">Round</strong><br><span style="font-size:1.2em;">[Series A/B/C/Seed/etc.]</span></div>
    <div><strong style="color:#004085;">Valuation</strong><br><span style="font-size:1.2em;">[$ valuation or N/A]</span></div>
    <div><strong style="color:#004085;">Lead Investor</strong><br><span style="font-size:1.2em;">[name or N/A]</span></div>
  </div>
</div>

<h2>Where the Money Goes</h2>
2 paragraphs. What will this capital actually be used for — R&D, headcount, market expansion, acquisitions?

<h2>Who Benefits and Who Doesn't</h2>
<ul>
  <li><strong>[Entity 1]:</strong> [one sentence on impact]</li>
  <li><strong>[Entity 2]:</strong> [one sentence on impact]</li>
  <li><strong>[Entity 3 — a loser]:</strong> [one sentence on why this is bad news for them]</li>
  <li><strong>[Entity 4]:</strong> [one sentence on impact]</li>
</ul>

<h2>What This Signals About the Market</h2>
2 paragraphs (~200 words). What does smart money moving here reveal about macro trends in fintech/AI finance?

<h2>Global Ripple Effect</h2>
<h3>Asia</h3>
~60 words on implications for Asian fintech markets.
<h3>Europe</h3>
~60 words on implications for European markets.
<h3>United States</h3>
~60 words on US market implications.

{_BOTTOM_LINE}

{_FAQ}""",

        "writer_rules": (
            "The Deal at a Glance snapshot MUST include amount, round type, and lead investor — use 'N/A' if not in the source. "
            "Do NOT fabricate investor names or valuation figures. "
            "The 'Who Doesn't Benefit' section must include at least one entity that loses out."
        ),

        "editor_checklist": [
            "Deal at a Glance snapshot box present with amount, round, valuation, lead investor",
            "Where the Money Goes section present",
            "Who Benefits/Loses list with at least one loser",
            "What This Signals section with market context",
            "Global Ripple Effect with Asia, Europe, US",
            "No fabricated investor names or valuations",
        ],
    },

    # ── 6. Regulatory ────────────────────────────────────────────────────────
    "regulatory": {
        "structure": f"""[HOOK] State the enforcement action, the penalty/ruling, and who is affected. Include the focus keyword.

{_SUMMARY_BOX}

<h2>Severity Assessment</h2>
<div style="display:inline-block;padding:10px 20px;border-radius:6px;font-weight:700;font-size:1.05em;margin-bottom:20px;background:[#f8d7da / #fff3cd / #d4edda];color:[#721c24 / #856404 / #155724];">
  [CRITICAL / HIGH / MEDIUM] SEVERITY
</div>
<p>[One paragraph justifying the severity rating — what's the scale of impact?]</p>

<h2>What Happened</h2>
2 paragraphs. Facts: regulator, target, ruling, date, penalty amount. Use <strong> on every figure.
{_STAT_CALLOUT}

<h2>Who Is Affected</h2>
<ul>
  <li><strong>[Directly affected entity]:</strong> [specific impact]</li>
  <li><strong>[Industry sector]:</strong> [how this sets precedent]</li>
  <li><strong>[Compliance teams / CFOs]:</strong> [what they need to review]</li>
  <li><strong>[Consumers/customers]:</strong> [impact if any]</li>
</ul>

<h2>The Regulatory Background</h2>
2 paragraphs. What rule was violated? What's the enforcement pattern — is this a one-off or part of a broader crackdown?

{_ACTION_CHECKLIST}

<h2>Deadlines and Next Steps</h2>
<div style="background:#fff3cd;border-left:4px solid #ffc107;padding:14px 18px;border-radius:6px;margin:20px 0;">
  <strong>Key Dates:</strong>
  <ul style="margin:8px 0 0;">
    <li><strong>[Date]:</strong> [What must happen by this date]</li>
    <li><strong>[Date]:</strong> [Next milestone]</li>
  </ul>
</div>

<h2>What Finance Leaders Should Watch</h2>
2 paragraphs. Is this the start of a wider enforcement wave? What policies need reviewing?

{_BOTTOM_LINE}

{_FAQ}""",

        "writer_rules": (
            "The Severity badge must be one of CRITICAL / HIGH / MEDIUM — choose based on penalty scale and precedent. "
            "Use the exact penalty figure in a stat callout. "
            "The Action Checklist must contain specific, actionable steps — not generic 'review your compliance'. "
            "Deadlines section must only include dates from the source."
        ),

        "editor_checklist": [
            "Severity badge present (CRITICAL/HIGH/MEDIUM)",
            "Stat callout with penalty/fine amount",
            "Who Is Affected list with at least 3 entities",
            "Action checklist for finance leaders",
            "Deadlines section present",
            "No fabricated penalty figures or dates",
        ],
    },

    # ── 7. Market Movers ─────────────────────────────────────────────────────
    "market_movers": {
        "structure": f"""[HOOK] Lead with the key move — what moved, by how much, and why it matters. Include the focus keyword.

{_SUMMARY_BOX}

<h2>The Numbers</h2>
<div style="overflow-x:auto;margin:20px 0;">
<table style="width:100%;border-collapse:collapse;font-size:0.95em;">
  <thead>
    <tr style="background:#0056b3;color:#fff;">
      <th style="padding:10px 14px;text-align:left;">Asset / Index</th>
      <th style="padding:10px 14px;text-align:right;">Level / Price</th>
      <th style="padding:10px 14px;text-align:right;">Change</th>
      <th style="padding:10px 14px;text-align:right;">% Change</th>
    </tr>
  </thead>
  <tbody>
    <tr style="border-bottom:1px solid #dee2e6;">
      <td style="padding:10px 14px;"><strong>[Asset 1]</strong></td>
      <td style="padding:10px 14px;text-align:right;">[level]</td>
      <td style="padding:10px 14px;text-align:right;">[+/-value]</td>
      <td style="padding:10px 14px;text-align:right;color:[#28a745 or #dc3545];"><strong>[+/-X%]</strong></td>
    </tr>
    <tr style="border-bottom:1px solid #dee2e6;background:#f8f9fa;">
      <td style="padding:10px 14px;"><strong>[Asset 2]</strong></td>
      <td style="padding:10px 14px;text-align:right;">[level]</td>
      <td style="padding:10px 14px;text-align:right;">[+/-value]</td>
      <td style="padding:10px 14px;text-align:right;color:[#28a745 or #dc3545];"><strong>[+/-X%]</strong></td>
    </tr>
    <tr>
      <td style="padding:10px 14px;"><strong>[Asset 3]</strong></td>
      <td style="padding:10px 14px;text-align:right;">[level]</td>
      <td style="padding:10px 14px;text-align:right;">[+/-value]</td>
      <td style="padding:10px 14px;text-align:right;color:[#28a745 or #dc3545];"><strong>[+/-X%]</strong></td>
    </tr>
  </tbody>
</table>
</div>

<h2>What's Driving It</h2>
2 paragraphs (~200 words). The actual catalyst — macro data, central bank signal, geopolitical event. Be specific.

<h2>Winners and Losers</h2>
{_WINNER_LOSER}
Bullet list of 4-5 specific sectors, assets, or entities with one sentence on each.

<h2>The Macro Context</h2>
2 paragraphs. Where does this fit in the broader macro cycle? Interest rates, inflation, dollar strength?

<h2>Regional Ripple</h2>
<h3>Asia</h3>
~60 words on Asian market impact.
<h3>Europe</h3>
~60 words on European market impact.
<h3>United States</h3>
~60 words on US market impact.

<h2>What to Watch Next</h2>
Bullet list of 4-5 upcoming events or data points that will determine the next move.

{_BOTTOM_LINE}

{_FAQ}""",

        "writer_rules": (
            "Populate the Numbers table only with figures from the source — use 'N/A' where data is unavailable. "
            "Percentage changes must be coloured green (#28a745) for gains, red (#dc3545) for losses. "
            "The 'What to Watch Next' list must include specific upcoming events (e.g. 'Fed meeting June 12') not vague phrases."
        ),

        "editor_checklist": [
            "Numbers table present with at least 2 assets and % change",
            "% changes colour-coded green/red",
            "What's Driving It section with specific catalyst",
            "Regional Ripple has Asia, Europe, US",
            "What to Watch Next list with specific upcoming events",
        ],
    },

    # ── 8. Explainer ─────────────────────────────────────────────────────────
    "explainer": {
        "structure": f"""[HOOK] One sentence that frames why this concept matters right now for finance professionals. Include the focus keyword.

{_SUMMARY_BOX}

<h2>The Plain-English Definition</h2>
<div style="background:#f0f7ff;border-left:4px solid #0056b3;padding:18px 22px;border-radius:6px;margin-bottom:20px;">
  <strong style="font-size:1.05em;color:#004085;">[Focus keyword / concept]:</strong>
  <p style="margin:8px 0 0;">[2-3 sentence plain-English definition. No jargon. Write it so a smart non-specialist would understand it in 20 seconds.]</p>
</div>

<h2>How It Works — Step by Step</h2>
<ol style="padding-left:1.4em;">
  <li><strong>[Step 1 title]</strong> — [1 sentence explanation]</li>
  <li><strong>[Step 2 title]</strong> — [1 sentence explanation]</li>
  <li><strong>[Step 3 title]</strong> — [1 sentence explanation]</li>
  <li><strong>[Step 4 title]</strong> — [1 sentence explanation]</li>
  <li><strong>[Step 5 title]</strong> — [1 sentence explanation]</li>
</ol>

<h2>A Real-World Example</h2>
<blockquote style="border-left:4px solid #007bff;padding-left:18px;color:#333;margin:20px 0;">
  [Concrete real-world example — name real companies, real numbers, real outcomes. 3-4 sentences.]
</blockquote>

<h2>Why Finance Professionals Are Paying Attention</h2>
2 paragraphs (~200 words). Practical implications — what does understanding this concept unlock?

{_STAT_CALLOUT}

<h2>Common Misconceptions</h2>
<ul>
  <li><strong>Myth:</strong> [Common wrong belief] <strong>Reality:</strong> [Correction in 1-2 sentences]</li>
  <li><strong>Myth:</strong> [Common wrong belief] <strong>Reality:</strong> [Correction in 1-2 sentences]</li>
  <li><strong>Myth:</strong> [Common wrong belief] <strong>Reality:</strong> [Correction in 1-2 sentences]</li>
</ul>

<h2>The Landscape</h2>
<h3>Key Players</h3>
Bullet list of 4-5 companies/institutions with one sentence on their role.
<h3>Regulation and Standards</h3>
1 paragraph on the regulatory environment.

{_BOTTOM_LINE}

{_FAQ}""",

        "writer_rules": (
            "The Plain-English Definition box must contain a genuine simple definition — no jargon. "
            "The How It Works steps must be numbered and logically sequential. "
            "The Real-World Example must name real companies and real outcomes — do not use hypotheticals. "
            "Every Myth/Reality pair must correct a genuinely common misconception."
        ),

        "editor_checklist": [
            "Plain-English Definition box present",
            "How It Works has numbered steps (4-5 minimum)",
            "Real-World Example with real company names",
            "Common Misconceptions with myth/reality pairs",
            "Key Players section with 4-5 named entities",
            "Stat callout with a relevant data point",
        ],
    },
}


def get_template(article_type: str) -> dict:
    """Return template for *article_type*, falling back to breaking_news."""
    return TEMPLATES.get(article_type, TEMPLATES["breaking_news"])


# ── Entertainment article templates (InfoRo Media) ────────────────────────────

_ENT_SUMMARY_BOX = """<div style="background:#f8f9fa;padding:16px 20px;border-left:4px solid #e50914;border-radius:6px;margin-bottom:20px;">
  <h3 style="margin-top:0;">15 Sec Read</h3>
  <ul>
    <li>[What happened — the industry event or announcement]</li>
    <li>[Why it matters — the business/strategic implication]</li>
    <li>[Who wins, who loses, or what shifts]</li>
  </ul>
</div>"""

_ENT_WINNER_LOSER = """<div style="display:flex;gap:16px;margin-bottom:24px;">
  <div style="flex:1;background:#d4edda;border-left:4px solid #28a745;padding:14px;border-radius:6px;">
    <strong style="color:#155724;">Winner</strong>
    <p style="margin:6px 0 0;color:#155724;">[Studio, platform, artist, or market that gains — one punchy sentence]</p>
  </div>
  <div style="flex:1;background:#f8d7da;border-left:4px solid #dc3545;padding:14px;border-radius:6px;">
    <strong style="color:#721c24;">Loser</strong>
    <p style="margin:6px 0 0;color:#721c24;">[Competitor, rival platform, or market most exposed — one punchy sentence]</p>
  </div>
</div>"""

_ENT_BOTTOM_LINE = """<h2>The Bottom Line</h2>
<div style="background:#e9ecef;padding:20px;border-radius:8px;margin:30px 0;">
  <p style="margin:0;"><strong>[Single most important industry takeaway ~80 words. Include the focus keyword here.]</strong></p>
</div>"""

_ENT_REGIONAL = """<h2>Regional Market Impact</h2>
<h3>Asia-Pacific</h3>
~60 words. Cover implications for India (Bollywood/OTT), South Korea (K-content), Japan (anime/J-film), China (domestic box office), Southeast Asia (streaming penetration).
<h3>Europe and MENA</h3>
~60 words. Cover implications for UK, France, Germany, streaming rights, co-production treaties, and MENA licensing.
<h3>Americas</h3>
~60 words. Cover implications for US studios, Latin American OTT markets, and distribution economics."""

ENTERTAINMENT_TEMPLATES: dict[str, dict] = {

    # ── Breaking News (entertainment) ─────────────────────────────────────────
    "breaking_news": {
        "structure": f"""[HOOK] One punchy opening sentence that frames the industry significance. Include the focus keyword. No heading above this.

{_ENT_SUMMARY_BOX}

{_ENT_WINNER_LOSER}

<h2>What Happened</h2>
2 paragraphs (~150 words). Hard facts — who, what, when, where, deal terms or figures if available.

<h2>The Business Angle</h2>
2 paragraphs (~200 words). What this means for the industry: content strategy, market share, talent deals, distribution economics, or platform positioning. Use <strong> on every figure, deal value, and company name.

<h2>Key Facts and Figures</h2>
Bullet list of 5–7 concrete data points: box office, streaming numbers, deal terms, viewership metrics, release dates.

{_ENT_REGIONAL}

<h2>Industry Reaction</h2>
~100 words. What analysts, rivals, and trades are saying. Use blockquotes for direct quotes.

<h2>The Contrarian Take</h2>
~80 words starting with exactly: "Here's what nobody's saying about this:"

<h2>What to Watch Next</h2>
Bullet list of 3–4 forward-looking signals: upcoming release dates, competing titles, regulatory hurdles, deal milestones.

{_ENT_BOTTOM_LINE}

<h3>Frequently Asked Questions</h3>
3 FAQ items — frame questions from an industry professional's perspective (acquisitions exec, distributor, platform strategist):
<h4>Question here?</h4>
<p>Answer here (40–60 words).</p>""",

        "writer_rules": (
            "Use <strong> on every box office figure, deal value, streaming number, and company name. "
            "The Contrarian Take MUST start with 'Here\\'s what nobody\\'s saying about this:'. "
            "Regional Market Impact must cover Asia-Pacific, Europe/MENA, and Americas sub-sections. "
            "FAQ questions must be framed for industry professionals, not casual fans."
        ),

        "editor_checklist": [
            "15 Sec Read summary box present at top",
            "Winner/Loser two-column box present",
            "Regional Market Impact has Asia-Pacific, Europe/MENA, Americas sub-sections",
            "Contrarian Take starts with 'Here's what nobody's saying about this:'",
            "What to Watch Next section has 3–4 forward-looking bullets",
            "FAQ has 3 genuine answers framed for industry professionals (40–60 words each)",
        ],
    },

    # ── Box Office ────────────────────────────────────────────────────────────
    "box_office": {
        "structure": f"""[HOOK] Lead with the headline number and the focus keyword. Frame it as an industry signal, not a fan celebration.

{_ENT_SUMMARY_BOX}

{_ENT_WINNER_LOSER}

<h2>The Numbers</h2>
<div style="background:#e8f4fd;border-left:4px solid #0056b3;padding:16px 20px;border-radius:6px;margin:20px 0;">
  <span style="font-size:2em;font-weight:700;color:#0056b3;">[Opening weekend / cumulative gross]</span>
  <p style="margin:6px 0 0;color:#333;font-size:0.95em;">[Global / domestic split and context]</p>
</div>
1 paragraph contextualising the gross — against production budget, marketing spend, breakeven threshold, and comparable titles.

<h2>What the Numbers Actually Mean</h2>
2 paragraphs (~200 words). Profitability analysis: P&A costs, theatrical window economics, backend streaming value. What does this result mean for the franchise, studio slate, or distribution model?

<h2>Market-by-Market Breakdown</h2>
<h3>North America</h3>
~60 words with specific figures.
<h3>International</h3>
~80 words. Call out the top 3 international markets with figures.
<h3>China</h3>
~50 words. Performance vs. expectations — China remains a separate story for most Hollywood titles.

<h2>Competitive Landscape</h2>
~100 words. What is this title displacing? Which rival releases are affected? What does this tell us about audience appetite?

<h2>The Contrarian Take</h2>
~80 words starting with exactly: "Here's what nobody's saying about this:"

<h2>What to Watch Next</h2>
Bullet list of 3–4 signals: legs (week-2 drop), streaming window, international rollout, awards positioning.

{_ENT_BOTTOM_LINE}

<h3>Frequently Asked Questions</h3>
<h4>Question here?</h4>
<p>Answer here (40–60 words).</p>""",

        "writer_rules": (
            "Every gross figure must have context: budget, comparables, or breakeven. "
            "Do NOT write like a fan — frame every number as a business signal. "
            "China box office is always a separate sub-section. "
            "Contrarian Take MUST start with 'Here\\'s what nobody\\'s saying about this:'."
        ),

        "editor_checklist": [
            "Headline number stat callout box present",
            "Market-by-Market has North America, International, China sub-sections",
            "Profitability analysis in 'What the Numbers Actually Mean'",
            "Contrarian Take starts with 'Here's what nobody's saying about this:'",
            "What to Watch Next includes week-2 or streaming window signal",
            "FAQ framed for industry professionals",
        ],
    },

    # ── Streaming Data ────────────────────────────────────────────────────────
    "streaming_data": {
        "structure": f"""[HOOK] Lead with the most significant number or trend, include the focus keyword.

{_ENT_SUMMARY_BOX}

{_ENT_WINNER_LOSER}

<h2>The Headline Metric</h2>
<div style="background:#e8f4fd;border-left:4px solid #0056b3;padding:16px 20px;border-radius:6px;margin:20px 0;">
  <span style="font-size:2em;font-weight:700;color:#0056b3;">[Subscriber count / viewership hours / retention figure]</span>
  <p style="margin:6px 0 0;color:#333;font-size:0.95em;">[What this measures and why it matters]</p>
</div>
1 paragraph: context against previous quarter, analyst estimates, and platform-wide trends.

<h2>Platform Breakdown</h2>
Compare the key platforms relevant to this story. For each, use a sub-heading:
<h3>[Platform Name]</h3>
~50 words: metric + trend + strategic implication.

<h2>Content Performance Drivers</h2>
~150 words. Which titles, genres, or originals moved the needle? What does this reveal about audience demand by market?

<h2>What This Means for the Content Economy</h2>
2 paragraphs (~200 words). Licensing economics, content spend trajectories, theatrical-to-streaming windows, and what this signals for commissioning decisions.

{_ENT_REGIONAL}

<h2>The Contrarian Take</h2>
~80 words starting with exactly: "Here's what nobody's saying about this:"

<h2>What to Watch Next</h2>
Bullet list of 3–4 forward-looking signals: next earnings, content slate milestones, competitive moves.

{_ENT_BOTTOM_LINE}

<h3>Frequently Asked Questions</h3>
<h4>Question here?</h4>
<p>Answer here (40–60 words).</p>""",

        "writer_rules": (
            "Every metric must be attributed — name the source (platform, analyst, Antenna, Ampere). "
            "If a platform is known to suppress viewership data, say so explicitly. "
            "Frame all metrics in terms of business implications, not just the number itself. "
            "Contrarian Take MUST start with 'Here\\'s what nobody\\'s saying about this:'."
        ),

        "editor_checklist": [
            "Headline metric stat callout box present",
            "Platform Breakdown has sub-sections per relevant platform",
            "Content Performance Drivers identifies specific titles or genres",
            "Regional Market Impact has Asia-Pacific, Europe/MENA, Americas sub-sections",
            "Contrarian Take starts with 'Here's what nobody's saying about this:'",
            "All metrics attributed to a named source",
        ],
    },

    # ── Deal / Funding ────────────────────────────────────────────────────────
    "deal_funding": {
        "structure": f"""[HOOK] The strategic implication of the deal, not the press release headline. Include focus keyword.

{_ENT_SUMMARY_BOX}

{_ENT_WINNER_LOSER}

<h2>Deal Terms</h2>
<div style="background:#e8f4fd;border-left:4px solid #0056b3;padding:16px 20px;border-radius:6px;margin:20px 0;">
  <span style="font-size:2em;font-weight:700;color:#0056b3;">[Deal value or valuation]</span>
  <p style="margin:6px 0 0;color:#333;font-size:0.95em;">[Deal type: acquisition, co-production, licensing, rights deal]</p>
</div>
1–2 paragraphs: known deal terms, parties involved, rights acquired, territory scope, exclusivity, and timeline.

<h2>Strategic Rationale</h2>
2 paragraphs (~200 words). Why now? What gap does this fill? How does it alter the competitive landscape — IP library, geographic reach, talent access, distribution muscle?

<h2>Market Implications</h2>
2 paragraphs (~150 words). Which competitors are most exposed? Does this trigger countermoves? What precedent does it set for deal-making in this space?

{_ENT_REGIONAL}

<h2>Comparable Deals</h2>
Bullet list of 3–4 comparable transactions with deal values and outcomes — gives context for whether this price is justified.

<h2>The Contrarian Take</h2>
~80 words starting with exactly: "Here's what nobody's saying about this:"

<h2>What to Watch Next</h2>
Bullet list of 3–4 milestones: regulatory approval, content delivery, integration timeline, financial disclosures.

{_ENT_BOTTOM_LINE}

<h3>Frequently Asked Questions</h3>
<h4>Question here?</h4>
<p>Answer here (40–60 words).</p>""",

        "writer_rules": (
            "Always include comparable deals for valuation context. "
            "Name the financial advisers or law firms if disclosed — these are deal signals. "
            "Distinguish between IP acquisition, distribution rights, and co-production deals — they have very different implications. "
            "Contrarian Take MUST start with 'Here\\'s what nobody\\'s saying about this:'."
        ),

        "editor_checklist": [
            "Deal value stat callout box present",
            "Comparable Deals section has 3–4 real transactions with values",
            "Strategic Rationale is specific — not generic 'synergies' language",
            "Regional Market Impact has Asia-Pacific, Europe/MENA, Americas sub-sections",
            "Contrarian Take starts with 'Here's what nobody's saying about this:'",
            "What to Watch Next includes regulatory or financial milestone",
        ],
    },

    # ── Awards Buzz ───────────────────────────────────────────────────────────
    "awards_buzz": {
        "structure": f"""[HOOK] The industry significance of this awards development — not a red carpet recap. Include focus keyword.

{_ENT_SUMMARY_BOX}

{_ENT_WINNER_LOSER}

<h2>What Happened</h2>
1–2 paragraphs (~150 words). The nominations, wins, or snubs — with the full category context. What was predicted vs. what actually occurred?

<h2>The Business Implications</h2>
2 paragraphs (~200 words). Awards move money. What does this nomination or win mean for: theatrical re-releases, streaming licensing fees, DVD/physical sales, sequel greenlight probability, talent deal valuations, and international distribution appeal?

<h2>Awards Circuit Tracker</h2>
<table style="width:100%;border-collapse:collapse;margin:20px 0;">
  <thead>
    <tr style="background:#f1f3f5;">
      <th style="padding:10px;text-align:left;border-bottom:2px solid #dee2e6;">Title / Artist</th>
      <th style="padding:10px;text-align:left;border-bottom:2px solid #dee2e6;">Category</th>
      <th style="padding:10px;text-align:left;border-bottom:2px solid #dee2e6;">Result</th>
      <th style="padding:10px;text-align:left;border-bottom:2px solid #dee2e6;">Commercial Impact</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding:10px;border-bottom:1px solid #dee2e6;">[Title]</td>
      <td style="padding:10px;border-bottom:1px solid #dee2e6;">[Category]</td>
      <td style="padding:10px;border-bottom:1px solid #dee2e6;">[Won / Nominated / Snubbed]</td>
      <td style="padding:10px;border-bottom:1px solid #dee2e6;">[Expected box office / licensing lift]</td>
    </tr>
  </tbody>
</table>

<h2>Global Awards Landscape</h2>
<h3>Hollywood / Academy</h3>
~60 words on Oscars positioning and US industry implications.
<h3>European Circuit</h3>
~60 words on BAFTA, Cannes, Berlin, Venice implications — co-production and arthouse distribution.
<h3>Asian Awards</h3>
~60 words on BIFF, Hong Kong Film Awards, Filmfare, MAMA — and what these signal for regional licensing.

<h2>The Contrarian Take</h2>
~80 words starting with exactly: "Here's what nobody's saying about this:"

<h2>What to Watch Next</h2>
Bullet list of 3–4 upcoming awards milestones or titles to track.

{_ENT_BOTTOM_LINE}

<h3>Frequently Asked Questions</h3>
<h4>Question here?</h4>
<p>Answer here (40–60 words).</p>""",

        "writer_rules": (
            "Awards coverage must always tie back to money — licensing fees, re-release revenue, talent deal premiums. "
            "The Awards Circuit Tracker table must be populated with real titles and categories from the source. "
            "Global Awards Landscape must cover Hollywood, European, and Asian circuits. "
            "Contrarian Take MUST start with 'Here\\'s what nobody\\'s saying about this:'."
        ),

        "editor_checklist": [
            "15 Sec Read summary box present at top",
            "Awards Circuit Tracker table populated with real data",
            "Business Implications links nominations/wins to commercial outcomes",
            "Global Awards Landscape has Hollywood, European, Asian sub-sections",
            "Contrarian Take starts with 'Here's what nobody's saying about this:'",
            "FAQ framed for acquisitions or distribution professionals",
        ],
    },

    # ── Talent Movement ───────────────────────────────────────────────────────
    "talent_movement": {
        "structure": f"""[HOOK] Why this casting, signing, or agency move matters to the industry. Include focus keyword.

{_ENT_SUMMARY_BOX}

{_ENT_WINNER_LOSER}

<h2>What Was Announced</h2>
1–2 paragraphs (~150 words). The facts: who, which project, which studio/platform, what role or deal, and the deal structure if disclosed.

<h2>Why This Changes the Equation</h2>
2 paragraphs (~200 words). What does attaching this talent mean for the project's commercial prospects? Does it affect greenlight probability, marketing spend, international pre-sales, or streaming rights valuation? Who did this talent leave behind?

<h2>Talent Value Analysis</h2>
<div style="background:#e8f4fd;border-left:4px solid #0056b3;padding:16px 20px;border-radius:6px;margin:20px 0;">
  <strong style="font-size:1.1em;">[Talent Name]</strong>
  <ul style="margin:8px 0 0;">
    <li>Last 3 projects and box office / streaming performance</li>
    <li>Current representation (agency, management, publicist)</li>
    <li>Estimated quote or deal range (if reported)</li>
    <li>Key international markets where this talent has proven draw</li>
  </ul>
</div>

<h2>Agency and Representation Landscape</h2>
~100 words. Which agencies and management companies are gaining or losing ground? Any packaging implications?

{_ENT_REGIONAL}

<h2>The Contrarian Take</h2>
~80 words starting with exactly: "Here's what nobody's saying about this:"

<h2>What to Watch Next</h2>
Bullet list of 3–4 signals: other projects in contention, competing offers, deal close timeline.

{_ENT_BOTTOM_LINE}

<h3>Frequently Asked Questions</h3>
<h4>Question here?</h4>
<p>Answer here (40–60 words).</p>""",

        "writer_rules": (
            "Talent coverage is about market value and commercial logic, not personal biography. "
            "The Talent Value Analysis callout box must be populated with real career data from the source. "
            "Always identify the agency or management company — these are deal-structuring signals. "
            "Contrarian Take MUST start with 'Here\\'s what nobody\\'s saying about this:'."
        ),

        "editor_checklist": [
            "15 Sec Read summary box present at top",
            "Talent Value Analysis callout box populated with career data",
            "Agency and Representation Landscape section present",
            "Regional Market Impact has Asia-Pacific, Europe/MENA, Americas sub-sections",
            "Contrarian Take starts with 'Here's what nobody's saying about this:'",
            "FAQ framed for producers or casting/distribution professionals",
        ],
    },

    # ── Platform Strategy ─────────────────────────────────────────────────────
    "platform_strategy": {
        "structure": f"""[HOOK] The strategic signal behind the platform move. Include focus keyword.

{_ENT_SUMMARY_BOX}

{_ENT_WINNER_LOSER}

<h2>What Changed</h2>
2 paragraphs (~150 words). The announcement: pricing, content slate, market entry/exit, technology change, or partnership.

<h2>Strategic Read</h2>
2 paragraphs (~200 words). Why now? What does this reveal about the platform's growth thesis, profitability pressure, or competitive positioning? Use <strong> on all figures: subscriber counts, content spend, ARPU, churn rates.

<h2>Platform Scorecard</h2>
<table style="width:100%;border-collapse:collapse;margin:20px 0;">
  <thead>
    <tr style="background:#f1f3f5;">
      <th style="padding:10px;text-align:left;border-bottom:2px solid #dee2e6;">Platform</th>
      <th style="padding:10px;text-align:left;border-bottom:2px solid #dee2e6;">Subscribers</th>
      <th style="padding:10px;text-align:left;border-bottom:2px solid #dee2e6;">Content Spend</th>
      <th style="padding:10px;text-align:left;border-bottom:2px solid #dee2e6;">Strategic Position</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding:10px;border-bottom:1px solid #dee2e6;">[Platform]</td>
      <td style="padding:10px;border-bottom:1px solid #dee2e6;">[Figure]</td>
      <td style="padding:10px;border-bottom:1px solid #dee2e6;">[Figure]</td>
      <td style="padding:10px;border-bottom:1px solid #dee2e6;">[One-line read]</td>
    </tr>
  </tbody>
</table>

{_ENT_REGIONAL}

<h2>Competitive Fallout</h2>
~100 words. Which rivals are most exposed? Does this force a counter-move? Who benefits?

<h2>The Contrarian Take</h2>
~80 words starting with exactly: "Here's what nobody's saying about this:"

<h2>What to Watch Next</h2>
Bullet list of 3–4 milestones: earnings disclosures, content delivery dates, pricing experiments, market expansion signals.

{_ENT_BOTTOM_LINE}

<h3>Frequently Asked Questions</h3>
<h4>Question here?</h4>
<p>Answer here (40–60 words).</p>""",

        "writer_rules": (
            "Platform Strategy articles must include the Platform Scorecard table with real figures from the source. "
            "Always name the metric source — platform self-reported vs. analyst estimates are very different. "
            "Regional Market Impact is essential: streaming penetration varies dramatically by region. "
            "Contrarian Take MUST start with 'Here\\'s what nobody\\'s saying about this:'."
        ),

        "editor_checklist": [
            "15 Sec Read summary box present at top",
            "Platform Scorecard table populated with real figures",
            "Regional Market Impact has Asia-Pacific, Europe/MENA, Americas sub-sections",
            "Competitive Fallout section present",
            "Contrarian Take starts with 'Here's what nobody's saying about this:'",
            "All platform metrics attributed to a named source",
        ],
    },

    # ── Explainer ─────────────────────────────────────────────────────────────
    "explainer": {
        "structure": f"""[HOOK] Why an industry professional needs to understand this right now. Include focus keyword.

{_ENT_SUMMARY_BOX}

<h2>What Is [Topic]?</h2>
2 paragraphs (~200 words). Clear, jargon-free definition with industry context. Who are the key players? What scale are we talking about?

<h2>How It Works</h2>
Step-by-step numbered list (4–5 steps). Each step: title + 1–2 sentence explanation.
<ol>
  <li><strong>[Step title]</strong> — [explanation]</li>
</ol>

<h2>Why It Matters to the Entertainment Industry</h2>
2 paragraphs (~150 words). Distribution economics, content valuation, talent deal structures, or platform strategy implications.

<h2>Key Players</h2>
Bullet list of 4–6 named companies, platforms, or individuals with one-line role descriptions.

<h2>The Numbers</h2>
<div style="background:#e8f4fd;border-left:4px solid #0056b3;padding:16px 20px;border-radius:6px;margin:20px 0;">
  <span style="font-size:2em;font-weight:700;color:#0056b3;">[Key market size or metric]</span>
  <p style="margin:6px 0 0;color:#333;font-size:0.95em;">[Source and context]</p>
</div>

<h2>Common Misconceptions</h2>
3 myth/reality pairs:
<p><strong>Myth:</strong> [Common misunderstanding]</p>
<p><strong>Reality:</strong> [What industry insiders actually know]</p>

{_ENT_REGIONAL}

<h2>The Contrarian Take</h2>
~80 words starting with exactly: "Here's what nobody's saying about this:"

{_ENT_BOTTOM_LINE}

<h3>Frequently Asked Questions</h3>
<h4>Question here?</h4>
<p>Answer here (40–60 words).</p>""",

        "writer_rules": (
            "Write for an industry professional who knows entertainment but may be unfamiliar with this specific topic. "
            "Never condescend. Never over-explain what a studio or streaming platform is. "
            "Common Misconceptions must reflect real industry misunderstandings, not obvious basic facts. "
            "Contrarian Take MUST start with 'Here\\'s what nobody\\'s saying about this:'."
        ),

        "editor_checklist": [
            "15 Sec Read summary box present at top",
            "How It Works has 4–5 numbered steps",
            "Common Misconceptions has 3 myth/reality pairs",
            "Key Players section has 4–6 named entities",
            "Stat callout with a relevant market figure",
            "Regional Market Impact covers Asia-Pacific, Europe/MENA, Americas",
        ],
    },
}

# Merge entertainment templates into the main TEMPLATES dict so get_template()
# finds them automatically when a site uses these article type keys.
TEMPLATES.update(ENTERTAINMENT_TEMPLATES)
