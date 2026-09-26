from models.rule_result import RuleResult
from config import (
    CLASS_JUST_STARTED_SCORE,
    CLASS_IN_PROGRESS_SCORE,
    CLASS_FULLY_RUNNING_SCORE,
)
from datetime import datetime
from rules.base_rule import BaseRule



class ClassRule(BaseRule):

    name = "Class Rule"

    def evaluate(self, context):


        if context.current_class is None:
            return RuleResult(
                rule="Class Rule",
                score=0,
                reason="No class running"
            )

        start_time = datetime.strptime(
            context.current_class.start,
            "%H:%M"
        )

        current_time = datetime.strptime(
            context.current_time,
            "%H:%M"
        )

        minutes_since_start = (
            current_time - start_time
        ).total_seconds() / 60

        if minutes_since_start <= 5:
            score = CLASS_JUST_STARTED_SCORE
            reason = "Class just started"

        elif minutes_since_start <= 15:
            score = CLASS_IN_PROGRESS_SCORE
            reason = "Class in progress"

        else:
            score = CLASS_FULLY_RUNNING_SCORE
            reason = "Class well underway"

        return RuleResult(
            rule="Class Rule",
            score=score,
            reason=reason
        )