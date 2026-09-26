from dataclasses import dataclass


@dataclass
class RuleResult:
    rule: str
    score: int
    reason: str