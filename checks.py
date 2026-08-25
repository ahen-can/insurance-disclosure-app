"""Arithmetic cross-checks over an extracted form.

The model is asked to rate its own confidence, but self-reported confidence is
soft evidence -- it cannot tell you it read the prior-year column, because it
does not know it did. These checks are the hard half: totals that must hold by
the definition of the form, recomputed from the values that were actually
written. A form that fails one of these is wrong regardless of how confident the
model was, and that is worth more on a review sheet than any score.

A check is (label, left, right). Each side is a list of terms; a term is a field
name, "-field" to subtract it, or a number to use as-is. A check is skipped when
every field it names is missing or zero, so a form that was legitimately nil
does not generate noise.
"""

TOLERANCE = 0.01        # 1% of the larger side
FLOOR = 1.0             # ...but never flag a gap smaller than this


CHECKS_LIFE = {
    "L2": [
        ("Total income - total expense = profit before tax",
         ["total_income", "-total_expense"], ["profit_before_tax"]),
    ],
    "L4": [
        ("First year + renewal + single = net total",
         ["first_year_premiums", "renewal_premiums", "single_premiums"], ["net_total"]),
        ("India + outside India = net total",
         ["premium_income_india", "premium_income_outside_india"], ["net_total"]),
    ],
    "L5": [
        ("Business India + outside India = total commission and rewards",
         ["business_india", "business_outside_india"], ["total_commission_and_rewards"]),
    ],
    "L6": [
        ("Expense lines sum to total operating expenses",
         ["employee_remuneration", "travel", "training", "rent", "repairs",
          "print_stationery", "comms", "legal_professional", "medical_fee",
          "auditor", "advertisement", "interest_bank_charges", "depreciation",
          "brand_trade", "bd_sales_promotion", "stamp_duty", "it", "gst",
          "others"], ["total_operating_expenses"]),
        ("India + outside India = total operating expenses",
         ["inside_india", "outside_india"], ["total_operating_expenses"]),
    ],
    "L7": [
        ("Benefit lines sum to benefits paid (gross)",
         ["claims_by_death", "claims_by_maturity", "annuity_pension",
          "survival_benefit", "periodical_benefit", "health", "surrender",
          "withdrawals", "discontinuance_payments", "bonus",
          "interest_on_unclaimed", "other_benefits"], ["benefits_paid_gross"]),
        ("Gross + reinsurance accepted - ceded = benefits paid (net)",
         ["benefits_paid_gross", "reinsurance_accepted", "-reinsurance_ceded"],
         ["benefits_paid_net"]),
    ],
    "L9": [
        ("Shareholding adds up to 100%",
         ["promoters_indian", "promoters_foreign", "investors_indian",
          "investors_foreign", "others"], [1.0]),
    ],
    "L37": [
        ("Schemes by channel sum to total", ["schemes_agency", "schemes_banca",
         "schemes_ca", "schemes_broking", "schemes_micro", "schemes_direct",
         "schemes_imf", "schemes_others"], ["schemes_total"]),
        ("Premium by channel sums to total", ["premium_agency", "premium_banca",
         "premium_ca", "premium_broking", "premium_micro", "premium_direct",
         "premium_imf", "premium_others"], ["premium_total"]),
        ("Lives by channel sum to total", ["lives_agency", "lives_banca",
         "lives_ca", "lives_broking", "lives_micro", "lives_direct",
         "lives_imf", "lives_others"], ["lives_total"]),
    ],
    "L38": [
        ("Policies by channel sum to total", ["nop_agency", "nop_banca",
         "nop_ca", "nop_broking", "nop_micro", "nop_direct_website",
         "nop_direct_others", "nop_imf", "nop_csc", "nop_web_aggregator",
         "nop_pos", "nop_others"], ["nop_total"]),
        ("Premium by channel sums to total", ["premium_agency", "premium_banca",
         "premium_ca", "premium_broking", "premium_micro",
         "premium_direct_website", "premium_direct_others", "premium_imf",
         "premium_csc", "premium_web_aggregator", "premium_pos",
         "premium_others"], ["premium_total"]),
    ],
    "L45": [
        ("Opening + opened - closed = offices at end",
         ["branch_opening", "branch_opened", "-branch_closed"], ["branch_total"]),
        ("Rural + urban = offices at end",
         ["branch_rural", "branch_urban"], ["branch_total"]),
    ],
}


