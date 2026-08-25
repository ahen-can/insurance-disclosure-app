"""Field map for the general-insurance (NL-form) template.

The lists below are the column order of `templates/template_general_v1.xlsx`,
left to right, starting at column B. Order is load-bearing: the writer puts
values in positionally, so a list that drifts out of step with the template
shifts every value on that sheet into the wrong column. `tests/test_template.py`
asserts the two stay in agreement.

Generated from the headers of the hand-made source workbook, then frozen here.
"""

# Data key -> sheet title in the template.
SHEET_TITLES = {
    "NL1": "NL-1 Revenue Account",
    "NL2": "NL-2 Profit & Loss",
    "NL3": "NL-3 Balance Sheet",
    "NL4": "NL-4 Premium",
    "NL5": "NL-5 Claims",
    "NL6": "NL-6 Commission",
    "NL7": "NL-7 Operating Expenses",
    "NL8": "NL-8 Share Capital",
    "NL9": "NL-9 Shareholding",
    "NL10": "NL-10 Reserves",
    "NL11": "NL-11 Borrowings",
    "NL14": "NL-14 Fixed Assets",
    "NL18": "NL-18 Provisions",
    "NL20": "NL-20 Analytical Ratios",
    "NL34": "NL-34 Geography",
    "NL36": "NL-36 Channel Premium",
    "NL37": "NL-37 Claims Data",
    "NL41": "NL-41 Office Info",
    "NL45": "NL-45 Grievances",
}

# Sheets whose header is deeper than the usual two rows. NL-34 groups its
# columns under India / Outside India / Total on row 2 and names them on row 3.
HEADER_ROWS = {
    "NL-34 Geography": 3,
}

