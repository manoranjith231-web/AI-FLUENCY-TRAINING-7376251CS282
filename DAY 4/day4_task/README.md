# Day 4 – Will It Fit, and May I Use It?

## 📌 Project Overview

This project is part of **Agentic AI: Foundations and Open-Source Practice – Day 4**.

The project focuses on understanding how to evaluate an open-weight language model before running it locally.

The main goal is to determine:

* Whether a model fits within the available memory
* How model parameters affect memory usage
* How quantization reduces memory requirements
* How context length affects KV cache memory
* How actual Ollama memory usage compares with an estimate
* How model licences affect whether a model can be used in a particular scenario

---

## 🎯 Aim

The aim of this project is to estimate the memory required by open language models and compare different model configurations.

The estimator calculates:

```text
Model Weights
      +
KV Cache
      +
Runtime Overhead
      =
Estimated Total Memory
```

The result is then compared with the available memory to determine whether the model is likely to fit.

---

## 💻 Scenario

### Machine

* **Device:** Laptop
* **Memory Budget:** 8 GB
* **Runtime:** Ollama
* **Purpose:** Local AI chatbot / coding assistant
* **Users:** Individual learning and experimentation

The memory budget can be changed in the Python estimator according to the machine being used.

---

## 🧠 Concepts Covered

### 1. Model Weights

Model weights are the parameters learned during model training.

The approximate memory required for weights depends on:

* Number of parameters
* Precision / quantization

The estimator uses:

```text
Weights = Parameters × Bytes per Parameter
```

---

### 2. Quantization

Quantization reduces the number of bytes required to represent model weights.

The project compares different precision levels such as:

```text
FP16
Q8
Q6
Q5
Q4
Q3
Q2
```

Lower-bit quantization generally requires less memory, but may involve a quality trade-off.

---

### 3. KV Cache

The KV cache stores information from previously processed tokens.

Its memory requirement increases as the context length increases.

This is particularly important for applications such as agents that continuously collect:

* Conversation history
* Tool results
* Retrieved information
* Previous instructions

---

### 4. Context Length

Context length determines how many tokens the model can consider during processing.

This project tests multiple context lengths while keeping the quantization fixed.

Example:

```text
2K
4K
8K
16K
```

The experiment demonstrates how increasing context affects KV-cache memory.

---

### 5. Model Cards

Model cards provide information about a model, including:

* Model name
* Parameters
* Context window
* Licence
* Usage conditions
* Tool-calling support

The model cards are used as part of the model comparison.

---

### 6. Open-Weight vs Open-Source

An open-weight model is not automatically the same as an open-source software project.

The exact licence and its conditions determine how the model can be:

* Used
* Modified
* Distributed
* Used commercially

Therefore, licence information is checked separately from memory requirements.

---

# 📂 Project Structure

```text
DAY4_OPEN_LLM_MEMORY/
│
├── screenshots/
│   ├── estimator_output.png
│   ├── context_output.png
│   ├── quantization_output.png
│   ├── ollama_list.png
│   ├── ollama_ps.png
│   ├── model_card_1.png
│   ├── model_card_2.png
│   └── model_card_3.png
│
├── estimator.py
├── context_quantization.py
├── ollama_check.py
├── models.py
├── requirements.txt
├── .gitignore
├── README.md
└── analysis.md
```

---

# 🐍 Python Files

## `estimator.py`

The main memory estimation program.

It calculates:

* Model weights
* KV cache
* Runtime overhead
* Total estimated memory
* Fit / no-fit verdict

Run:

```bash
python estimator.py
```

---

## `context_quantization.py`

Runs two experiments:

### Context Experiment

Changes:

```text
2K → 4K → 8K → 16K
```

while keeping quantization fixed.

### Quantization Experiment

Changes:

```text
FP16 → Q8 → Q6 → Q5 → Q4 → Q3 → Q2
```

while keeping context fixed.

Run:

```bash
python context_quantization.py
```

---

## `ollama_check.py`

Checks installed and currently running Ollama models.

It collects information from:

```bash
ollama list
```

and:

```bash
ollama ps
```

Run:

```bash
python ollama_check.py
```

---

## `models.py`

Contains the model information used for the model comparison section.

The licence and model-card information should be verified from the official sources before final submission.

