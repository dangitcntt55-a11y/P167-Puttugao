"""Build evidence package từ diagnosis results."""
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class EvidencePackage:
    """Evidence package cho 1 gap diagnosis."""
    hypotheses: list[dict] = field(default_factory=list)
    # [{hypothesis, confidence, evidence_urls, quote_span, claim_type}]
    recommended_actions: list[dict] = field(default_factory=list)
    # [{action_type, target_url, suggested_change, evidence_url}]
    severity: str = "medium"  # low | medium | high | critical
    requires_hitl: bool = False
    verified_at: datetime | None = None

    def to_dict(self) -> dict:
        return {
            "hypotheses": self.hypotheses,
            "recommended_actions": self.recommended_actions,
            "severity": self.severity,
            "requires_hitl": self.requires_hitl,
            "verified_at": self.verified_at.isoformat() if self.verified_at else None,
        }