SHEET_CONFIG_GENERAL = {
    # NL-1 Revenue Account -- 11 columns
    "NL1": [
        "premiums_earned_net", "profit_loss_on_sale_redemption_of_investments",
        "interest_dividend_and_rent_gross", "other_income", "total_income",
        "claims_incurred_net", "commission_net", "operating_expenses",
        "premium_deficiency", "total_expenses", "operating_profit_loss"
    ],
    # NL-2 Profit & Loss -- 13 columns
    "NL2": [
        "operating_profit_fire", "operating_profit_marine",
        "operating_profit_miscellaneous", "total_operating_profit",
        "total_investment_income", "other_income", "provisions", "other_expenses",
        "profit_before_tax", "profit_after_tax", "transfer_to_reserves",
        "opening_pandl_balance", "closing_pandl_balance"
    ],
    # NL-3 Balance Sheet -- 9 columns
    "NL3": [
        "share_capital", "reserves_and_surplus", "fair_value_change_account",
        "borrowings", "total_sources", "total_assets", "current_liabilities",
        "provisions", "total_application_of_funds"
    ],
    # NL-4 Premium -- 24 columns
    "NL4": [
        "gross_direct_premium", "reinsurance_accepted", "reinsurance_ceded",
        "net_written_premium", "net_earned_premium", "fire", "marine_cargo",
        "marine_hull", "motor_od", "motor_tp", "health", "personal_accident", "travel",
        "crop_weather", "workmen_compensation", "public_product_liability", "engineering",
        "aviation", "other_liability", "specialty", "home", "other_miscellaneous",
        "total_gross_direct_premium_india", "total_gross_direct_premium_outside_india"
    ],
    # NL-5 Claims -- 26 columns
    "NL5": [
        "claims_paid_direct", "ri_accepted_on_claims_paid", "ri_ceded_on_claims_paid",
        "net_claims_paid", "closing_claims_outstanding", "opening_claims_outstanding",
        "net_incurred_claims", "closing_ibnr_ibner", "opening_ibnr_ibner", "fire",
        "marine_cargo", "marine_hull", "motor_od", "motor_tp", "health",
        "personal_accident", "travel", "crop_weather", "workmen_compensation",
        "public_product_liability", "engineering", "aviation", "other_liability",
        "specialty", "home", "other_miscellaneous"
    ],
    # NL-6 Commission -- 22 columns
    "NL6": [
        "commission_and_remuneration", "rewards", "distribution_fees", "gross_commission",
        "commission_on_ri_accepted", "commission_on_ri_ceded", "net_commission",
        "individual_agents", "corporate_agents_banks_fii_hfc", "corporate_agents_others",
        "insurance_brokers", "direct_online", "misp_direct", "web_aggregators",
        "insurance_marketing_firm", "common_service_centres", "micro_agents",
        "point_of_sales_direct", "other", "total", "india", "outside_india"
    ],
    # NL-7 Operating Expenses -- 22 columns
    "NL7": [
        "employees_remuneration_and_welfare", "travel_and_conveyance", "training",
        "rent_rates_and_taxes", "repairs", "printing_and_stationery", "communication",
        "legal_and_professional", "medical_fees", "auditors_fees",
        "advertisement_and_publicity", "interest_and_bank_charges", "depreciation",
        "brand_trade_name_usage", "business_development_and_sales_promotion",
        "stamp_duty", "information_technology", "gst_expenses", "other_expenses",
        "total_operating_expenses", "india", "outside_india"
    ],
    # NL-8 Share Capital -- 8 columns
    "NL8": [
        "authorised_capital", "issued_capital", "subscribed_capital", "called_up_capital",
        "paid_up_capital_opening", "additions", "reductions", "paid_up_capital_closing"
    ],
    # NL-9 Shareholding -- 6 columns
    "NL9": [
        "indian_promoters", "foreign_promoters", "indian_investors", "foreign_investors",
        "others", "total"
    ],
    # NL-10 Reserves -- 8 columns
    "NL10": [
        "capital_reserve", "capital_redemption_reserve", "share_premium",
        "general_reserve", "catastrophe_reserve", "other_reserves",
        "profit_and_loss_balance", "total_reserves_and_surplus"
    ],
    # NL-11 Borrowings -- 5 columns
    "NL11": [
        "debentures_bonds", "banks", "financial_institutions", "other_borrowings",
        "total_borrowings"
    ],
    # NL-14 Fixed Assets -- 11 columns
    "NL14": [
        "land_and_buildings", "furniture_and_fittings",
        "information_technology_equipment", "vehicles", "office_equipment",
        "intangible_assets", "right_of_use_assets", "capital_work_in_progress",
        "gross_block", "accumulated_depreciation", "net_block"
    ],
    # NL-18 Provisions -- 6 columns
    "NL18": [
        "reserve_for_unexpired_risk", "premium_deficiency_reserve", "taxation",
        "employee_benefits", "other_provisions", "total_provisions"
    ],
    # NL-20 Analytical Ratios -- 26 columns
    "NL20": [
        "gross_direct_premium_growth", "gross_direct_premium_to_net_worth_growth_rate",
        "net_worth_growth_rate", "net_retention_ratio", "net_commission_ratio",
        "eom_to_gdp_ratio", "eom_to_nwp_ratio", "net_incurred_claims_to_nep",
        "claims_paid_to_claims_provisions", "combined_ratio", "investment_income_ratio",
        "technical_reserves_to_net_premium_ratio", "underwriting_balance_ratio",
        "operating_profit_ratio", "liquid_assets_to_liabilities_ratio",
        "net_earning_ratio", "return_on_net_worth_ratio", "asm_to_rsm_ratio",
        "gross_npa_ratio", "net_npa_ratio", "debt_equity_ratio",
        "debt_service_coverage_ratio", "interest_service_coverage_ratio", "eps_basic",
        "eps_diluted", "book_value_per_share"
    ],
    # NL-34 Geography -- 12 columns
    "NL34": [
        "india_gross_direct_premium", "india_number_of_policies", "india_claims_paid",
        "india_claims_incurred", "outside_india_gross_direct_premium",
        "outside_india_number_of_policies", "outside_india_claims_paid",
        "outside_india_claims_incurred", "total_gross_direct_premium",
        "total_number_of_policies", "total_claims_paid", "total_claims_incurred"
    ],
    # NL-36 Channel Premium -- 16 columns
    "NL36": [
        "individual_agents", "corporate_agents_banks", "corporate_agents_others",
        "brokers", "micro_agents", "direct_officers_employees", "direct_online",
        "direct_other", "csc", "imf", "point_of_sales_person", "misp", "web_aggregators",
        "referral", "others", "total"
    ],
    # NL-37 Claims Data -- 10 columns
    "NL37": [
        "opening_outstanding", "reported_during_period", "total_claims_settled",
        "claims_repudiated", "total_claims_outstanding_end_of_period",
        "outstanding_within_1_month", "outstanding_1_3_months",
        "outstanding_3_6_months", "outstanding_6_12_months",
        "outstanding_more_than_1_year"
    ],
    # NL-41 Office Info -- 18 columns
    "NL41": [
        "no_of_offices_at_beginning_of_year", "approved_during_year",
        "opened_during_year", "closed_during_year", "no_of_offices_at_end_of_year",
        "rural_offices", "urban_offices", "employees_on_roll", "employees_off_roll",
        "individual_agents", "corporate_agents_banks", "corporate_agents_others",
        "insurance_brokers", "web_aggregators", "imf", "micro_agents", "pos", "others"
    ],
    # NL-45 Grievances -- 7 columns
    "NL45": [
        "opening_balance", "complaints_resolved_fully_accepted",
        "complaints_resolved_partial_accepted", "rejected",
        "total_complaints_registered_upto_the_quarter_for_this_fy",
        "no_of_claim_complaints_per_10_000_policies",
        "no_of_policy_complaints_per_10_000_policies"
    ],
}

