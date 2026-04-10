# ─────────────────────────────────────────────────────────────────────────────
# minutes_generator.py — Project Finance Contract Minutes Generator
#
# Translates a SPE diagram + PF assumptions into a set of contract documents:
# Facility Agreement, Common Terms Agreement, Intercreditor Agreement,
# Direct Agreements, Security Trust Deed, Accounts Agreement.
#
# Reference: agent_reference.md Section 18 (full-stack PF spec)
# ─────────────────────────────────────────────────────────────────────────────
import datetime
from typing import Dict, List

from pf_models import (
    DiagramState, DiagramNode, PFAssumptions,
    Clause, ContractDocument, GeneratedMinutes,
)


# ─── Role mapping ────────────────────────────────────────────────────────────

ROLE_MAP: Dict[str, str] = {
    "spv":       "Borrower",
    "sponsor":   "Sponsor",
    "lender":    "Senior Lender",
    "mla":       "Mandated Lead Arranger",
    "dfi":       "DFI Lender",
    "offtaker":  "Offtaker",
    "epc":       "EPC Contractor",
    "om":        "O&M Operator",
    "govt":      "Contracting Authority",
    "insurance": "Insurer",
    "dsra":      "Account Bank",
    "custom":    "Party",
}

RELEVANT_TYPES: Dict[str, List[str]] = {
    "Facility Agreement":                  ["spv", "lender", "mla", "dfi"],
    "Common Terms Agreement":              ["spv", "lender", "mla", "dfi"],
    "Intercreditor Agreement":             ["lender", "mla", "dfi"],
    "Direct Agreement — EPC Contractor":   ["spv", "epc", "lender", "mla"],
    "Direct Agreement — O&M Operator":     ["spv", "om", "lender", "mla"],
    "Direct Agreement — Offtaker / PPA":   ["spv", "offtaker", "lender", "mla"],
    "Direct Agreement — Concession / PPP": ["spv", "govt", "lender", "mla"],
    "Security Trust Deed":                 ["spv", "lender", "mla", "dfi", "sponsor"],
    "Accounts Agreement":                  ["spv", "dsra", "lender", "mla"],
}


# ─── Algorithm — Step 1: classify diagram ────────────────────────────────────

def classify_diagram(diagram: DiagramState) -> dict:
    """Count entity types and produce boolean flags."""
    counts: Dict[str, int] = {}
    for node in diagram.nodes:
        counts[node.type] = counts.get(node.type, 0) + 1
    return {
        "num_lenders":   counts.get("lender", 0) + counts.get("mla", 0) + counts.get("dfi", 0),
        "num_sponsors":  counts.get("sponsor", 0),
        "has_spv":       counts.get("spv", 0) > 0,
        "has_dfi":       counts.get("dfi", 0) > 0,
        "has_govt":      counts.get("govt", 0) > 0,
        "has_epc":       counts.get("epc", 0) > 0,
        "has_om":        counts.get("om", 0) > 0,
        "has_offtaker":  counts.get("offtaker", 0) > 0,
        "has_dsra":      counts.get("dsra", 0) > 0,
        "has_insurance": counts.get("insurance", 0) > 0,
        "has_mla":       counts.get("mla", 0) > 0,
    }


# ─── Algorithm — Step 2: select documents ────────────────────────────────────

def select_documents(flags: dict) -> List[str]:
    """Decide which contract documents to generate, based on entity flags."""
    docs: List[str] = []
    if flags["has_spv"] and flags["num_lenders"] > 0:
        docs.append("Facility Agreement")
    if flags["num_lenders"] >= 2 or flags["has_dfi"]:
        docs.append("Common Terms Agreement")
    if flags["num_lenders"] >= 2:
        docs.append("Intercreditor Agreement")
    if flags["has_epc"]:
        docs.append("Direct Agreement — EPC Contractor")
    if flags["has_om"]:
        docs.append("Direct Agreement — O&M Operator")
    if flags["has_offtaker"]:
        docs.append("Direct Agreement — Offtaker / PPA")
    if flags["has_govt"]:
        docs.append("Direct Agreement — Concession / PPP")
    docs.append("Security Trust Deed")
    docs.append("Accounts Agreement")
    return docs


# ─── Algorithm — Step 3: extract parties ─────────────────────────────────────

