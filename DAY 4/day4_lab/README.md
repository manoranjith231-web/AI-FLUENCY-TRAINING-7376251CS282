# Day 4 – Local Model Memory Estimator

## 📌 Project Overview

This project estimates how much memory a Large Language Model (LLM) needs to run locally and checks whether the model can fit within the available hardware memory.

The program automatically detects:

* Operating System
* Processor
* System RAM
* Dedicated GPU VRAM
* Memory type
* Recommended usable memory budget

It then estimates the memory requirements of different LLM sizes and quantization formats.

---

## 🎯 Objective

The main objective of this project is to understand:

1. How model size affects memory usage.
2. How quantization reduces memory requirements.
3. How context length affects KV-cache memory.
4. How hardware configuration affects local LLM compatibility.
5. Whether a model can comfortably run on a particular machine.

---

## ⚙️ Technologies Used

* Python 3
* `os`
* `platform`
* `subprocess`
* `ctypes`
* Optional `psutil`
* Windows system APIs
* `nvidia-smi`

---

## 🧠 Memory Estimation

The program uses approximate bytes-per-parameter values for different model precisions.

| Precision | Approx. Bytes / Parameter |
| --------- | ------------------------: |
| FP16      |                      2.00 |
| Q8_0      |                      1.00 |
| Q6_K      |                      0.81 |
| Q5_K_M    |                      0.68 |
| Q4_K_M    |                      0.57 |
| Q3_K_M    |                      0.43 |

The approximate model weight memory is calculated using:

```text
Weight Memory = Parameters × Bytes per Parameter
```

The program also estimates KV-cache memory based on:

```text
KV Cache = Parameters × Context Length × KV Cost
```

Finally, a 10% overhead is added for runtime memory, activations and fragmentation.

```text
Total Memory = (Weight Memory + KV Cache) × 1.10
```

---

## 🔍 Hardware Detection

### Windows

The program attempts to detect RAM using:

* Windows `GlobalMemoryStatusEx`
* WMIC fallback
* Optional `psutil`

Dedicated NVIDIA GPU memory can be detected using:

```text
nvidia-smi
```

### macOS

The program uses system information such as:

```text
sysconf
sysctl
```

Apple Silicon is treated as unified memory because CPU and GPU share the same memory pool.

### Linux

The program uses:

```text
os.sysconf()
```

and optionally `psutil`.

---

## 🤖 Models Tested

The program evaluates several example models:

```text
Qwen small                 1.5B
Granite / Qwen mid         8B
Mid at FP16                8B
Large local                30B
Server class               70B
```

It also compares an 8B model using different context lengths:

```text
4K
8K
32K
128K
```

and different quantization formats:

```text
Q3_K_M
Q4_K_M
Q5_K_M
Q8_0
FP16
```

---

## 📊 Compatibility Verdict

The program classifies models into three categories:

### Fits comfortably

The estimated memory is less than or equal to 70% of the available memory budget.

### Fits, but tight

The model fits within the available budget but leaves less safety margin.

### Does NOT fit

The estimated memory requirement is greater than the available memory budget.

---

## ▶️ How to Run

Open the project folder in VS Code.

Run:

```bash
python day4.py
```

The program will automatically detect your hardware and display the model compatibility results.

---

## 📁 Project Structure

```text
Day4/
│
├── day4.py
├── README.md
└── analysis.md
```

---

## 💡 Key Learning

This project demonstrates that running an LLM locally is not determined only by the number of parameters.

Memory requirements are also affected by:

* Quantization
* Context length
* KV cache
* Runtime overhead
* Available RAM
* GPU VRAM
* Hardware architecture

Therefore, selecting an appropriate model requires considering both **model requirements and available hardware resources**.

---

## ⚠️ Note

The memory calculations in this project are estimates rather than exact measurements.

Actual memory usage can vary depending on:

* Model architecture
* Runtime/framework
* Quantization implementation
* KV-cache precision
* Context length
* GPU offloading
* Operating system
* Other applications running on the machine
