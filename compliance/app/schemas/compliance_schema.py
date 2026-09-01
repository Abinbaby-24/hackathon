from typing import Any, Dict, List


class ComplianceResult:
    """
    Standard structure returned by the compliance engine.
    """

    def __init__(
        self,
        status: str,
        score: float,
        checks: Dict[str, Any],
        violations: List[Dict[str, str]]
    ):
        self.status = status
        self.score = score
        self.checks = checks
        self.violations = violations

    def to_dict(self):
        return {
            "status": self.status,
            "score": self.score,
            "checks": self.checks,
            "violations": self.violations
        }