def extract_parties(nodes: List[DiagramNode], document_type: str) -> List[dict]:
    """Map relevant diagram nodes to legal parties for a given document type."""
    relevant = RELEVANT_TYPES.get(document_type, list(ROLE_MAP.keys()))
    return [
        {"name": n.name, "role": ROLE_MAP.get(n.type, "Party"), "type": n.type}
        for n in nodes if n.type in relevant
    ]


# ─── Algorithm — Step 4: populate clause templates ───────────────────────────

def populate_clause(template: str, diagram: DiagramState, a: PFAssumptions) -> str:
    """Replace all {{VARIABLE}} placeholders in a clause template."""
    spv      = next((n for n in diagram.nodes if n.type == "spv"), None)
    sponsors = [n for n in diagram.nodes if n.type == "sponsor"]
    lenders  = [n for n in diagram.nodes if n.type in ("lender", "mla", "dfi")]
    dsra_node = next((n for n in diagram.nodes if n.type == "dsra"), None)

    debt_amt   = a.total_ev * a.debt_percentage
    equity_amt = a.total_ev * (1 - a.debt_percentage)

    vars_map: Dict[str, str] = {
        "{{BORROWER_NAME}}":          spv.name if spv else "[PROJECT CO. NAME]",
        "{{SPONSOR_NAMES}}":          " and ".join(s.name for s in sponsors) or "[SPONSOR]",
        "{{LENDER_NAMES}}":           ", ".join(l.name for l in lenders) or "[LENDER]",
        "{{CURRENCY}}":               a.currency,
        "{{FACILITY_AMOUNT}}":        f"{debt_amt:,.0f}",
        "{{EQUITY_AMOUNT}}":          f"{equity_amt:,.0f}",
        "{{DEBT_AMOUNT}}":            f"{debt_amt:,.0f}",
        "{{TOTAL_EV}}":               f"{a.currency} {a.total_ev:,.0f}",
        "{{DEBT_PCT}}":               f"{a.debt_percentage * 100:.0f}",
        "{{EQUITY_PCT}}":             f"{(1 - a.debt_percentage) * 100:.0f}",
        "{{MARGIN}}":                 f"{a.interest_margin:.2f}",
        "{{FLOATING_RATE_INDEX}}":    a.floating_rate,
        "{{TENOR}}":                  str(a.tenor_years),
        "{{DSCR_MINIMUM}}":           f"{a.dscr_target:.2f}",
        "{{DSCR_SCULPTING_TARGET}}":  f"{a.dscr_target + 0.05:.2f}",
        "{{LLCR_MINIMUM}}":           f"{a.llcr_minimum:.2f}",
        "{{GEARING_MAX}}":            f"{a.debt_percentage * 100:.0f}",
        "{{DSRA_MONTHS}}":            str(a.dsra_months),
        "{{CASH_SWEEP_PCT}}":         f"{a.cash_sweep_pct:.0f}",
        "{{GOVERNING_LAW}}":          a.governing_law,
        "{{JURISDICTION_COURTS}}":    a.jurisdiction_courts,
        "{{JURISDICTION}}":           a.jurisdiction_courts,
        "{{ACCOUNTING_STANDARD}}":    a.accounting_standard,
        "{{DEFAULT_MARGIN}}":         f"{a.default_margin:.0f}",
        "{{DISTRIBUTION_DSCR_TEST}}": f"{a.distribution_dscr:.2f}",
        "{{AVAILABILITY_END_DATE}}":  "[●]",
        "{{GOVERNING_LAW_CITY}}":     a.governing_law_city,
        "{{COD_DATE_OR_PLACEHOLDER}}": a.cod_date or "[●]",
        "{{PROJECT_DESCRIPTION}}":    a.project_description or "[PROJECT DESCRIPTION]",
        "{{ACCOUNT_BANK}}":           dsra_node.name if dsra_node else "[ACCOUNT BANK]",
        "{{ARRANGEMENT_FEE}}":        "[●]",
        "{{AGENCY_FEE}}":             "[●]",
        "{{COMMITMENT_FEE_PCT}}":     f"{a.commitment_fee_pct:.2f}",
        "{{DSRA_REPLENISHMENT_DAYS}}": "30",
        "{{MMRA_ANNUAL_CONTRIBUTION}}": "[●]",
        "{{CROSS_DEFAULT_THRESHOLD}}": "[●]",
        "{{ABANDONMENT_DAYS}}":       str(a.abandonment_days),
        "{{FORCE_MAJEURE_MONTHS}}":   str(a.force_majeure_months),
        "{{EQUITY_CURE_MAX}}":        str(a.equity_cure_max),
        "{{REPAYMENT_COMMENCEMENT}}": a.cod_date or "[●]",
        "{{PROJECT_DOCUMENTS_LIST}}": "PPA, EPC Contract, O&M Agreement, Concession Agreement",
        "{{EQUATOR_PRINCIPLES_IF_APPLICABLE}}": " and the Equator Principles (where applicable)",
    }

    result = template
    for key, val in vars_map.items():
        result = result.replace(key, str(val))
    return result


