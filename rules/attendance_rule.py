from models.rule_result import RuleResult
from config import LOW_ATTENDANCE_SCORE
from rules.base_rule import BaseRule


class AttendanceRule(BaseRule):

    name = "Attendance Rule"

    def evaluate(self, context):

        attendance = context.attendance.percentage

        if attendance is not None and attendance < 67:
            return RuleResult(
                rule="Attendance Rule",
                score=LOW_ATTENDANCE_SCORE,
                reason="Attendance below minimum"
            )

        return RuleResult(
            rule="Attendance Rule",
            score=0,
            reason="Attendance is safe"
        )