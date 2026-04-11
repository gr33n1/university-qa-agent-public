from pprint import pprint
from uuid import uuid4

from dotenv import load_dotenv

from app.graph import build_graph


def main() -> None:
    load_dotenv()
    graph = build_graph()

    question = input("Ask a question about the university database: ").strip()
    debug_input = input("Show debug output? (y/n): ").strip().lower()
    debug = debug_input == "y"

    initial_state = {
        "question": question,
        "trace": [],
        "repair_attempts": 0,
        "max_repair_attempts": 1,
        "request_id": str(uuid4()),
    }

    result = graph.invoke(initial_state)

    print("\nFinal answer:")
    print(result.get("final_answer", ""))

    if debug:
        print("\nRequest ID:")
        print(result.get("request_id", ""))

        print("\nGenerated SQL:")
        print(result.get("generated_sql", ""))

        print("\nValidated SQL:")
        print(result.get("validated_sql", ""))

        if result.get("error"):
            print("\nError:")
            print(result["error"])

        print("\nTrace:")
        pprint(result.get("trace", []))


if __name__ == "__main__":
    main()