CHECKS_GENERAL = {
    "NL1": [
        ("Income lines sum to total income",
         ["premiums_earned_net", "profit_loss_on_sale_redemption_of_investments",
          "interest_dividend_and_rent_gross", "other_income"], ["total_income"]),
        ("Expense lines sum to total expenses",
         ["claims_incurred_net", "commission_net", "operating_expenses",
          "premium_deficiency"], ["total_expenses"]),
        ("Total income - total expenses = operating profit",
         ["total_income", "-total_expenses"], ["operating_profit_loss"]),
    ],
    "NL2": [
        ("Segment operating profits sum to total",
         ["operating_profit_fire", "operating_profit_marine",
          "operating_profit_miscellaneous"], ["total_operating_profit"]),
    ],
    "NL3": [
        ("Sources of funds = application of funds",
         ["total_sources"], ["total_application_of_funds"]),
        ("Share capital + reserves + fair value change + borrowings = total sources",
         ["share_capital", "reserves_and_surplus", "fair_value_change_account",
          "borrowings"], ["total_sources"]),
    ],
    "NL4": [
        ("Gross direct + RI accepted - RI ceded = net written premium",
         ["gross_direct_premium", "reinsurance_accepted", "-reinsurance_ceded"],
         ["net_written_premium"]),
        ("Lines of business sum to gross direct premium",
         ["fire", "marine_cargo", "marine_hull", "motor_od", "motor_tp", "health",
          "personal_accident", "travel", "crop_weather", "workmen_compensation",
          "public_product_liability", "engineering", "aviation", "other_liability",
          "specialty", "home", "other_miscellaneous"], ["gross_direct_premium"]),
        ("India + outside India = gross direct premium",
         ["total_gross_direct_premium_india",
          "total_gross_direct_premium_outside_india"], ["gross_direct_premium"]),
    ],
    "NL5": [
        ("Direct + RI accepted - RI ceded = net claims paid",
         ["claims_paid_direct", "ri_accepted_on_claims_paid",
          "-ri_ceded_on_claims_paid"], ["net_claims_paid"]),
        ("Net paid + closing outstanding - opening outstanding = net incurred",
         ["net_claims_paid", "closing_claims_outstanding",
          "-opening_claims_outstanding"], ["net_incurred_claims"]),
    ],
    "NL6": [
        ("Commission + rewards + distribution fees = gross commission",
         ["commission_and_remuneration", "rewards", "distribution_fees"],
         ["gross_commission"]),
        ("Gross + on RI accepted - on RI ceded = net commission",
         ["gross_commission", "commission_on_ri_accepted",
          "-commission_on_ri_ceded"], ["net_commission"]),
        ("Channels sum to total",
         ["individual_agents", "corporate_agents_banks_fii_hfc",
          "corporate_agents_others", "insurance_brokers", "direct_online",
          "misp_direct", "web_aggregators", "insurance_marketing_firm",
          "common_service_centres", "micro_agents", "point_of_sales_direct",
          "other"], ["total"]),
        ("India + outside India = total", ["india", "outside_india"], ["total"]),
    ],
    "NL7": [
        ("Expense lines sum to total operating expenses",
         ["employees_remuneration_and_welfare", "travel_and_conveyance",
          "training", "rent_rates_and_taxes", "repairs",
          "printing_and_stationery", "communication", "legal_and_professional",
          "medical_fees", "auditors_fees", "advertisement_and_publicity",
          "interest_and_bank_charges", "depreciation", "brand_trade_name_usage",
          "business_development_and_sales_promotion", "stamp_duty",
          "information_technology", "gst_expenses", "other_expenses"],
         ["total_operating_expenses"]),
        ("India + outside India = total operating expenses",
         ["india", "outside_india"], ["total_operating_expenses"]),
    ],
    "NL9": [
        ("Shareholding adds up to 100",
         ["indian_promoters", "foreign_promoters", "indian_investors",
          "foreign_investors", "others"], ["total"]),
    ],
    "NL10": [
        ("Reserve lines sum to total reserves and surplus",
         ["capital_reserve", "capital_redemption_reserve", "share_premium",
          "general_reserve", "catastrophe_reserve", "other_reserves",
          "profit_and_loss_balance"], ["total_reserves_and_surplus"]),
    ],
    "NL11": [
        ("Borrowing lines sum to total borrowings",
         ["debentures_bonds", "banks", "financial_institutions",
          "other_borrowings"], ["total_borrowings"]),
    ],
    "NL14": [
        ("Gross block - accumulated depreciation = net block",
         ["gross_block", "-accumulated_depreciation"], ["net_block"]),
        ("Asset classes sum to net block",
         ["land_and_buildings", "furniture_and_fittings",
          "information_technology_equipment", "vehicles", "office_equipment",
          "intangible_assets", "right_of_use_assets",
          "capital_work_in_progress"], ["net_block"]),
    ],
    "NL18": [
        ("Provision lines sum to total provisions",
         ["reserve_for_unexpired_risk", "premium_deficiency_reserve", "taxation",
          "employee_benefits", "other_provisions"], ["total_provisions"]),
    ],
    "NL34": [
        ("India + outside India = total gross direct premium",
         ["india_gross_direct_premium", "outside_india_gross_direct_premium"],
         ["total_gross_direct_premium"]),
        ("India + outside India = total policies",
         ["india_number_of_policies", "outside_india_number_of_policies"],
         ["total_number_of_policies"]),
        ("India + outside India = total claims paid",
         ["india_claims_paid", "outside_india_claims_paid"],
         ["total_claims_paid"]),
        ("India + outside India = total claims incurred",
         ["india_claims_incurred", "outside_india_claims_incurred"],
         ["total_claims_incurred"]),
    ],
    "NL36": [
        ("Channels sum to total",
         ["individual_agents", "corporate_agents_banks", "corporate_agents_others",
          "brokers", "micro_agents", "direct_officers_employees", "direct_online",
          "direct_other", "csc", "imf", "point_of_sales_person", "misp",
          "web_aggregators", "referral", "others"], ["total"]),
    ],
    "NL37": [
        # Filings often carry an unlabelled "Other Adjustment" row that the
        # template has no column for, so this can fail on a correct reading.
        # Kept anyway: it is what caught NL-37 being read across the wrong
        # pages, and the cost of the false positive is one page lookup.
        ("Opening + reported - settled - repudiated = closing outstanding "
         "(before any 'other adjustment' rows)",
         ["opening_outstanding", "reported_during_period",
          "-total_claims_settled", "-claims_repudiated"],
         ["total_claims_outstanding_end_of_period"]),
        ("Ageing buckets sum to claims outstanding",
         ["outstanding_within_1_month", "outstanding_1_3_months",
          "outstanding_3_6_months", "outstanding_6_12_months",
          "outstanding_more_than_1_year"],
         ["total_claims_outstanding_end_of_period"]),
    ],
    "NL41": [
        ("Opening + opened - closed = offices at end",
         ["no_of_offices_at_beginning_of_year", "opened_during_year",
          "-closed_during_year"], ["no_of_offices_at_end_of_year"]),
        ("Rural + urban = offices at end",
         ["rural_offices", "urban_offices"], ["no_of_offices_at_end_of_year"]),
    ],
    # NL-45 has no check: the template carries a cumulative "registered upto
    # the quarter" figure and no closing-pending column, so the complaints
    # movement cannot be closed off arithmetically.
}


