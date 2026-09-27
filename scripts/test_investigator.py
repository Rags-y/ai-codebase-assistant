from src.retrieval.investigator import CodeInvestigator


investigator = CodeInvestigator()


queries = [
    "Which functions use the Task model?",
    "What does create_task use?",
    "How are tasks created and what validates the input?",
]


print("\n")
print("=" * 80)
print("CODE INVESTIGATION")
print("=" * 80)


for query in queries:

    print("\n")
    print(f"Query: {query}")
    print()

    direction = investigator.detect_direction(query)

    print(f"Detected direction: {direction}")
    print()

    results = investigator.investigate(
        query,
        max_hops=1,
    )

    if not results:
        print("No graph relationships found.")
        continue

    for index, result in enumerate(results, start=1):

        chunk = result["chunk"]

        print(
            f"{index}. "
            f"{chunk['name']} "
            f"({chunk['path']})"
        )

        print(
            f"Entity: {result['entity']}"
        )

        print(
            f"Direction: {result['direction']}"
        )

        print(
            f"Relationship: {result['relationship']}"
        )

        print(
            f"Hop: {result['hop']}"
        )

        print(
            f"Lines: "
            f"{chunk['start_line']}-"
            f"{chunk['end_line']}"
        )