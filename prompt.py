def build_prompt():   
    return f"""
You are extracting data from an Indian life insurance company's Public Disclosure document.

Return ONLY a valid JSON object. No explanation, no markdown, no extra text.
Use null for any missing value. Numbers only — no commas, no % signs, no Rs symbols.

Return this exact JSON structure:

{{
  "year": "FYXX",
  "company_name": "<full legal company name>",
  "L2": {{
    "amounts_transferred": <number>,
    "income_from_investments": <number>,
    "other_income": <number>,
    "total_income": <number>,
    "total_expense": <number>,
    "profit_before_tax": <number>,
    "profit_after_tax": <number>,
    "opening_balance": <number>,
    "net_profit_till_date": <number>
  }},
  "L3": {{
    "shareholders_funds": <number>,
    "borrowings": <number>,
    "policyholders_funds": <number>
  }},
  "L4": {{
    "first_year_premiums": <number>,
    "renewal_premiums": <number>,
    "single_premiums": <number>,
    "premium_income_india": <number>,
    "premium_income_outside_india": <number>,
    "net_total": <number>
  }},
  "L5": {{
    "first_year_commission": <number>,
    "ry_premium_commission": <number>,
    "single_premium_commission": <number>,
    "direct_commission": <number>,
    "reinsurance_accepted": <number>,
    "reinsurance_ceded": <number>,
    "rewards": <number>,
    "channelwise breakup": <number>,
    "agents": <number>,
    "banca": <number>,
    "ca_others": <number>,
    "broker": <number>,
    "micro_agents": <number>,
    "direct_online": <number>,
    "direct_others": <number>,
    "csc": <number>,
    "web_aggregator": <number>,
    "imf": <number>,
    "pos_direct": <number>,
    "others": <number>,
    "business_india": <number>,
    "business_outside_india": <number>,
    "total_commission_and_rewards": <number>
  }},
  "L6": {{
    "employee_remuneration": <number>,
    "travel": <number>,
    "training": <number>,
    "rent": <number>,
    "repairs": <number>,
    "print_stationery": <number>,
    "comms": <number>,
    "legal_professional": <number>,
    "medical_fee": <number>,
    "auditor": <number>,
    "advertisement": <number>,
    "interest_bank_charges": <number>,
    "depreciation": <number>,
    "brand_trade": <number>,
    "bd_sales_promotion": <number>,
    "stamp_duty": <number>,
    "it": <number>,
    "gst": <number>,
    "others": <number>,
    "inside_india": <number>,
    "outside_india": <number>,
    "total_operating_expenses": <number>
  }},
  "L7": {{
    "claims_by_death": <number>,
    "claims_by_maturity": <number>,
    "annuity_pension": <number>,
    "survival_benefit": <number>,
    "periodical_benefit": <number>,
    "health": <number>,
    "surrender": <number>,
    "withdrawals": <number>,
    "discontinuance_payments": <number>,
    "bonus": <number>,
    "interest_on_unclaimed": <number>,
    "other_benefits": <number>,
    "benefits_paid_gross": <number>,
    "reinsurance_ceded": <number>,
    "reinsurance_accepted": <number>,
    "benefits_paid_net": <number>
  }},
  "L9": {{
    "promoters_indian": <number>,
    "promoters_foreign": <number>,
    "investors_indian": <number>,
    "investors_foreign": <number>,
    "others": <number>
  }},
  "L22": {{
    "single_premium_to_total": <number>,
    "linked_nb_to_total_nb": <number>,
    "retention_ratio": <number>,
    "eom_ratio": <number>,
    "commission_ratio": <number>,
    "bd_sales_to_nb_premium": <number>,
    "pat_to_total_income": <number>,
    "persistency_premium_13": <number>,
    "persistency_premium_25": <number>,
    "persistency_premium_37": <number>,
    "persistency_premium_49": <number>,
    "persistency_premium_61": <number>,
    "persistency_nop_13": <number>,
    "persistency_nop_25": <number>,
    "persistency_nop_37": <number>,
    "persistency_nop_49": <number>,
    "persistency_nop_61": <number>,
    "solvency_ratio": <number>,
    "avg_ticket_size": <number>
  }},
  "L37": {{
    "schemes_agency": <number>, "schemes_banca": <number>, "schemes_ca": <number>,
    "schemes_broking": <number>, "schemes_micro": <number>, "schemes_direct": <number>,
    "schemes_imf": <number>, "schemes_others": <number>, "schemes_total": <number>,
    "premium_agency": <number>, "premium_banca": <number>, "premium_ca": <number>,
    "premium_broking": <number>, "premium_micro": <number>, "premium_direct": <number>,
    "premium_imf": <number>, "premium_others": <number>, "premium_total": <number>,
    "lives_agency": <number>, "lives_banca": <number>, "lives_ca": <number>,
    "lives_broking": <number>, "lives_micro": <number>, "lives_direct": <number>,
    "lives_imf": <number>, "lives_others": <number>, "lives_total": <number>
  }},
  "L38": {{
    "nop_agency": <number>, "nop_banca": <number>, "nop_ca": <number>,
    "nop_broking": <number>, "nop_micro": <number>, "nop_direct_website": <number>,
    "nop_direct_others": <number>, "nop_imf": <number>, "nop_csc": <number>,
    "nop_web_aggregator": <number>, "nop_pos": <number>, "nop_others": <number>,
    "nop_total": <number>,
    "premium_agency": <number>, "premium_banca": <number>, "premium_ca": <number>,
    "premium_broking": <number>, "premium_micro": <number>, "premium_direct_website": <number>,
    "premium_direct_others": <number>, "premium_imf": <number>, "premium_csc": <number>,
    "premium_web_aggregator": <number>, "premium_pos": <number>, "premium_others": <number>,
    "premium_total": <number>
  }},
  "L39_individual": {{
    "maturity_on_or_before": <number>, "maturity_1m": <number>, "maturity_1_3m": <number>,
    "maturity_3_6m": <number>, "maturity_6m_1y": <number>, "maturity_1y_plus": <number>,
    "maturity_total_claims": <number>, "maturity_total_amount": <number>,
    "survival_on_or_before": <number>, "survival_1m": <number>, "survival_1_3m": <number>,
    "survival_3_6m": <number>, "survival_6m_1y": <number>, "survival_1y_plus": <number>,
    "survival_total_claims": <number>, "survival_total_amount": <number>,
    "annuity_on_or_before": <number>, "annuity_1m": <number>, "annuity_1_3m": <number>,
    "annuity_3_6m": <number>, "annuity_6m_1y": <number>, "annuity_1y_plus": <number>,
    "annuity_total_claims": <number>, "annuity_total_amount": <number>,
    "surrender_on_or_before": <number>, "surrender_1m": <number>, "surrender_1_3m": <number>,
    "surrender_3_6m": <number>, "surrender_6m_1y": <number>, "surrender_1y_plus": <number>,
    "surrender_total_claims": <number>, "surrender_total_amount": <number>,
    "other_on_or_before": <number>, "other_1m": <number>, "other_1_3m": <number>,
    "other_3_6m": <number>, "other_6m_1y": <number>, "other_1y_plus": <number>,
    "other_total_claims": <number>, "other_total_amount": <number>,
    "death_on_or_before": <number>, "death_1m": <number>, "death_1_3m": <number>,
    "death_3_6m": <number>, "death_6m_1y": <number>, "death_1y_plus": <number>,
    "death_total_claims": <number>
  }},
  "L39_group": {{
    "maturity_on_or_before": <number>, "maturity_1m": <number>, "maturity_1_3m": <number>,
    "maturity_3_6m": <number>, "maturity_6m_1y": <number>, "maturity_1y_plus": <number>,
    "maturity_total_claims": <number>, "maturity_total_amount": <number>,
    "survival_on_or_before": <number>, "survival_1m": <number>, "survival_1_3m": <number>,
    "survival_3_6m": <number>, "survival_6m_1y": <number>, "survival_1y_plus": <number>,
    "survival_total_claims": <number>, "survival_total_amount": <number>,
    "annuity_on_or_before": <number>, "annuity_1m": <number>, "annuity_1_3m": <number>,
    "annuity_3_6m": <number>, "annuity_6m_1y": <number>, "annuity_1y_plus": <number>,
    "annuity_total_claims": <number>, "annuity_total_amount": <number>,
    "surrender_on_or_before": <number>, "surrender_1m": <number>, "surrender_1_3m": <number>,
    "surrender_3_6m": <number>, "surrender_6m_1y": <number>, "surrender_1y_plus": <number>,
    "surrender_total_claims": <number>, "surrender_total_amount": <number>,
    "other_on_or_before": <number>, "other_1m": <number>, "other_1_3m": <number>,
    "other_3_6m": <number>, "other_6m_1y": <number>, "other_1y_plus": <number>,
    "other_total_claims": <number>, "other_total_amount": <number>,
    "death_on_or_before": <number>, "death_1m": <number>, "death_1_3m": <number>,
    "death_3_6m": <number>, "death_6m_1y": <number>, "death_1y_plus": <number>,
    "death_total_claims": <number>
  }},
  "L41": {{
    "total_policies": <number>,
    "total_claims": <number>,
    "policy_complaints_per_10000": <number>,
    "claim_complaints_per_10000": <number>
  }},
  "L45": {{
    "branch_opening": <number>,
    "branch_approved": <number>,
    "branch_opened": <number>,
    "branch_closed": <number>,
    "branch_total": <number>,
    "branch_rural": <number>,
    "branch_urban": <number>,
    "employee_onrole": <number>,
    "employee_offrole": <number>,
    "agent_counts": <number>,
    "bank": <number>,
    "ca": <number>,
    "broker": <number>,
    "web_agg": <number>,
    "imf": <number>,
    "micro": <number>,
    "pos": <number>,
    "others": <number>
  }},
{CONFIDENCE_BLOCK}
}}

Important notes:
- Extract data for the latest financial year reported in the document. Determine the financial year from the report itself.

Populate the "year" field in the format:
FY23
FY24
FY25
FY26
etc.

- Please make sure that all values are for the year ended March 31, 20XX (FYXX) or up to March 31, 20XX
- Extract the insurer's full legal name exactly as it appears in the document.

Usually this appears near the beginning as:

"Name of the Insurer: ..."

Do not abbreviate or infer the name.

Examples:
"Axis Max Life Insurance Limited"
"HDFC Life Insurance Company Limited"
"ICICI Prudential Life Insurance Company Limited"

- L9 values are percentages of holding so divide the value by 100 so when I format it in excel, it is a percentage of correct value.
- L22 ratios/percentages: divide the value by 100 so when I format it in excel, it is a percentage of correct value.
- Make correct unit conversions between lakhs and crores wherever required.
- If a number is in brackets, it means it has a negative value i.e. (25) means -25.
- Auditor field in L-6 should comprise of all the fields under "Auditor".
e.g.
 Auditors' fees, expenses etc
a) as auditor: 98                                   
b) as adviser or in any other capacity, in 
respect of
(i) Taxation matters: 3                              
(ii) Insurance matters                            
(iii) Management services; and                                
c) in any other capacity
        - Certification: 62                            
        - Out of pocket expenses: 16

Above means Auditor value is 179.

- Search the entire PDF before returning null. Return null only if the required value is genuinely absent from the document. Do not return an entire section as null simply because the table format differs from previous reports.
- If null is being returned, replace it with 0.
{CONFIDENCE_NOTES}
"""


