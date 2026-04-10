# ─────────────────────────────────────────────────────────────────────────────
# pf_models.py — Project Finance data models for SPE Diagram + Contract Minutes
# Pure Python dataclasses (no Pydantic dependency)
# ─────────────────────────────────────────────────────────────────────────────
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List, Dict


# ─── Enumerations ────────────────────────────────────────────────────────────

class EntityType(str, Enum):
    SPV       = "spv"
    SPONSOR   = "sponsor"
    LENDER    = "lender"
    MLA       = "mla"
    DFI       = "dfi"
    OFFTAKER  = "offtaker"
    EPC       = "epc"
    OM        = "om"
    GOVT      = "govt"
    INSURANCE = "insurance"
    DSRA      = "dsra"
    CUSTOM    = "custom"


class FlowType(str, Enum):
    EQUITY   = "equity"
    DEBT     = "debt"
    REVENUE  = "revenue"
    PAYMENT  = "payment"
    SERVICE  = "service"
    SECURITY = "security"
    CUSTOM   = "custom"


# ─── Entity colour palette (matches design system) ──────────────────────────
ENTITY_COLORS: Dict[str, str] = {
    "spv":       "#3b82f6",
    "sponsor":   "#8b5cf6",
    "lender":    "#10b981",
    "mla":       "#a78bfa",
    "dfi":       "#34d399",
    "offtaker":  "#f59e0b",
    "epc":       "#ef4444",
    "om":        "#06b6d4",
    "govt":      "#f97316",
    "insurance": "#ec4899",
    "dsra":      "#14b8a6",
    "custom":    "#94a3b8",
}

ENTITY_LABELS: Dict[str, str] = {
    "spv":       "SPV / Project Co.",
    "sponsor":   "Sponsor (Equity)",
    "lender":    "Senior Lender",
    "mla":       "MLA / Arranger",
    "dfi":       "DFI / MDB / IFC",
    "offtaker":  "Offtaker / PPA",
    "epc":       "EPC Contractor",
    "om":        "O&M Operator",
    "govt":      "Government / PPP",
    "insurance": "Insurance Co.",
    "dsra":      "DSRA / Reserve",
    "custom":    "Custom Entity",
}

ENTITY_ICONS: Dict[str, str] = {
    "spv":       "🏗️",
    "sponsor":   "🏦",
    "lender":    "💰",
    "mla":       "📋",
    "dfi":       "🌍",
    "offtaker":  "⚡",
    "epc":       "🔧",
    "om":        "⚙️",
    "govt":      "🏛️",
    "insurance": "🛡️",
    "dsra":      "🔒",
    "custom":    "📦",
}

FLOW_COLORS: Dict[str, str] = {
    "equity":   "#8b5cf6",
    "debt":     "#10b981",
    "revenue":  "#f59e0b",
    "payment":  "#f59e0b",
    "service":  "#06b6d4",
    "security": "#f87171",
    "custom":   "#94a3b8",
}

FLOW_LABELS: Dict[str, str] = {
    "equity":   "Equity Contribution",
    "debt":     "Debt / Loan Drawdown",
    "revenue":  "Revenue / Offtake",
    "payment":  "Fee / Service Payment",
    "service":  "Service / Operational",
    "security": "Security / Charge",
    "custom":   "Custom Flow",
}


# ─── Data classes ────────────────────────────────────────────────────────────

@dataclass
class DiagramNode:
    """A node (entity) on the SPE diagram."""
    id: str
    type: str  # EntityType value
    name: str
    sub: str = ""
    color: str = "#94a3b8"

    def __post_init__(self):
        if not self.color or self.color == "#94a3b8":
            self.color = ENTITY_COLORS.get(self.type, "#94a3b8")
        if not self.sub:
            self.sub = ENTITY_LABELS.get(self.type, "Entity")


@dataclass
class DiagramEdge:
    """A flow (edge) connecting two nodes on the SPE diagram."""
    id: str
    from_node: str  # node id
    to_node: str    # node id
    flow_type: str  # FlowType value
    label: str = ""
    amount: Optional[str] = None
    notes: Optional[str] = None

    def __post_init__(self):
        if not self.label:
            self.label = FLOW_LABELS.get(self.flow_type, "Flow")


@dataclass
class DiagramState:
    """Complete SPE diagram: metadata + nodes + edges."""
    project_name: str = ""
    currency:     str = "USD"
    total_ev:     float = 0.0
    closing_date: str = ""
    nodes: List[DiagramNode] = field(default_factory=list)
    edges: List[DiagramEdge] = field(default_factory=list)


@dataclass
class PFAssumptions:
    """Project Finance assumptions used to populate contract clauses."""
    total_ev:            float = 100_000_000
    debt_percentage:     float = 0.70
    interest_margin:     float = 2.0          # in % (e.g. 2.0 = SOFR+200bps)
    floating_rate:       str   = "SOFR"
    tenor_years:         int   = 15
    dscr_target:         float = 1.25
    dsra_months:         int   = 6
    governing_law:       str   = "English law"
    currency:            str   = "USD"
    project_description: str   = ""
    cod_date:            str   = ""
    distribution_dscr:   float = 1.15
    cash_sweep_pct:      float = 100.0        # in %
    llcr_minimum:        float = 1.15
    jurisdiction_courts: str   = "England and Wales"
    governing_law_city:  str   = "London"
    accounting_standard: str   = "IFRS"
    default_margin:      float = 2.0
    abandonment_days:    int   = 90
    force_majeure_months: int  = 6
    equity_cure_max:     int   = 2
    commitment_fee_pct:  float = 0.50


@dataclass
class Clause:
    """A single contract clause."""
    number: int
    title:  str
    text:   str  # template with {{VARIABLES}} or already populated


@dataclass
class ContractDocument:
    """A complete contract document with parties + clauses + rendered markdown."""
    type:     str           # e.g. "Facility Agreement"
    title:    str
    parties:  List[Dict]    # [{"name": ..., "role": ..., "type": ...}, ...]
    clauses:  List[Clause]
    markdown: str = ""


@dataclass
class GeneratedMinutes:
    """The full set of contract documents generated from a diagram + assumptions."""
    project_name: str
    documents:    List[ContractDocument]
    generated_at: str = ""
