"""
Day 4 - Context Length and Quantization Experiment
"""

from estimator import estimate_model


MODEL_NAME = "Qwen 2.5 1.5B"

PARAMETERS = 1.5

MEMORY_BUDGET = 8


def context_experiment():

    print("\n")
    print("=" * 75)
    print("CONTEXT LENGTH EXPERIMENT")
    print("=" * 75)

    precision = "Q4"

    contexts = [2, 4, 8, 16]

    print(
        f"{'Context(K)':<15}"
        f"{'Weights(GB)':<15}"
        f"{'KV Cache(GB)':<15}"
        f"{'Total(GB)':<15}"
        f"{'Fits?':<10}"
    )

    print("-" * 75)

    for context in contexts:

        result = estimate_model(
            MODEL_NAME,
            PARAMETERS,
            precision,
            context,
            MEMORY_BUDGET
        )

        print(
            f"{context:<15}"
            f"{result['weights']:<15.2f}"
            f"{result['kv_cache']:<15.2f}"
            f"{result['total']:<15.2f}"
            f"{'YES' if result['fits'] else 'NO':<10}"
        )


def quantization_experiment():

    print("\n")
    print("=" * 75)
    print("QUANTIZATION EXPERIMENT")
    print("=" * 75)

    context = 8

    quantizations = [
        "FP16",
        "Q8",
        "Q6",
        "Q5",
        "Q4",
        "Q3",
        "Q2"
    ]

    print(
        f"{'Quantization':<15}"
        f"{'Weights(GB)':<15}"
        f"{'KV Cache(GB)':<15}"
        f"{'Total(GB)':<15}"
        f"{'Fits?':<10}"
    )

    print("-" * 75)

    for precision in quantizations:

        result = estimate_model(
            MODEL_NAME,
            PARAMETERS,
            precision,
            context,
            MEMORY_BUDGET
        )

        print(
            f"{precision:<15}"
            f"{result['weights']:<15.2f}"
            f"{result['kv_cache']:<15.2f}"
            f"{result['total']:<15.2f}"
            f"{'YES' if result['fits'] else 'NO':<10}"
        )


def main():

    context_experiment()

    quantization_experiment()


if __name__ == "__main__":
    main()