# --------------------------------------------------------------------------
# General insurance (NL forms)
#
# Kept apart from the life prompt above rather than parameterised: the two form
# families share almost no field names, and the one instruction that matters
# most inverts between them (life divides its ratios by 100 for a %-formatted
# template, general does not).
# --------------------------------------------------------------------------

CONFIDENCE_BLOCK = """
  "confidence": {
    "<FORM>": {"score": <0.0 to 1.0>, "note": "<why, one short line>"}
  },
  "review": [
    {"form": "<FORM>", "field": "<field name>", "reason": "<what you were unsure of>"}
  ]"""

CONFIDENCE_NOTES = """
CONFIDENCE AND REVIEW

Alongside the data, report how well the extraction actually went. This is used
to decide which numbers a human re-checks, so it is worth being honest rather
than reassuring.

- "confidence": one entry per form you were asked for, scored 0.0 to 1.0.
  1.0  the form was laid out plainly and every figure was unambiguous
  0.7  readable, but you had to interpret a label or pick between columns
  0.4  the layout fought you: merged cells, split rows, unlabelled columns
  0.1  you largely could not find the form, or had to guess
  Score the form you were actually looking at. A form that is genuinely absent
  from the document scores 0.0 with a note saying so.

- "review": every individual field you are not confident in. Add an entry when
  * the label in the document did not clearly match the field asked for
  * you combined or split rows to arrive at the number
  * two candidate figures existed and you chose one
  * the figure is present but implausible against the rest of the form
  * a value the form should contain was missing and you returned 0
  An empty list means you are confident in every single field. Only say that if
  it is true. Do not add an entry merely because a value is zero in the filing.

Do not pad this list to look thorough, and do not leave it empty to look
competent. The list is read by someone who will open the PDF to the page you
name.
"""