---

# 📊 Memory Estimation

The estimator separates memory into three main parts:

```text
Weights
   +
KV Cache
   +
Runtime Overhead
   =
Total Estimated Memory
```

The result is compared with the available memory.

Example:

```text
Available Memory : 8 GB
Estimated Total  : X GB
Fit Verdict      : YES / NO
```

The estimate is intended for deciding whether a model is likely to fit. Actual runtime memory can differ because of architecture, runtime configuration, quantization implementation and other overhead.

---

# 🔬 Experiments

## Experiment 1 – Context Length

The same model and quantization are used while changing context length.

| Context | Weights | KV Cache | Total | Fits? |
| ------- | ------: | -------: | ----: | ----- |
| 2K      |       - |        - |     - | -     |
| 4K      |       - |        - |     - | -     |
| 8K      |       - |        - |     - | -     |
| 16K     |       - |        - |     - | -     |

The results are recorded in `analysis.md`.

---

## Experiment 2 – Quantization

The same model and context are used while changing quantization.

| Quantization | Weights | KV Cache | Total | Fits? |
| ------------ | ------: | -------: | ----: | ----- |
| FP16         |       - |        - |     - | -     |
| Q8           |       - |        - |     - | -     |
| Q6           |       - |        - |     - | -     |
| Q5           |       - |        - |     - | -     |
| Q4           |       - |        - |     - | -     |
| Q3           |       - |        - |     - | -     |
| Q2           |       - |        - |     - | -     |

The results are recorded in `analysis.md`.

---

# 🦙 Ollama Verification

The project compares the estimated memory with a model actually running through Ollama.

Commands used:

```bash
ollama list
```

```bash
ollama ps
```

The screenshots are stored in:

```text
screenshots/
```

The difference between estimated and actual memory is discussed in `analysis.md`.

---

# 📸 Screenshots

The `screenshots` folder contains evidence for:

1. Memory estimator output
2. Context-length experiment
3. Quantization experiment
4. `ollama list`
5. `ollama ps`
6. Model card information
7. Licence information

These screenshots provide evidence for the experiments and analysis.

---

# 📄 Analysis

The complete written analysis is available in:

```text
analysis.md
```

It contains:

* Scenario statement
* Concept explanations
* Memory estimate table
* Model comparison table
* Context-length experiment
* Quantization experiment
* Estimate vs reality
* Suitability analysis
* Conclusion

---

# 🚀 How to Run

## Step 1 – Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

## Step 2 – Enter the project

```bash
cd DAY4_OPEN_LLM_MEMORY
```

## Step 3 – Create virtual environment

```bash
python -m venv .venv
```

## Step 4 – Activate virtual environment

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Then:

```powershell
.venv\Scripts\Activate.ps1
```

## Step 5 – Run the estimator

```bash
python estimator.py
```

## Step 6 – Run experiments

```bash
python context_quantization.py
```

## Step 7 – Check Ollama

```bash
python ollama_check.py
```

---

# 🛠️ Technologies Used

* **Python**
* **Ollama**
* **Open LLMs**
* **GGUF / Quantized Models**
* **Model Cards**
* **Git**
* **GitHub**

---

# 📚 Learning Outcomes

Through this project, I learned how to:

* Estimate memory requirements before downloading a model
* Understand the relationship between parameter count and memory
* Understand quantization
* Understand KV cache and context length
* Compare estimated memory with real Ollama usage
* Read model cards
* Check model licences
* Understand the difference between open-weight and open-source models
* Evaluate whether a model is suitable for a local deployment scenario

---

# 📌 Conclusion

Choosing a local language model requires more than checking its parameter count or download size.

The decision involves considering:

```text
Model Size
     ↓
Quantization
     ↓
Context Length
     ↓
KV Cache
     ↓
Runtime Memory
     ↓
Licence
     ↓
Final Suitability
```

This project demonstrates a practical approach to checking both **whether a model will fit** and **whether it may be used for the intended scenario** before deployment.

---

## 👨‍💻 Project

**Course:** Agentic AI: Foundations and Open-Source Practice
**Task:** Day 4 – Will It Fit, and May I Use It?
**Focus:** Open LLMs, Memory Estimation, Quantization and Licences