# ─── Clause Library — Facility Agreement (16 clauses, verbatim) ─────────────

FACILITY_AGREEMENT_CLAUSES: List[Clause] = [
    Clause(1, "DEFINITIONS AND INTERPRETATION",
        "In this Agreement, the following terms shall have the meanings set out below: "
        "'Availability Period' means the period from the date of this Agreement until {{AVAILABILITY_END_DATE}}; "
        "'Business Day' means a day on which banks are open for business in {{GOVERNING_LAW_CITY}}; "
        "'CFADS' means Cash Flow Available for Debt Service, being Revenues less Operating Costs less Taxes "
        "less Capital Expenditure less Changes in Working Capital in each period; "
        "'COD' or 'Commercial Operation Date' means {{COD_DATE_OR_PLACEHOLDER}}; "
        "'DSRA' means the Debt Service Reserve Account maintained with {{ACCOUNT_BANK}} in accordance with Clause 14; "
        "'DSCR' means the Debt Service Coverage Ratio, being the ratio of CFADS to Debt Service for the relevant period; "
        "'Finance Documents' means this Agreement, the Security Documents, the Accounts Agreement and any other "
        "document designated as such by the Agent; "
        "'Project' means {{PROJECT_DESCRIPTION}}; "
        "'Sponsors' means {{SPONSOR_NAMES}}."),
    Clause(2, "THE FACILITY",
        "2.1 The Lenders make available to the Borrower, on the terms and subject to the conditions of this Agreement, "
        "a term loan facility in an aggregate amount of {{CURRENCY}} {{FACILITY_AMOUNT}} (the 'Facility'). "
        "2.2 The Facility is available for the sole purpose of financing the {{PROJECT_DESCRIPTION}} (the 'Project'). "
        "2.3 The total capital cost of the Project is approximately {{TOTAL_EV}}, financed as follows: "
        "(a) Equity of {{CURRENCY}} {{EQUITY_AMOUNT}} ({{EQUITY_PCT}}%) to be contributed by {{SPONSOR_NAMES}}; and "
        "(b) Senior Debt of {{CURRENCY}} {{DEBT_AMOUNT}} ({{DEBT_PCT}}%) under this Facility."),
    Clause(3, "CONDITIONS PRECEDENT",
        "3.1 The obligations of the Lenders under this Agreement are subject to: "
        "(a) receipt of duly executed copies of each Finance Document; "
        "(b) evidence satisfactory to the Agent of all required governmental and regulatory consents and approvals; "
        "(c) receipt of legal opinions from counsel in {{JURISDICTION}} as to capacity, due execution and enforceability; "
        "(d) evidence of adequate insurance in accordance with the Insurance Schedule; "
        "(e) receipt of the Base Case Financial Model, reviewed and approved by the Independent Technical Adviser; "
        "(f) confirmation that the equity referred to in Clause 2.3(a) has been contributed in full to the Borrower."),
    Clause(4, "DRAWDOWN",
        "4.1 The Borrower may draw the Facility in tranches during the Availability Period by delivering a Drawdown Notice "
        "to the Agent not less than 5 Business Days prior to the proposed Drawdown Date. "
        "4.2 Each Drawdown Notice shall specify: (a) the proposed Drawdown Date; (b) the amount of the proposed advance; "
        "and (c) the purpose for which funds will be applied. "
        "4.3 The Lenders shall fund their respective pro-rata shares of each advance on the relevant Drawdown Date, "
        "subject to satisfaction of the conditions in Clause 3 and no Event of Default being outstanding."),
    Clause(5, "REPAYMENT",
        "5.1 The Borrower shall repay the Facility in accordance with the Repayment Schedule set out in Schedule [●], "
        "which is sculpted to maintain a DSCR of not less than {{DSCR_SCULPTING_TARGET}}x in each period. "
        "5.2 Repayment shall commence on the first Payment Date following {{REPAYMENT_COMMENCEMENT}}, being {{TENOR}} years from COD. "
        "5.3 Mandatory Prepayment: The Borrower shall apply the proceeds of any insurance recovery, asset disposal, "
        "or compensation event in prepayment of the Facility. "
        "5.4 Cash Sweep: {{CASH_SWEEP_PCT}}% of Excess Cash Flow (being CFADS less Scheduled Debt Service less DSRA "
        "top-up requirements) shall be applied in optional prepayment of the Facility."),
    Clause(6, "INTEREST",
        "6.1 The rate of interest on the Facility for each Interest Period is the aggregate of: "
        "(a) the Applicable Margin of {{MARGIN}}% per annum; and "
        "(b) {{FLOATING_RATE_INDEX}} for the relevant Interest Period. "
        "6.2 Interest shall be payable in arrear on each Payment Date. "
        "6.3 During the construction phase, interest shall be capitalised to the Facility and added to the outstanding "
        "balance (Interest During Construction, 'IDC'). "
        "6.4 Default Interest: If the Borrower fails to pay any amount when due, interest shall accrue at the rate of "
        "{{DEFAULT_MARGIN}}% per annum above the rate otherwise applicable."),
    Clause(7, "FEES",
        "7.1 Arrangement Fee: {{CURRENCY}} {{ARRANGEMENT_FEE}} payable by the Borrower to the MLA on Financial Close. "
        "7.2 Agency Fee: {{AGENCY_FEE}} per annum payable to the Agent, in advance on each anniversary of Financial Close. "
        "7.3 Commitment Fee: {{COMMITMENT_FEE_PCT}}% per annum on the undrawn and uncancelled amount of the Facility, "
        "accruing from Financial Close and payable quarterly."),
    Clause(8, "SECURITY",
        "8.1 The Borrower shall grant in favour of the Security Trustee (for the benefit of the Finance Parties) the "
        "following security: "
        "(a) a first-ranking fixed and floating charge over all present and future assets of the Borrower; "
        "(b) an assignment by way of security of all of the Borrower's rights, title and interest in and to the Project "
        "Documents (being the {{PROJECT_DOCUMENTS_LIST}}); "
        "(c) a pledge over all shares in the Borrower held by {{SPONSOR_NAMES}}; "
        "(d) an assignment of all Project Accounts; and "
        "(e) a deed of assignment over all insurance policies maintained in connection with the Project."),
    Clause(9, "FINANCIAL COVENANTS",
        "9.1 The Borrower shall ensure that: "
        "(a) the DSCR for each six-month calculation period ending on a Payment Date shall not be less than {{DSCR_MINIMUM}}x; "
        "(b) the LLCR calculated as at each Payment Date shall not be less than {{LLCR_MINIMUM}}x; "
        "(c) the ratio of Total Senior Debt to Total Project Cost shall not at any time exceed {{GEARING_MAX}}%; "
        "(d) the DSRA shall be funded to an amount equal to not less than {{DSRA_MONTHS}} months of projected Debt Service. "
        "9.2 The financial covenants shall be tested on each Payment Date by reference to a Compliance Certificate signed "
        "by an Authorised Signatory of the Borrower and delivered to the Agent within 30 days of each Payment Date. "
        "9.3 Equity Cure: In the event of a breach of Clause 9.1(a), the Sponsors may cure such breach by contributing "
        "additional equity to the Borrower within 20 Business Days, provided that such cure right may not be exercised "
        "more than {{EQUITY_CURE_MAX}} times during the life of the Facility."),
    Clause(10, "INFORMATION COVENANTS",
        "10.1 The Borrower shall deliver to the Agent: "
        "(a) within 120 days of each fiscal year end, audited financial statements of the Borrower prepared in accordance "
        "with {{ACCOUNTING_STANDARD}}; "
        "(b) within 45 days of each semi-annual period end, unaudited management accounts; "
        "(c) with each set of financial statements, a Compliance Certificate; "
        "(d) during construction, monthly progress reports from the Independent Technical Adviser; "
        "(e) promptly upon becoming aware, notice of any Material Adverse Effect, Force Majeure Event, dispute with any "
        "Project counterparty, or pending governmental action affecting the Project."),
    Clause(11, "POSITIVE COVENANTS",
        "11.1 The Borrower undertakes to: "
        "(a) carry out and complete the Project in accordance with the Project Documents and the Base Case Financial Model; "
        "(b) maintain all necessary governmental authorisations, licences and permits; "
        "(c) maintain adequate insurance in accordance with the Insurance Schedule; "
        "(d) maintain the Project in good working order and condition; "
        "(e) comply with all applicable laws, including Environmental and Social Standards{{EQUATOR_PRINCIPLES_IF_APPLICABLE}}; "
        "(f) maintain all Project Accounts in accordance with the Accounts Agreement."),
    Clause(12, "NEGATIVE COVENANTS",
        "12.1 Without the prior written consent of the Agent (acting on instructions of the Majority Lenders), the "
        "Borrower shall not: "
        "(a) incur any additional financial indebtedness other than Permitted Indebtedness; "
        "(b) create or permit to subsist any security over any of its assets other than Permitted Security; "
        "(c) make any distribution or payment to any Sponsor or equity holder unless the Restricted Payment Conditions "
        "are satisfied (being: no Default, DSCR > {{DISTRIBUTION_DSCR_TEST}}x, DSRA fully funded); "
        "(d) make any material amendment to any Project Document without Lender consent; "
        "(e) dispose of any material assets; "
        "(f) permit any change of control of the Borrower; "
        "(g) abandon or suspend Project operations for more than {{ABANDONMENT_DAYS}} consecutive days."),
    Clause(13, "EVENTS OF DEFAULT",
        "13.1 Each of the following events constitutes an Event of Default: "
        "(a) Non-Payment: the Borrower fails to pay any amount due within 3 Business Days of the due date; "
        "(b) Financial Covenant Breach: breach of any financial covenant in Clause 9, subject to cure provisions in Clause 9.3; "
        "(c) Other Covenant Breach: breach of any other covenant, uncured after 30 Business Days' notice; "
        "(d) Misrepresentation: any representation or warranty proves to be materially incorrect; "
        "(e) Insolvency: the Borrower or any Material Subsidiary is unable to pay its debts or commences insolvency proceedings; "
        "(f) Cross-Default: default by the Borrower on any other financial indebtedness exceeding {{CROSS_DEFAULT_THRESHOLD}}; "
        "(g) Project Document Termination: any Project Document is terminated, repudiated or becomes unenforceable; "
        "(h) Abandonment: the Project is abandoned for more than {{ABANDONMENT_DAYS}} days; "
        "(i) Expropriation or Nationalisation; "
        "(j) Material Adverse Effect; "
        "(k) Force Majeure lasting more than {{FORCE_MAJEURE_MONTHS}} months; "
        "(l) Loss of any material licence or permit."),
    Clause(14, "RESERVE ACCOUNTS",
        "14.1 Debt Service Reserve Account (DSRA): The Borrower shall maintain the DSRA with {{ACCOUNT_BANK}} and shall "
        "fund it to an amount equal to {{DSRA_MONTHS}} months of projected Debt Service on the first Funding Date. The "
        "DSRA shall be replenished after any withdrawal within {{DSRA_REPLENISHMENT_DAYS}} days. "
        "14.2 Major Maintenance Reserve Account (MMRA): The Borrower shall maintain the MMRA and contribute "
        "{{MMRA_ANNUAL_CONTRIBUTION}} per annum, representing the average annual cost of major maintenance as set out in "
        "the O&M Report. "
        "14.3 The Finance Parties shall have security over all Reserve Accounts by way of assignment pursuant to the "
        "Accounts Agreement. "
        "14.4 Withdrawals from any Reserve Account during the continuance of an Event of Default shall require the prior "
        "written consent of the Agent."),
    Clause(15, "GOVERNING LAW AND JURISDICTION",
        "15.1 This Agreement and any non-contractual obligations arising out of or in connection with it are governed "
        "by {{GOVERNING_LAW}}. "
        "15.2 Each Party irrevocably agrees that the courts of {{JURISDICTION_COURTS}} are to have non-exclusive "
        "jurisdiction to settle any dispute arising out of or in connection with this Agreement. "
        "15.3 Nothing in this Clause shall prevent any Finance Party from taking proceedings in any other court of "
        "competent jurisdiction."),
    Clause(16, "SCHEDULES",
        "Schedule 1 — Repayment Schedule (sculpted per DSCR target). "
        "Schedule 2 — Drawdown Notice Form. "
        "Schedule 3 — Compliance Certificate Form. "
        "Schedule 4 — Project Documents List. "
        "Schedule 5 — Insurance Requirements. "
        "Schedule 6 — Base Case Financial Model Key Parameters. "
        "Schedule 7 — Environmental and Social Management Plan Reference."),
]


