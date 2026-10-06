# Day 4 – Model Memory Analysis

## 1. Introduction

Large Language Models can contain millions or billions of parameters. Running these models locally requires sufficient memory for the model weights, KV cache, runtime operations and other overhead.

The purpose of this experiment is to estimate the memory required by different model sizes and determine whether they can run within the available hardware memory.

---

## 2. Model Parameters and Memory

A model with more parameters generally requires more memory.

For example, an 8B model contains approximately:

```text
8 billion parameters
```

However, the actual memory requirement depends heavily on the numerical precision used to store the parameters.

The project uses the following approximate values:

| Precision | Bytes / Parameter |
| --------- | ----------------: |
| FP16      |              2.00 |
| Q8_0      |              1.00 |
| Q6_K      |              0.81 |
| Q5_K_M    |              0.68 |
| Q4_K_M    |              0.57 |
| Q3_K_M    |              0.43 |

Therefore, quantization can significantly reduce the memory required by a model.

---

## 3. Effect of Quantization

Consider an 8B model.

### FP16

```text
8 × 2.00 = 16 GB
```

Approximately 16 GB is required just for the model weights.

### Q4_K_M

```text
8 × 0.57 = 4.56 GB
```

The approximate weight requirement is only 4.56 GB.

This shows why quantized models are useful for local AI applications.

Instead of requiring approximately 16 GB for FP16 weights, a Q4_K_M version requires approximately 4.56 GB before KV cache and other overhead are included.

---

## 4. Effect of Context Length

Context length determines how much text the model can process at once.

A larger context requires more KV-cache memory.

The experiment tests:

```text
4K
8K
32K
128K
```

For the same 8B Q4_K_M model, increasing the context length increases the estimated KV-cache requirement.

Using the project's approximation:

```text
KV Memory = Parameters × Context × 0.02
```

For an 8B model with 8K context:

```text
8 × 8 × 0.02
= 1.28 GB
```

Therefore, context length is an important factor when estimating local model memory.

---

## 5. Runtime Overhead

The project adds a 10% overhead:

```python
OVERHEAD = 1.10
```

This accounts approximately for:

* Runtime memory
* Activations
* Memory fragmentation
* Other inference-related requirements

The final estimate is:

```text
Total Memory =
(Weight Memory + KV Cache) × 1.10
```

This provides a safer estimate than considering model weights alone.

---

## 6. Hardware Detection

The program automatically detects the available hardware.

It checks:

```text
Operating System
Processor
System RAM
GPU VRAM
Memory Type
```

On Windows, it attempts to use the Windows memory API and WMIC as fallbacks.

For NVIDIA GPUs, the program attempts to use:

```text
nvidia-smi
```

On macOS, Apple Silicon is treated differently because CPU and GPU use unified memory.

---

## 7. Memory Budget

The program does not assume that 100% of system memory can be used by the model.

For Apple Silicon:

```text
Usable Memory ≈ 75% of System RAM
```

For CPU-based Windows/Linux inference:

```text
Usable Memory ≈ 70% of System RAM
```

For dedicated GPUs:

```text
Usable VRAM ≈ 90% of GPU VRAM
```

The remaining memory is reserved for the operating system, drivers and other applications.

---

## 8. Model Compatibility

The experiment evaluates models ranging from approximately 1.5B to 70B parameters.

The tested models include:

```text
1.5B Q4_K_M
8B Q4_K_M
8B FP16
30B Q4_K_M
70B Q4_K_M
```

The program classifies each model based on its estimated memory requirement.

### Classification

```text
≤ 70% of available memory
        ↓
Fits comfortably

≤ 100% of available memory
        ↓
Fits, but tight

> 100% of available memory
        ↓
Does NOT fit
```

---

## 9. Important Observations

### Observation 1 – Model size matters

Increasing the number of parameters increases the memory required for model weights.

A 70B model requires substantially more memory than a 1.5B model.

---

### Observation 2 – Quantization reduces memory

Quantized formats such as Q4_K_M require considerably less memory than FP16.

This makes quantized models more practical for local inference.

---

### Observation 3 – Context length matters

Even when the model weights remain unchanged, increasing the context length increases KV-cache memory.

Therefore, a model that fits at 4K context may require significantly more memory at 32K or 128K context.

---

### Observation 4 – Hardware affects model selection

A model that fits on a high-memory machine may not fit on a machine with limited RAM or VRAM.

Therefore, hardware detection is an important part of local LLM deployment.

---

## 10. Limitations

This project provides an estimation rather than an exact measurement.

Actual memory usage can differ because of:

1. Model architecture.
2. Different KV-cache implementations.
3. Quantization format.
4. Inference framework.
5. GPU offloading.
6. Operating system memory usage.
7. Runtime implementation.
8. Number of active applications.
9. Actual context usage.

The KV-cache formula used in this project is a rough approximation and should not be treated as a universal value for every LLM.

---

## 11. Conclusion

This experiment demonstrates the main factors involved in running LLMs locally.

The most important factors are:

```text
Model Parameters
        +
Quantization
        +
Context Length
        +
KV Cache
        +
Runtime Overhead
        +
Available Hardware Memory
```

A smaller quantized model can often be practical on consumer hardware, while larger models may require substantially more memory or specialized hardware.

The experiment provides a simple way to estimate model requirements before attempting local deployment.

---

## 12. Key Takeaway

> **Choosing a local LLM is not only about model size. It is about matching model size, quantization, context length and runtime requirements with the available hardware memory.**
