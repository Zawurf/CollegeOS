from models.rule_result import RuleResult
from config import INSIDE_CAMPUS_SCORE
from rules.base_rule import BaseRule


class CampusRule(BaseRule):

    name = "Campus Rule"

    def evaluate(self, context):

        if context.location.inside_campus:
            return RuleResult(
                rule="Campus Rule",
                score=INSIDE_CAMPUS_SCORE,
                reason="Inside campus"
            )

        return RuleResult(
            rule="Campus Rule",
            score=0,
            reason="Outside campus"
        )