# ─── Abbreviated clause libraries for other documents ───────────────────────

COMMON_TERMS_CLAUSES: List[Clause] = [
    Clause(1, "DEFINITIONS",
        "Definitions used in this Common Terms Agreement shall have the same meanings as in the Facility Agreement, "
        "save where the context requires otherwise."),
    Clause(2, "COMMON CONDITIONS PRECEDENT",
        "2.1 The conditions precedent set out in this Clause 2 are conditions precedent to all Financings provided to "
        "the Borrower under any Finance Document. (a) corporate authorisations of the Borrower; (b) executed Project "
        "Documents in agreed form; (c) confirmation of equity contribution; (d) legal opinions from {{JURISDICTION}} counsel."),
    Clause(3, "COMMON COVENANTS",
        "3.1 The Borrower shall comply with the financial, information, positive and negative covenants set out in "
        "Schedules 1 to 4 to this Agreement, which apply equally for the benefit of all Senior Lenders, MLAs and DFI Lenders."),
    Clause(4, "DECISION MAKING",
        "4.1 Decisions in respect of any waiver, amendment or consent under any Common Document shall be made by the "
        "Majority Lenders, save for Reserved Matters which require the consent of all Lenders. "
        "4.2 Reserved Matters include: (a) any reduction of principal, interest or fees; (b) any extension of any "
        "Repayment Date; (c) any release of security; (d) any amendment of this Clause 4."),
    Clause(5, "SHARING",
        "5.1 If any Finance Party receives or recovers any amount from the Borrower in respect of the Secured Obligations "
        "in excess of its pro rata share, such Finance Party shall promptly pay the excess to the Security Trustee for "
        "redistribution among the Finance Parties pro rata to their respective participations."),
]

