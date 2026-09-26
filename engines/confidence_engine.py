from rules.class_rule import ClassRule
from rules.campus_rule import CampusRule
from rules.attendance_rule import AttendanceRule
from rules.time_rule import TimeRule


RULES = [
    ClassRule(),
    CampusRule(),
    AttendanceRule(),
    TimeRule()
]


def calculate_confidence(context):

    score = 0
    results = []

    for rule in RULES:

        result = rule.evaluate(context)

        score += result.score
        results.append(result)

    context.confidence.rule_results = results

    return min(score, 100)


def get_decision(score):

    if score >= 90:
        return "AUTO_LOG"

    elif score >= 60:
        return "ASK_USER"

    else:
        return "IGNORE"


def run(context):

    score = calculate_confidence(context)

    context.confidence.score = score
    context.confidence.decision = get_decision(score)

    return context