def _side(terms, data):
    """Evaluate one side. Returns (value, named_fields, any_field_present)."""
    total = 0.0
    fields = []
    present = False
    for term in terms:
        if isinstance(term, (int, float)):
            total += term
            continue
        sign = -1.0 if term.startswith("-") else 1.0
        name = term.lstrip("-")
        fields.append(name)
        value = data.get(name)
        if isinstance(value, (int, float)):
            total += sign * float(value)
            if value:
                present = True
    return total, fields, present


def run_checks(form: str, data: dict, kind: str) -> list:
    """[{label, left, right, gap, passed, fields}, ...] for one form."""
    table = CHECKS_GENERAL if kind == "general" else CHECKS_LIFE
    results = []
    for label, left_terms, right_terms in table.get(form, []):
        left, left_fields, left_present = _side(left_terms, data)
        right, right_fields, right_present = _side(right_terms, data)
        if left_fields and not left_present:
            continue        # that side was not reported at all, not a mismatch
        if right_fields and not right_present:
            continue
        gap = abs(left - right)
        limit = max(FLOOR, TOLERANCE * max(abs(left), abs(right)))
        results.append({
            "label": label,
            "left": left,
            "right": right,
            "gap": gap,
            "passed": gap <= limit,
            "fields": left_fields + right_fields,
        })
    return results