INTERCREDITOR_CLAUSES: List[Clause] = [
    Clause(1, "RANKING AND PRIORITY",
        "1.1 The Senior Lenders rank pari passu among themselves. "
        "1.2 Any Subordinated Debt shall be subordinated in right of payment and security to the Senior Debt. "
        "1.3 The Sponsors agree that no payment of any kind shall be made on Sponsor Loans (if any) prior to the "
        "Discharge Date of all Senior Debt, save for Permitted Distributions."),
    Clause(2, "TURNOVER OBLIGATIONS",
        "2.1 If a Subordinated Creditor or Sponsor receives any payment in breach of this Agreement, such party shall "
        "hold such amount on trust for the Senior Lenders and immediately turn it over to the Security Trustee."),
    Clause(3, "WATERFALL",
        "3.1 All amounts received under or in connection with the Project shall be applied in accordance with the "
        "following priority: "
        "(a) first, in payment of operating costs of the Borrower; "
        "(b) second, in payment of taxes; "
        "(c) third, in payment of Senior Debt Service; "
        "(d) fourth, in funding the DSRA to the required level; "
        "(e) fifth, in funding the MMRA to the required level; "
        "(f) sixth, in payment of Subordinated Debt Service; "
        "(g) seventh, in distributions to Sponsors, subject to the Restricted Payment Conditions."),
    Clause(4, "VOTING",
        "4.1 Voting rights in respect of any decision under the Finance Documents shall be allocated pro rata to each "
        "Lender's outstanding commitment. "
        "4.2 The Majority Lenders means Lenders holding more than 66.7% of total commitments."),
    Clause(5, "ENFORCEMENT",
        "5.1 Following the occurrence of an Event of Default which is continuing, the Majority Lenders may instruct the "
        "Security Trustee to enforce the Security. All proceeds of enforcement shall be applied in accordance with the "
        "Waterfall in Clause 3."),
]

