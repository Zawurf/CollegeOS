from datetime import datetime

from models.rule_result import RuleResult
from rules.base_rule import BaseRule

from config import (
    NEXT_CLASS_SOON_SCORE,
    NEXT_CLASS_NEAR_SCORE,
    NEXT_CLASS_IMMINENT_SCORE
)


class TimeRule(BaseRule):

    name = "Time Rule"

    def evaluate(self, context):

        if context.next_class is None:
            return RuleResult(
                rule="Time Rule",
                score=0,
                reason="No more classes today"
            )

        current = datetime.strptime(
            context.current_time,
            "%H:%M"
        )

        next_start = datetime.strptime(
            context.next_class.start,
            "%H:%M"
        )

        minutes = (next_start - current).total_seconds() / 60

        if minutes <= 5:
            score = NEXT_CLASS_IMMINENT_SCORE
            reason = "Next class starts in less than 5 minutes"

        elif minutes <= 15:
            score = NEXT_CLASS_NEAR_SCORE
            reason = "Next class starts soon"

        elif minutes <= 30:
            score = NEXT_CLASS_SOON_SCORE
            reason = "Next class is within 30 minutes"

        else:
            score = 0
            reason = "Next class is far away"

        return RuleResult(
            rule="Time Rule",
            score=score,
            reason=reason
        )