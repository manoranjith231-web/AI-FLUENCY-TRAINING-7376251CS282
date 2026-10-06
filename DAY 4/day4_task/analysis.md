# Day 4 - Will It Fit, and May I Use It?

## 1. Scenario

I want to run an open-weight language model locally on my laptop.

My scenario is a small AI chatbot/coding assistant.

### Machine

- Device: My laptop
- Available memory: 8 GB
- Processor: [Enter your CPU]
- GPU: [Enter GPU or No dedicated GPU]
- Runtime: Ollama

### Purpose

The model will be used for:

- Learning
- Simple chatbot tasks
- Small coding questions
- Local experimentation

### Memory budget

My available memory budget is 8 GB.

### Licensing situation

I will verify the exact licence of each model from its official model card before deciding whether it can be used for my scenario.


# 2. Model Weights

Model weights are the parameters learned during model training.

The memory required for the weights mainly depends on:

1. Number of parameters
2. Precision or quantization

For example, a model with more parameters requires more memory.

Higher precision also requires more bytes per parameter.

My estimator calculates:

Weights = Number of Parameters × Bytes per Parameter

For my scenario, I tested different model sizes and quantization levels.

If model size is ignored, I may select a model that cannot fit into my machine's available memory.


# 3. Quantization

Quantization reduces the number of bits or bytes used to represent model weights.

For example:

- FP16 uses approximately 2 bytes per parameter
- Q8 uses approximately 1 byte
- Q4 uses approximately 0.5 bytes

Therefore, Q4 requires less memory than FP16.

The advantage is lower memory usage.

The trade-off is that lower precision can reduce model quality.

In my experiment, I kept the context length fixed and changed the quantization.

The results showed that the weight memory changed when the quantization changed.

I would choose a quantization that fits my machine while maintaining acceptable quality.


# 4. KV Cache and Context Length

The KV cache stores information from previous tokens during generation.

As context length increases, KV-cache memory also increases.

This means that a model that fits at a short context may not fit at a much longer context.

This is especially important for an AI agent because the conversation may contain:

- Previous messages
- Tool results
- Instructions
- Retrieved information

In my experiment, I kept the quantization fixed and changed the context length.

The weight memory remained approximately constant.

The KV cache increased as context increased.

Therefore, context length mainly affects the KV-cache portion of memory.


# 5. Memory Formula

My estimator separates memory into:

- Model weights
- KV cache
- Runtime overhead

The simplified calculation is:

Weights = Parameters × Bytes per Parameter

Total memory is estimated using:

Total = Weights + KV Cache + Runtime Overhead

This is an estimate rather than an exact prediction.

Actual memory can differ because of:

- Model architecture
- Runtime
- Context defaults
- Quantization implementation
- Hardware
- Runtime overhead


# 6. Model Card

A model card provides important information about a model.

I used the model card to check:

- Model name
- Parameter count
- Context length
- Licence
- Usage conditions
- Tool-calling support

The model card is important because model size alone does not determine whether I can legally use a model.


# 7. Open-Weight vs Open-Source

Open-weight and open-source are not necessarily the same thing.

An open-weight model may provide access to model weights while still having specific licence conditions.

Therefore, I need to check the exact licence before using or redistributing a model.

For my scenario, I checked:

- Licence name
- Commercial use
- Redistribution conditions
- Additional conditions


# 8. Memory Estimate Table

| Model | Params | Precision | Context | Weights GB | KV Cache GB | Total GB | Fits in 8 GB? |
|---|---:|---|---:|---:|---:|---:|---|
| Small Model Q4 | 1.5B | Q4 | 4K | | | | |
| Small Model Q4 | 1.5B | Q4 | 8K | | | | |
| Medium Model Q4 | 3B | Q4 | 4K | | | | |
| Medium Model Q4 | 3B | Q4 | 8K | | | | |


# 9. Model Comparison

| Basis | Model 1 | Model 2 | Model 3 |
|---|---|---|---|
| Full model name/version | | | |
| Publisher | | | |
| Total/active parameters | | | |
| MoE? | | | |
| Context window | | | |
| Exact licence | | | |
| Commercial use allowed? | | | |
| Extra conditions | | | |
| Tool calling stated? | | | |
| GGUF/Ollama available? | | | |
| Download size at Q4 | | | |
| Memory estimate | | | |
| Fits machine? | | | |
| Date checked | | | |


# 10. Context Length Experiment

I selected [MODEL NAME] at [QUANTIZATION].

| Context | Weights GB | KV Cache GB | Total GB | Fits? |
|---:|---:|---:|---:|---|
| 2K | | | | |
| 4K | | | | |
| 8K | | | | |
| 16K | | | | |

When the context length increased, the weight size stayed approximately constant.

The KV cache increased because more context tokens need to be stored.

The largest context that fits my machine at the selected quantization is [VALUE].


# 11. Quantization Experiment

I kept the context fixed at [VALUE]K.

| Quantization | Weights GB | KV Cache GB | Total GB | Fits? |
|---|---:|---:|---:|---|
| FP16 | | | | |
| Q8 | | | | |
| Q6 | | | | |
| Q5 | | | | |
| Q4 | | | | |
| Q3 | | | | |
| Q2 | | | | |

As quantization became smaller, the weight memory decreased.

The KV cache was not changed by the weight quantization in this simplified experiment.

I would use [QUANTIZATION] because it provides a suitable balance between memory usage and model quality.


# 12. Estimate vs Reality

I also checked a model running through Ollama.

### Ollama list

Model:

[MODEL]

Size shown:

[SIZE]


### Ollama ps

Model:

[MODEL]

Processor:

[CPU/GPU/SPLIT]

Memory:

[VALUE]


### Comparison

My estimated memory was approximately:

[VALUE] GB

The actual runtime memory was:

[VALUE] GB

The estimate was [close/not close].

The difference may be caused by:

- Runtime overhead
- Context size
- Quantization implementation
- Model architecture
- Ollama runtime behaviour


# 13. Suitability Analysis

For my scenario, I selected:

Model:

[MODEL NAME]

Parameters:

[PARAMETERS]

Quantization:

[QUANTIZATION]

Context:

[CONTEXT]

Licence:

[LICENCE]

The choice is based on the memory estimate, context requirement, actual Ollama observation and licence conditions.

The model needs to fit within my available memory while also satisfying the usage conditions of its licence.

### Runner-up

My runner-up is:

[MODEL NAME]

I considered it because:

[REASON]

I did not select it for my current scenario because:

[REASON]


# 14. What Could Change My Choice?

My choice could change if:

- I had more RAM
- I had a dedicated GPU
- I needed a longer context
- I needed stronger tool-calling support
- I needed commercial redistribution
- The model licence changed
- I needed higher model quality


# 15. Conclusion

Memory, quantization, context length and licence are all important when selecting an open model.

Memory is especially important when the available hardware is limited.

Quantization is useful when a model is too large at higher precision because it reduces weight memory.

Context length becomes important when an application needs long conversations or an agent stores many tool results.

Licence becomes the deciding factor when the model will be commercially distributed or used in a product.

Therefore, model selection should not be based only on parameter count or download size. The model's memory requirement, runtime behaviour, context requirement and exact licence all need to be checked before deployment.