DIRECT_AGREEMENT_CLAUSES: List[Clause] = [
    Clause(1, "RECOGNITION OF SECURITY",
        "1.1 The Counterparty acknowledges and consents to the assignment by way of security of the Borrower's rights, "
        "title and interest in and to the Project Document in favour of the Security Trustee."),
    Clause(2, "STEP-IN RIGHTS",
        "2.1 If the Borrower defaults under the Project Document or an Event of Default occurs under the Finance "
        "Documents, the Security Trustee (acting on instructions of the Majority Lenders) may serve a Step-In Notice "
        "on the Counterparty. "
        "2.2 Following service of a Step-In Notice, the Security Trustee or its nominee shall assume all rights and "
        "obligations of the Borrower under the Project Document for the Step-In Period."),
    Clause(3, "CURE PERIODS",
        "3.1 Prior to terminating the Project Document, the Counterparty shall give the Security Trustee written notice "
        "of any default by the Borrower and shall allow the Security Trustee a Cure Period of not less than 30 days to "
        "remedy such default."),
    Clause(4, "NO TERMINATION",
        "4.1 The Counterparty agrees that it shall not terminate the Project Document for any reason without first "
        "complying with Clause 3 and giving the Security Trustee the opportunity to remedy any default or to procure "
        "a Substitute Borrower."),
    Clause(5, "GOVERNING LAW",
        "5.1 This Direct Agreement is governed by {{GOVERNING_LAW}}."),
]

