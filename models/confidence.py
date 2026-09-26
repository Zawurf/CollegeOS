from dataclasses import dataclass, field
from models.rule_result import RuleResult


@dataclass
class Confidence:
    score: int = 0
    decision: str = "IGNORE"
    rule_results: list[RuleResult] = field(default_factory=list)