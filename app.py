from engines.collegeos_runner import run_college_os


def tick():

    context = run_college_os(
        latitude=28.6057146,
        longitude=77.0385629
    )

    print(context.current_class)
    print(context.attendance)
    print(context.location)

    print("\nConfidence:")
    print(f"Score    : {context.confidence.score}")
    print(f"Decision : {context.confidence.decision}")

    print(context.notifications)


if __name__ == "__main__":
    tick()