SECURITY_TRUST_DEED_CLAUSES: List[Clause] = [
    Clause(1, "APPOINTMENT OF SECURITY TRUSTEE",
        "1.1 The Finance Parties hereby appoint the Security Trustee to hold the Security on trust for the Finance "
        "Parties on the terms set out in this Deed."),
    Clause(2, "SECURITY GRANTED",
        "2.1 The Borrower hereby grants in favour of the Security Trustee, for the benefit of the Finance Parties, the "
        "Security described in Schedule 1 hereto. "
        "2.2 The Security shall include: (a) a first-ranking fixed and floating charge over all assets of the Borrower; "
        "(b) an assignment of all Project Documents; (c) a pledge over all shares in the Borrower; (d) an assignment "
        "of all Project Accounts and insurance proceeds."),
    Clause(3, "TRUSTEE DUTIES",
        "3.1 The Security Trustee shall: "
        "(a) hold the Security on trust for the Finance Parties; "
        "(b) act in accordance with the instructions of the Majority Lenders; "
        "(c) not take any enforcement action without instructions from the Majority Lenders, save in cases of urgent "
        "necessity to preserve the Security."),
    Clause(4, "ENFORCEMENT",
        "4.1 Following an Event of Default, the Security Trustee shall enforce the Security in accordance with the "
        "instructions of the Majority Lenders. "
        "4.2 The Security Trustee may appoint a receiver, sell assets, or otherwise realise the Security."),
    Clause(5, "DISTRIBUTIONS",
        "5.1 All proceeds of enforcement shall be applied in accordance with the Waterfall set out in the Intercreditor "
        "Agreement (or, if none, in this Deed)."),
]

ACCOUNTS_AGREEMENT_CLAUSES: List[Clause] = [
    Clause(1, "PROJECT ACCOUNTS",
        "1.1 The Borrower shall maintain the following Project Accounts with {{ACCOUNT_BANK}}: "
        "(a) Operating Account; (b) Debt Service Reserve Account (DSRA); (c) Major Maintenance Reserve Account (MMRA); "
        "(d) Distribution Account; (e) Insurance and Compensation Account."),
    Clause(2, "OPERATING ACCOUNT",
        "2.1 All Project revenues shall be paid into the Operating Account. "
        "2.2 The Borrower may make withdrawals from the Operating Account to pay Operating Costs in the ordinary "
        "course of business."),
    Clause(3, "DSRA",
        "3.1 The DSRA shall at all times be funded to an amount equal to not less than {{DSRA_MONTHS}} months of "
        "projected Debt Service. "
        "3.2 Withdrawals from the DSRA may only be made to cover Debt Service shortfalls and must be replenished "
        "within {{DSRA_REPLENISHMENT_DAYS}} days."),
    Clause(4, "MMRA",
        "4.1 The Borrower shall contribute {{MMRA_ANNUAL_CONTRIBUTION}} per annum to the MMRA, equal to the average "
        "annual cost of major maintenance. "
        "4.2 Withdrawals may be made to fund scheduled major maintenance as set out in the O&M Report."),
    Clause(5, "DISTRIBUTION ACCOUNT",
        "5.1 Distributions to Sponsors shall be made via the Distribution Account, and only when the Restricted "
        "Payment Conditions are satisfied: (a) no Default; (b) DSCR > {{DISTRIBUTION_DSCR_TEST}}x; (c) DSRA fully funded; "
        "(d) MMRA fully funded."),
    Clause(6, "ACCOUNT SECURITY",
        "6.1 The Borrower hereby grants to the Security Trustee a first-ranking security over all Project Accounts. "
        "6.2 Following an Event of Default, the Security Trustee may take control of the Project Accounts and apply "
        "the balances in accordance with the Waterfall."),
]