def _schema_for(code, fields, labels):
    lines = [f'  "{code}": {{']
    for i, (field, label) in enumerate(zip(fields, labels)):
        comma = "," if i < len(fields) - 1 else ""
        lines.append(f'    "{field}": <number>{comma}'.ljust(52) + f"// {label}")
    lines.append("  }")
    return "\n".join(lines)


def build_general_prompt():
    """Prompt for general (non-life) insurers, rendered from the NL field map.

    The JSON schema is generated from SHEET_CONFIG_GENERAL rather than written
    out by hand, so the keys the model is asked for cannot drift away from the
    columns the writer will file them under.
    """
    from config_general import FIELD_LABELS, SHEET_CONFIG_GENERAL, SHEET_TITLES

    blocks = ",\n".join(
        _schema_for(code, SHEET_CONFIG_GENERAL[code], FIELD_LABELS[code])
        for code in SHEET_CONFIG_GENERAL
    )
    form_list = "\n".join(f"  {code:<6} {SHEET_TITLES[code]}"
                          for code in SHEET_CONFIG_GENERAL)

    return f"""
You are extracting data from an Indian GENERAL (non-life) insurance company's
Public Disclosure document. These are the IRDAI NL-series forms.

Return ONLY a valid JSON object. No explanation, no markdown, no extra text.
Numbers only - no commas, no % signs, no Rs symbols.

Forms to extract:
{form_list}

WHICH COLUMN TO READ - read this twice, it is where these documents go wrong.

Every NL form in this document reports four columns of the same figure:

    For the quarter ended 31st March 20XX     <- NOT this
    For the period ended  31st March 20XX     <- THIS ONE, current year
    For the quarter ended 31st March 20XX-1   <- NOT this, prior year
    For the period ended  31st March 20XX-1   <- NOT this, prior year

Always take the "For the period ended" (year-to-date, full financial year)
column for the LATEST financial year in the document. Never the quarter column.
Never the prior year.

Work this out from the column headings only. Sheet titles and subtitles in
these filings are frequently stale - a form headed "as at 31st March 2025" may
carry March 2026 columns. The column heading wins, every time.

Some forms are also split by segment, with Fire / Marine / Miscellaneous
columns and then a Total. Take the TOTAL segment. NL-1 is always laid out this
way. If a form is split by line of business (NL-37), take the grand Total
column, and take the DIRECT page where the filing separates DIRECT from CO-INS.

OTHER NOTES

- All money figures go in LAKHS. Convert if the form states another unit; a
  multiplier such as "100000" printed near the top of a form means the figures
  are already in lakhs.
- A number in brackets is negative: (25) means -25.
- Ratios and percentages in NL-9 and NL-20: return the number AS PRINTED. If
  the form says 14.51%, return 14.51. If it says 0.99, return 0.99. Do NOT
  divide by 100.
- "N.A.", "-", "Nil" and blank all mean nothing was reported. Return 0.
- NL-7 auditors' fees should be the total of everything beneath the "Auditors'
  fees, expenses etc" heading - as auditor, plus taxation matters, plus
  certification, plus out of pocket expenses, and so on. Sum the sub-rows; do
  not read the (often blank) parent row.
- NL-37 ageing buckets: some insurers collapse the first two buckets into a
  single "Less than 3 months". Where that happens, put the combined figure in
  outstanding_1_3_months, leave outstanding_within_1_month as 0, and add a
  review entry saying the filing does not break the bucket out.
- NL-37 runs across SEVERAL PAGES, and each page repeats the same rows for a
  different set of lines of business, each with its own "Total" column. Those
  page totals are for that page only. Read every figure from ONE page - the
  DIRECT page whose Total column is the grand total - and never add figures
  from different NL-37 pages together. Every row you return (opening, reported,
  settled, repudiated, closing, ageing) must come from that same column. If
  closing outstanding does not roughly reconcile with opening plus reported
  less settled and repudiated, you are reading across pages: go back and take
  them all from one.
- NL-3 fair_value_change_account is the Fair Value Change Account on the
  sources-of-funds side of the balance sheet. Where the filing splits it into
  shareholders' and policyholders' funds, add the two together. It is routinely
  negative, and a negative figure here is correct - do not drop the sign. Check
  your answer: share capital plus reserves and surplus plus fair value change
  plus borrowings should equal the TOTAL of sources of funds.
- NL-41 "branches opened during the year" is often split into two sub-rows,
  "out of approvals of previous year" and "out of approvals of this year". Add
  them together for opened_during_year. Check your answer: offices at the
  beginning, plus opened, less closed, should equal offices at the end.
- Extract the insurer's full legal name exactly as printed, usually as "Name of
  the Insurer: ...". Do not abbreviate or infer it. Where the name carries a
  suffix such as "- DIRECT" or "- CO-INS", drop the suffix.
- Search the entire PDF before returning 0. Return 0 only when the value is
  genuinely absent. Do not return a whole form as zeros just because its layout
  differs from what you expected.

Return this exact JSON structure:

{{
  "year": "FYXX",
  "company_name": "<full legal company name>",
{blocks},
{CONFIDENCE_BLOCK}
}}

The "year" field is the financial year of the column you read, formatted FY23,
FY24, FY25, FY26.
{CONFIDENCE_NOTES}
"""