# Human-readable column header for each field, straight from the template.
# Used to caption the extraction prompt and the review sheet.
FIELD_LABELS = {
    "NL1": [
        "Premiums Earned (Net)", "Profit/(Loss) on Sale/Redemption of Investments",
        "Interest, Dividend & Rent - Gross", "Other Income", "Total Income",
        "Claims Incurred (Net)", "Commission (Net)", "Operating Expenses",
        "Premium Deficiency", "Total Expenses", "Operating Profit/(Loss)"
    ],
    "NL2": [
        "Operating Profit - Fire", "Operating Profit - Marine",
        "Operating Profit - Miscellaneous", "Total Operating Profit",
        "Total Investment Income", "Other Income", "Provisions", "Other Expenses",
        "Profit Before Tax", "Profit After Tax", "Transfer to Reserves",
        "Opening P&L Balance", "Closing P&L Balance"
    ],
    "NL3": [
        "Share Capital", "Reserves & Surplus", "Fair Value Change Account",
        "Borrowings", "Total Sources", "Total Assets", "Current Liabilities",
        "Provisions", "Total Application of Funds"
    ],
    "NL4": [
        "Gross Direct Premium", "Reinsurance Accepted", "Reinsurance Ceded",
        "Net Written Premium", "Net Earned Premium", "Fire", "Marine Cargo",
        "Marine Hull", "Motor OD", "Motor TP", "Health", "Personal Accident",
        "Travel", "Crop / Weather", "Workmen Compensation",
        "Public / Product Liability", "Engineering", "Aviation", "Other Liability",
        "Specialty", "Home", "Other Miscellaneous",
        "Total Gross Direct Premium - India",
        "Total Gross Direct Premium - Outside India"
    ],
    "NL5": [
        "Claims Paid - Direct", "RI Accepted on Claims Paid",
        "RI Ceded on Claims Paid", "Net Claims Paid", "Closing Claims Outstanding",
        "Opening Claims Outstanding", "Net Incurred Claims", "Closing IBNR + IBNER",
        "Opening IBNR + IBNER", "Fire", "Marine Cargo", "Marine Hull", "Motor OD",
        "Motor TP", "Health", "Personal Accident", "Travel", "Crop / Weather",
        "Workmen Compensation", "Public / Product Liability", "Engineering",
        "Aviation", "Other Liability", "Specialty", "Home", "Other Miscellaneous"
    ],
    "NL6": [
        "Commission & Remuneration", "Rewards", "Distribution Fees",
        "Gross Commission", "Commission on RI Accepted", "Commission on RI Ceded",
        "Net Commission", "Individual Agents", "Corporate Agents - Banks/FII/HFC",
        "Corporate Agents - Others", "Insurance Brokers", "Direct - Online",
        "MISP - Direct", "Web Aggregators", "Insurance Marketing Firm",
        "Common Service Centres", "Micro Agents", "Point of Sales - Direct",
        "Other", "Total", "India", "Outside India"
    ],
    "NL7": [
        "Employees Remuneration & Welfare", "Travel & Conveyance", "Training",
        "Rent, Rates & Taxes", "Repairs", "Printing & Stationery", "Communication",
        "Legal & Professional", "Medical Fees", "Auditors Fees",
        "Advertisement & Publicity", "Interest & Bank Charges", "Depreciation",
        "Brand / Trade Name Usage", "Business Development & Sales Promotion",
        "Stamp Duty", "Information Technology", "GST Expenses", "Other Expenses",
        "Total Operating Expenses", "India", "Outside India"
    ],
    "NL8": [
        "Authorised Capital", "Issued Capital", "Subscribed Capital",
        "Called-up Capital", "Paid-up Capital - Opening", "Additions", "Reductions",
        "Paid-up Capital - Closing"
    ],
    "NL9": [
        "Indian Promoters", "Foreign Promoters", "Indian Investors",
        "Foreign Investors", "Others", "Total"
    ],
    "NL10": [
        "Capital Reserve", "Capital Redemption Reserve", "Share Premium",
        "General Reserve", "Catastrophe Reserve", "Other Reserves",
        "Profit & Loss Balance", "Total Reserves & Surplus"
    ],
    "NL11": [
        "Debentures / Bonds", "Banks", "Financial Institutions", "Other Borrowings",
        "Total Borrowings"
    ],
    "NL14": [
        "Land & Buildings", "Furniture & Fittings",
        "Information Technology Equipment", "Vehicles", "Office Equipment",
        "Intangible Assets", "Right-of-use Assets", "Capital Work-in-progress",
        "Gross Block", "Accumulated Depreciation", "Net Block"
    ],
    "NL18": [
        "Reserve for Unexpired Risk", "Premium Deficiency Reserve", "Taxation",
        "Employee Benefits", "Other Provisions", "Total Provisions"
    ],
    "NL20": [
        "Gross Direct Premium Growth",
        "Gross Direct Premium to Net Worth Growth Rate", "Net Worth Growth Rate",
        "Net Retention Ratio", "Net Commission Ratio", "EOM to GDP Ratio",
        "EOM to NWP Ratio", "Net Incurred Claims to NEP",
        "Claims Paid to Claims Provisions", "Combined Ratio",
        "Investment Income Ratio", "Technical Reserves to Net Premium Ratio",
        "Underwriting Balance Ratio", "Operating Profit Ratio",
        "Liquid Assets to Liabilities Ratio", "Net Earning Ratio",
        "Return on Net Worth Ratio", "ASM to RSM Ratio", "Gross NPA Ratio",
        "Net NPA Ratio", "Debt Equity Ratio", "Debt Service Coverage Ratio",
        "Interest Service Coverage Ratio", "EPS – Basic", "EPS – Diluted",
        "Book Value per Share"
    ],
    "NL34": [
        "India - Gross Direct Premium", "India - Number of Policies",
        "India - Claims Paid", "India - Claims Incurred",
        "Outside India - Gross Direct Premium",
        "Outside India - Number of Policies", "Outside India - Claims Paid",
        "Outside India - Claims Incurred", "Total - Gross Direct Premium",
        "Total - Number of Policies", "Total - Claims Paid",
        "Total - Claims Incurred"
    ],
    "NL36": [
        "Individual Agents", "Corporate Agents - Banks",
        "Corporate Agents - Others", "Brokers", "Micro-Agents",
        "Direct-Officers/Employees", "Direct - Online", "Direct - Other", "CSC",
        "IMF", "Point of sales person", "MISP", "Web Aggregators", "Referral",
        "Others", "Total"
    ],
    "NL37": [
        "Opening Outstanding", "Reported During Period", "Total Claims Settled",
        "Claims Repudiated", "Total Claims Outstanding (end of period)",
        "Within 1 Month", "1-3 Months", "3-6 Months", "6-12 Months",
        "More Than 1 Year"
    ],
    "NL41": [
        "No. of offices at beginning of year", "Approved During Year",
        "Opened During Year", "Closed During Year", "No. of offices at end of year",
        "Rural Offices", "Urban Offices", "Employees - On-roll",
        "Employees - Off-roll", "Individual Agents", "Corporate Agents - Banks",
        "Corporate Agents - Others", "Insurance Brokers", "Web Aggregators", "IMF",
        "Micro Agents", "POS", "Others"
    ],
    "NL45": [
        "Opening balance", "Complaints Resolved-Fully Accepted",
        "Complaints Resolved-Partial Accepted", "Rejected",
        "Total complaints registered upto the quarter for this FY",
        "No. of claim complaints per 10,000 policies",
        "No. of policy complaints per 10,000 policies"
    ],
}