CLAUSE_LIBRARY: Dict[str, List[Clause]] = {
    "Facility Agreement":                  FACILITY_AGREEMENT_CLAUSES,
    "Common Terms Agreement":              COMMON_TERMS_CLAUSES,
    "Intercreditor Agreement":             INTERCREDITOR_CLAUSES,
    "Direct Agreement — EPC Contractor":   DIRECT_AGREEMENT_CLAUSES,
    "Direct Agreement — O&M Operator":     DIRECT_AGREEMENT_CLAUSES,
    "Direct Agreement — Offtaker / PPA":   DIRECT_AGREEMENT_CLAUSES,
    "Direct Agreement — Concession / PPP": DIRECT_AGREEMENT_CLAUSES,
    "Security Trust Deed":                 SECURITY_TRUST_DEED_CLAUSES,
    "Accounts Agreement":                  ACCOUNTS_AGREEMENT_CLAUSES,
}


# ─── Markdown rendering ──────────────────────────────────────────────────────

def render_to_markdown(doc_type: str, parties: List[dict],
                       clauses: List[Clause], diagram: DiagramState,
                       a: PFAssumptions) -> str:
    """Assemble a contract document into legal-style markdown."""
    lines: List[str] = []

    # Title
    lines.append(f"# {doc_type.upper()}")
    lines.append("")
    if a.cod_date:
        lines.append(f"*Dated {a.cod_date}*")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Parties block
    lines.append("## PARTIES")
    lines.append("")
    if parties:
        for i, p in enumerate(parties, start=1):
            lines.append(f"({i}) **{p['name']}** (the '{p['role']}')")
            lines.append("")
    else:
        lines.append("*[No parties identified — add entities to the diagram]*")
        lines.append("")

    # Recitals
    lines.append("## RECITALS")
    lines.append("")
    lines.append(f"(A) The Borrower is undertaking the development, construction and operation of "
                 f"{a.project_description or '[the Project]'} (the 'Project').")
    lines.append("")
    lines.append(f"(B) The Borrower has requested the Lenders to provide financing in respect of the Project on "
                 f"the terms set out in this Agreement.")
    lines.append("")
    lines.append("(C) The Lenders have agreed to provide such financing on the terms and subject to the conditions "
                 "set out herein.")
    lines.append("")
    lines.append("**NOW THIS AGREEMENT WITNESSES** as follows:")
    lines.append("")

    # Clauses
    for cl in clauses:
        text = populate_clause(cl.text, diagram, a)
        lines.append(f"### {cl.number}. {cl.title}")
        lines.append("")
        lines.append(text)
        lines.append("")

    # Signature block
    lines.append("---")
    lines.append("")
    lines.append("**EXECUTED** as a deed by the parties hereto on the date first written above.")
    lines.append("")
    if parties:
        for p in parties:
            lines.append(f"_______________________________  ")
            lines.append(f"For and on behalf of **{p['name']}** ({p['role']})")
            lines.append("")

    return "\n".join(lines)


# ─── Main entry point ────────────────────────────────────────────────────────

def generate_minutes(diagram: DiagramState, assumptions: PFAssumptions) -> GeneratedMinutes:
    """Generate the full set of contract minutes from a diagram + assumptions."""
    flags = classify_diagram(diagram)
    doc_types = select_documents(flags)

    documents: List[ContractDocument] = []
    for doc_type in doc_types:
        parties = extract_parties(diagram.nodes, doc_type)
        clauses_template = CLAUSE_LIBRARY.get(doc_type, [])
        # Populate each clause's text
        filled_clauses = [
            Clause(cl.number, cl.title, populate_clause(cl.text, diagram, assumptions))
            for cl in clauses_template
        ]
        markdown = render_to_markdown(doc_type, parties, clauses_template, diagram, assumptions)
        documents.append(ContractDocument(
            type=doc_type,
            title=doc_type.upper(),
            parties=parties,
            clauses=filled_clauses,
            markdown=markdown,
        ))

    return GeneratedMinutes(
        project_name=diagram.project_name or assumptions.project_description or "Project",
        documents=documents,
        generated_at=datetime.datetime.now().isoformat(timespec="seconds"),
    )
