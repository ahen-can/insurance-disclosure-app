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

"""
