"""
Day 4 - Open LLM Memory Estimator

Estimates:
1. Model weights
2. KV cache
3. Runtime overhead
4. Total memory
5. Whether the model fits in available memory
"""

import math


# Approximate bytes per parameter
BYTES_PER_PARAMETER = {
    "FP32": 4.0,
    "FP16": 2.0,
    "BF16": 2.0,
    "Q8": 1.0,
    "Q6": 0.75,
    "Q5": 0.625,
    "Q4": 0.5,
    "Q3": 0.375,
    "Q2": 0.25
}


def calculate_weights(params_billion, precision):
    """
    Calculate model weight memory.
    """

    if precision not in BYTES_PER_PARAMETER:
        raise ValueError("Invalid precision")

    bytes_per_parameter = BYTES_PER_PARAMETER[precision]

    parameters = params_billion * 1_000_000_000

    weight_bytes = parameters * bytes_per_parameter

    weight_gb = weight_bytes / (1024 ** 3)

    return weight_gb


def calculate_kv_cache(
    params_billion,
    context_k,
    kv_bytes_per_token=0.25
):
    """
    Approximate KV cache.

    This is a simplified estimate for comparison.
    Real KV cache depends on model architecture,
    number of layers, attention heads and KV heads.
    """

    context_tokens = context_k * 1024

    kv_bytes = (
        context_tokens
        * params_billion
        * kv_bytes_per_token
    )

    kv_gb = kv_bytes / (1024 ** 3)

    return kv_gb


def calculate_total(weights_gb, kv_gb, overhead_percent=15):
    """
    Calculate total estimated memory.
    """

    subtotal = weights_gb + kv_gb

    overhead = subtotal * (overhead_percent / 100)

    total = subtotal + overhead

    return total


def estimate_model(
    model_name,
    params_billion,
    precision,
    context_k,
    memory_budget_gb
):
    """
    Complete model memory estimation.
    """

    weights = calculate_weights(
        params_billion,
        precision
    )

    kv_cache = calculate_kv_cache(
        params_billion,
        context_k
    )

    total = calculate_total(
        weights,
        kv_cache
    )

    fits = total <= memory_budget_gb

    return {
        "model": model_name,
        "params": params_billion,
        "precision": precision,
        "context": context_k,
        "weights": weights,
        "kv_cache": kv_cache,
        "total": total,
        "memory_budget": memory_budget_gb,
        "fits": fits
    }


def print_result(result):

    print("\n" + "=" * 60)
    print("OPEN LLM MEMORY ESTIMATION")
    print("=" * 60)

    print(f"Model          : {result['model']}")
    print(f"Parameters     : {result['params']} B")
    print(f"Precision      : {result['precision']}")
    print(f"Context        : {result['context']} K")

    print("-" * 60)

    print(f"Weights        : {result['weights']:.2f} GB")
    print(f"KV Cache       : {result['kv_cache']:.2f} GB")
    print(f"Total Memory   : {result['total']:.2f} GB")

    print("-" * 60)

    print(f"Memory Budget  : {result['memory_budget']} GB")

    if result["fits"]:
        print("FIT VERDICT    : YES")
    else:
        print("FIT VERDICT    : NO")

    print("=" * 60)


def main():

    # Scenario
    memory_budget = 8

    models = [
        ("Small Model Q4", 1.5, "Q4", 4),
        ("Small Model Q4", 1.5, "Q4", 8),
        ("Medium Model Q4", 3.0, "Q4", 4),
        ("Medium Model Q4", 3.0, "Q4", 8)
    ]

    print("\nDAY 4 - MODEL MEMORY ESTIMATOR")
    print(f"Available memory: {memory_budget} GB")

    for model_name, params, precision, context in models:

        result = estimate_model(
            model_name,
            params,
            precision,
            context,
            memory_budget
        )

        print_result(result)


if __name__ == "__main__":
    main()