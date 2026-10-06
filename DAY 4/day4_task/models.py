"""
Model information used for Day 4 comparison.

IMPORTANT:
Verify these details from the official model card
and Ollama library page before putting them into analysis.md.
"""

models = [

    {
        "name": "Qwen2.5 1.5B",
        "family": "Qwen",
        "publisher": "Qwen",
        "parameters": "1.54B",
        "license": "Apache-2.0",
        "tool_calling": "Check official model card",
    },

    {
        "name": "Llama 3.2 3B",
        "family": "Llama",
        "publisher": "Meta",
        "parameters": "3B",
        "license": "Check official model card",
        "tool_calling": "Check official model card",
    },

    {
        "name": "Gemma 3 1B",
        "family": "Gemma",
        "publisher": "Google",
        "parameters": "1B",
        "license": "Check official model card",
        "tool_calling": "Check official model card",
    }

]


def show_models():

    print("\nMODEL COMPARISON")
    print("=" * 70)

    for model in models:

        print(f"\nModel       : {model['name']}")
        print(f"Family      : {model['family']}")
        print(f"Publisher   : {model['publisher']}")
        print(f"Parameters  : {model['parameters']}")
        print(f"License     : {model['license']}")
        print(f"Tool Calling: {model['tool_calling']}")


if __name__ == "__main__":
    show_models()