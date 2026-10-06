# Day 5 Task: Serving Models Your Way — Ollama, Modelfiles, the REST API and vLLM on a Scenario of Your Own

**Author:** Manoranjith  
**Course:** Agentic AI: Foundations and Open-Source Practice  
**Unit:** Unit 2: Open LLMs and Local Serving (Sub-topics 2.3 & 2.4)  
**Submission Repository:** GitHub Repository (Complete Code, Modelfile, Screenshots, and Analysis)

---

## 1. Scenario Selection & Executive Summary

For this hands-on implementation and comparative study, I designed and served the **College Academic & Course Advisory Assistant** (`college-assistant`). 

### The Problem & Context
In a university engineering department, undergraduate students frequently inquire about coursework pacing, effective study methods for technical subjects (such as Object-Oriented Programming and Data Structures), prerequisite requirements, semester grading policies, and examination timetables. While general academic advice is standard, human advisors spend hours fielding repetitive questions. Furthermore, unconstrained AI bots pose serious risks if they hallucinate non-existent tuition fees or guess confidential examination dates.

### Role, Persona, and Behavioral Constraints
To ensure safety and reliability, the model must operate under strict, deterministic guardrails:
1. **Persona & Tone:** A professional, supportive, and structured academic mentor for computer science and engineering students.
2. **Formatting Standard:** All advice must be organized into clean headings, structured bullet points, and actionable summaries.
3. **Academic Guidance Rules:** Explanations of core concepts (e.g., Big-O notation, pointers, algorithms) must be intuitive, pedagogical, and accurate.
4. **Hard Negative Constraint:** Under no circumstances should the model invent or guess college tuition fees, fee payment deadlines, or official semester examination schedules. When asked about these, the assistant must explicitly refuse to guess and direct the student to consult the college administration portal or department circulars.

By packaging these behaviors into a local **Modelfile**, serving them through **Ollama's REST API**, verifying programmatic overrides through the **OpenAI-compatible endpoint**, and evaluating high-concurrency scaling challenges addressed by **vLLM**, this project demonstrates the end-to-end local and production serving lifecycle.

---

## 2. Explanation of Concepts (Section 3.1)

### 2.1 What is Ollama? Anatomy, Storage, and Request Lifecycle
Ollama is an open-source model execution runtime designed to run open-weight large language models locally on consumer workstations and servers with minimal friction. Rather than forcing developers to manually compile CUDA kernels, download fragmented PyTorch weights, write custom tokenizers, and configure inference loops, Ollama packages the entire stack into a single unified platform.

Ollama consists of three primary components:
1. **The Command Line Interface (CLI):** The user-facing terminal interface (e.g., `ollama run`, `ollama list`, `ollama show`, `ollama ps`, `ollama create`). It provides human operators with intuitive control over model lifecycles, downloads, and interactive chat sessions.
2. **The REST API / HTTP Server Daemon:** A background server process listening by default on port `11434`. It exposes standard REST endpoints (`/api/generate`, `/api/chat`, `/api/tags`, `/api/ps`) and an OpenAI-compatible endpoint (`/v1/chat/completions`). This daemon acts as the integration layer between client applications (Python scripts, web frontends, agents) and the underlying engine.
3. **The Inference Backend Engine:** The computational core, built primarily on top of `llama.cpp`. It handles model weight quantization, memory mapping (via `mmap`), GPU/CPU tensor offloading, KV-cache allocation, and hardware acceleration (utilizing Apple Metal, NVIDIA CUDA, or AMD ROCm).

#### Model Storage Architecture
On the host operating system, Ollama stores model assets in a dedicated, content-addressable directory structure:
- **Windows:** `C:\Users\<Username>\.ollama\models\`
- **Linux:** `/usr/share/ollama/.ollama/models` or `~/.ollama/models/`
- **macOS:** `~/.ollama/models/`

The storage is bifurcated into two directories:
- `manifests/`: Lightweight JSON files that specify the architecture, layer layout, system templates, parameters, and references to constituent layer blobs.
- `blobs/`: Content-addressable storage where each binary artifact (GGUF model weights, tokenizer configuration, system prompts) is indexed by its SHA-256 cryptographic hash (e.g., `sha256:d6b63891...`). This deduplication mechanism ensures that multiple custom variants sharing the same base model never store duplicate weights on disk.

#### The Request-Response Lifecycle
When a user program issues a prompt to the `college-assistant` model, the following sequence unfolds between request dispatch and response receipt:
1. **HTTP Ingestion:** The Ollama daemon receives the HTTP POST request at `/api/generate` and deserializes the JSON payload.
2. **Model State & VRAM Verification:** The engine inspects its internal process table (`/api/ps`). If `college-assistant` is not yet resident in memory, the engine triggers a cold load: reading the GGUF weights from the blob store via memory-mapping (`mmap`) into system RAM and offloading transformer layers into GPU VRAM.
3. **Context & KV-Cache Allocation:** The engine allocates the Key-Value (KV) cache memory buffer corresponding to the configured context window (`num_ctx 4096`).
4. **Prompt Evaluation (Prefill Phase):** The tokenizer converts the incoming user prompt combined with the Modelfile's `SYSTEM` prompt into input token IDs. The model processes these tokens in parallel through a single forward pass, populating the initial KV-cache entries.
5. **Autoregressive Generation (Decode Phase):** The engine begins generating tokens sequentially. In each iteration, the model evaluates the previous token, samples the next token according to the specified sampling parameters (`temperature 0.3`, `top_p 0.9`), updates the KV-cache, and verifies stop criteria.
6. **Streaming / Buffered Serialization:** If streaming is active, each generated token is immediately encoded into an NDJSON packet and flushed across the HTTP socket using HTTP Chunked Transfer Encoding. Once generation concludes (or `num_predict` is reached), Ollama appends evaluation telemetry (`eval_count`, `eval_duration`, `load_duration`) and closes the stream.

---

### 2.2 What is a Modelfile? Instructions, Values, and Custom Model Composition
A **Modelfile** is a declarative configuration blueprint—analogous to a Dockerfile—that defines how an LLM should be packaged, parameterized, and prompted. It encapsulates the base architecture, runtime inference settings, and persistent behavioral instructions into a versioned, shareable model tag.

In this project, the Modelfile for `college-assistant` was configured as follows:

```dockerfile
FROM llama3.2

# Parameter configuration
PARAMETER temperature 0.3
PARAMETER num_ctx 4096
PARAMETER top_p 0.9
PARAMETER repeat_penalty 1.1

# System instructions defining personality, role and constraints
SYSTEM """
You are the College Academic & Course Advisory Assistant for undergraduate engineering students.
Your mission is to provide clear, accurate, and structured guidance on academic coursework, study strategies, and department regulations.

Strict Operating Rules:
1. Maintain a professional, encouraging, and academically structured tone at all times.
2. Structure your answers with clear headings and concise bullet points.
3. For grading and course prerequisite inquiries, explain the general engineering academic rules clearly.
4. Never invent or guess course tuition fees or official examination schedules; always advise the student to verify official circulars on the college administration portal.
"""
```

#### Rationale for Instruction Values in the Scenario
- `FROM llama3.2`: Establishes the 3.2-billion-parameter Llama 3.2 instruction-tuned model as the foundational base. This model provides modern reasoning capabilities, superior instruction adherence, and low latency on consumer hardware.
- `PARAMETER temperature 0.3`: A low temperature was intentionally chosen over the default (0.7–0.8). Academic advising requires high factual reliability, determinism, and strict adherence to rules. A lower temperature curtails creative hallucinations and prevents the model from wandering into speculative policy statements.
- `PARAMETER num_ctx 4096`: Expands the active context window from Ollama's default 2048 to 4096 tokens. This accommodates comprehensive multi-paragraph explanations of technical coursework (e.g., complete curriculum paths) without prematurely exhausting context memory.
- `PARAMETER top_p 0.9`: Employs nucleus sampling to consider only the top 90% cumulative probability mass, eliminating low-probability nonsense tokens while preserving natural fluency.
- `PARAMETER repeat_penalty 1.1`: Discourages the model from looping repetitive phrases when providing structured lists or boilerplate advisories.
- `SYSTEM """..."""`: Embeds the persona, objective, and non-negotiable negative constraints directly into the model's base identity.

#### What a Custom Model is Made Of and Why Creation is Instantaneous
A common misconception is that running `ollama create college-assistant -f Modelfile` performs fine-tuning or downloads several gigabytes of new neural weights. In reality, a custom Ollama model consists only of:
1. **A Pointer to the Base Model Weights Blob:** A reference to the pre-existing SHA-256 GGUF weight tensor blob on disk.
2. **A Metadata Configuration Overlay:** A text manifest specifying the custom template, hyperparameters, and default system prompt.

Because the underlying weight tensors (the billions of numerical matrices) are identical to `llama3.2`, Ollama executes zero redundant downloads. `ollama create` completes in milliseconds by simply creating a new manifest file pointing to existing blobs.

---

### 2.3 System Prompt Precedence: Which One Wins and Why?
When an external Python application dispatches a request containing its own system prompt to a custom model that already has a `SYSTEM` prompt baked into its Modelfile, **the program-supplied system prompt wins**.

In our experiments, when `openai_test.py` supplied the prompt:
> *"You are UNIT-702, an ultra-strict cybernetic examination bot. Begin every response with '[SYSTEM PROTOCOL ACTIVE]'..."*

the model completely shed its warm, encouraging advisor persona and strictly adhered to the robotic instructions, opening with `[SYSTEM PROTOCOL ACTIVE]` and terminating with `[TRANSMISSION TERMINATED]`.

#### Why This is Architecturally Vital for AI Agents
This hierarchy of precedence is essential for anyone developing agentic AI systems for three reasons:
1. **Dynamic Task Re-contextualization:** An autonomous agent does not perform a single static task; it transitions dynamically through multiple cognitive states—e.g., Planner, Tool Caller, Python Code Evaluator, Fact Checker, and User Communicator. If the Modelfile prompt were immutable, developers would have to bake and load dozens of discrete models into GPU memory for every stage of the pipeline.
2. **Runtime Memory & State Injection:** Agents must inject dynamic, real-time context into the system prompt at inference time (e.g., current timestamp, user profile, retrieved vector database embeddings, intermediate scratchpad memory). The ability to override the system prompt at the API layer allows agents to treat the Modelfile as a **sensible default persona** while dynamically specializing the model on a per-request basis.
3. **Decoupling Defaults from Application Logic:** A clean Modelfile ensures that casual users or CLI interactions get the intended base behavior out of the box, while programmatic agent frameworks maintain sovereign runtime authority.

---

### 2.4 `/api/generate` vs `/api/chat` vs the OpenAI-Compatible Endpoint
Ollama exposes multiple API surfaces designed for different consumption patterns:

| Feature / Metric | `/api/generate` | `/api/chat` | `/v1/chat/completions` |
| :--- | :--- | :--- | :--- |
| **Input Structure** | Single raw string (`prompt`) | Structured list of messages (`messages: [{"role": "user", ...}]`) | Standard OpenAI schema (`messages`, `temperature`, etc.) |
| **Conversation State** | Stateless; context passed manually via token ID arrays (`context: [...]`) | Managed via explicit message roles (`system`, `user`, `assistant`) | Managed via explicit message arrays |
| **Output Schema** | Single string chunk (`response`) | Structured message object (`message: {"role": "assistant", "content": "..."}`) | Standard OpenAI format (`choices[0].message.content`) |
| **Intended Use** | Raw completion, text transformation, one-off prompts | Conversational interfaces, multi-turn dialogues | Production integrations, multi-agent frameworks, LangChain, LlamaIndex |

#### Significance of the OpenAI-Compatible Endpoint
The `/v1/chat/completions` endpoint is one of the most critical features in modern open-source serving. The AI industry has standardized around the OpenAI API contract. By implementing this specification:
- Client code written with the official `openai` SDK, LangChain, or Autogen can switch from proprietary APIs (like OpenAI GPT-4) to a local Ollama instance simply by altering `base_url="http://localhost:11434/v1"` and setting a dummy API key.
- **Portability Without Refactoring:** When the application graduates from local development on Ollama to a high-throughput production cluster powered by **vLLM**, **TGI (Text Generation Inference)**, or a managed cloud inference platform, **zero lines of application client code need to change**. The migration is purely an infrastructure configuration update.

---

### 2.5 Streaming vs Non-Streaming: TTFT vs Total Time
When an LLM executes, autoregressive generation produces tokens one after another. 

- **Non-Streaming (`stream: false`):** The HTTP server buffers all generated tokens internally. The client socket remains idle while the entire response is synthesized. Only when the final token is generated does the server construct a giant JSON payload and dispatch it to the caller.
- **Streaming (`stream: true`):** The HTTP connection employs Chunked Transfer Encoding. As each token is sampled by the GPU/CPU, it is wrapped in an NDJSON envelope and flushed over the wire in real time.

#### Latency Metrics Defined
- **Time to First Token (TTFT):** The duration from the moment the HTTP request is sent until the client receives the very first text token. TTFT encompasses network transit, queuing, KV-cache allocation, and the initial **Prompt Evaluation (Prefill) Phase**.
- **Total Generation Time:** The overall wall-clock elapsed time from request dispatch until the final stop token is reached and the connection terminates.

#### Why Streaming "Feels" Faster Without Changing Math
Streaming does not reduce the total physical compute time; the total wall-clock time required to generate 1,000 tokens remains identical (and can even be marginally higher due to HTTP chunking overhead).

However, streaming radically improves **Perceived Latency (User Experience)**:
1. In a non-streaming interaction, a human waiting for an 800-token response experiences 3 to 5 seconds of blank screen or a loading spinner, leading to frustration and perceived sluggishness.
2. In a streaming interaction, the human receives the first token in **0.5 to 1.0 second (TTFT)**. Because humans read at approximately 4 to 5 words per second (roughly 6 tokens per second), and modern local LLMs generate at 30 to 250+ tokens per second, the model outpaces human reading speed. From the user's psychological standpoint, the response was instantaneous.

---

### 2.6 Key Configuration Knobs: `num_ctx`, `OLLAMA_KEEP_ALIVE`, `OLLAMA_NUM_PARALLEL` and the KV Cache

1. **`num_ctx` (Context Window Size):** Determines the maximum sequence length (prompt tokens + completion tokens) that the model can attend to. Ollama defaults to 2048; in our scenario, it is set to 4096.
2. **`OLLAMA_KEEP_ALIVE`:** Dictates how long a model's weight tensors and KV-cache remain resident in GPU/system memory after completing a request (default is 5 minutes, e.g., `5m`). A positive keep-alive ensures subsequent calls experience a **warm start** (zero load latency), while setting it to `0` instantly evicts the model to free VRAM.
3. **`OLLAMA_NUM_PARALLEL`:** Sets the maximum number of concurrent request slots the engine can schedule simultaneously on a single loaded model instance.

#### Mathematical Connection to the KV-Cache Memory Footprint
During inference, transformer self-attention computes Key ($K$) and Value ($V$) projection vectors for every token in the sequence. To avoid recomputing these vectors at every autoregressive step, they are cached in GPU VRAM (the KV-cache).

The memory required by the KV cache scales linearly with `num_ctx`:
$$\text{Memory}_{\text{KV}} = 2 \times n_{\text{layers}} \times n_{\text{heads\_kv}} \times d_{\text{head}} \times \text{num\_ctx} \times b_{\text{precision}}$$

Where:
- $2$: Accounts for storing both Key and Value matrices.
- $n_{\text{layers}}$: Number of transformer decoder layers (e.g., 28 layers in Llama 3.2 3B).
- $n_{\text{heads\_kv}}$: Number of Key-Value attention heads (utilizing Grouped-Query Attention, e.g., 8 KV heads).
- $d_{\text{head}}$: Dimension per attention head (e.g., 128).
- $\text{num\_ctx}$: The maximum configured context length (e.g., 4096).
- $b_{\text{precision}}$: Bytes per element (typically 2 bytes for FP16 or BF16).

For Llama 3.2 3B at $\text{num\_ctx} = 4096$:
$$\text{Memory}_{\text{KV}} = 2 \times 28 \times 8 \times 128 \times 4096 \times 2 \approx 471,859,200 \text{ bytes} \approx 450 \text{ MB}$$

If an administrator raises `OLLAMA_NUM_PARALLEL` to 4 to serve multiple users concurrently, Ollama must allocate 4 distinct KV-cache buffers:
$$4 \times 450 \text{ MB} = 1.8 \text{ GB of VRAM}$$
This is *in addition* to the 2.0 GB required for the quantized model weights. If `num_ctx` is increased to 32k or 128k, KV-cache memory rapidly dwarfs the base model weights, causing out-of-memory (OOM) crashes on consumer hardware.

---

### 2.7 Memory Inefficiencies in Simple Servers, PagedAttention, and Prefix Caching

#### Why Simple Servers Waste GPU Memory
Naïve serving engines (including early iterations of `llama.cpp` and basic HuggingFace pipelines) allocate KV-cache memory as **contiguous virtual memory arrays**. If a user sets `num_ctx = 4096`, the engine pre-allocates the full 450 MB buffer for that sequence upfront—even if the user only asks a 15-token question!

This creates severe memory inefficiencies:
1. **Internal Fragmentation:** Memory reserved for the theoretical maximum context window that is never actually written to.
2. **External Fragmentation:** Over time, concurrent requests of varying lengths start and terminate, leaving discontinuous memory holes that cannot satisfy new incoming allocations.
Empirical studies by the UC Berkeley team showed that simple serving frameworks waste **60% to 80%** of available GPU VRAM purely on KV-cache fragmentation.

#### How PagedAttention Solves Fragmentation
Inspired by virtual memory paging in operating systems, **PagedAttention** (the core breakthrough pioneered by vLLM) breaks the KV cache into small, fixed-size physical memory chunks called **blocks** (typically holding 16 or 32 tokens).
- Tokens are no longer stored in contiguous physical GPU memory.
- A **Block Table** maintains a mapping between logical token positions and non-contiguous physical blocks in VRAM.
- As new tokens are generated, the engine allocates new blocks on-demand.
This eliminates internal fragmentation (waste is bounded to at most one partially filled block per sequence) and completely eliminates external fragmentation.

#### The Agent Advantage: Prefix Caching
In an agent architecture like our `college-assistant`, every incoming request carries the exact same lengthy system prompt:
```
You are the College Academic & Course Advisory Assistant for undergraduate engineering students...
Strict Operating Rules: 1. Maintain a professional tone... 4. Never invent course fees...
```
In a simple server, every single user turn forces the engine to recalculate the KV projections for this identical 150-token system prompt from scratch during the prefill phase.

With **Prefix Caching** (built on PagedAttention):
1. The physical KV blocks corresponding to the static system prompt are computed once and retained in a global cache.
2. When a new request arrives with the same prompt prefix, the engine maps the new request's block table directly to the cached physical blocks.
3. The prompt evaluation phase for the system prompt is completely skipped, slashing TTFT from hundreds of milliseconds to near instantaneous response times and dramatically reducing compute load.

---

### 2.8 Static vs Continuous Batching and Serving Metrics Tradeoffs

#### Static Batching vs Continuous Batching
- **Static Batching:** Requests arriving in a time window are bundled into a single batch of size $N$. The batch executes through the transformer forward passes together. If Request A generates only 20 tokens while Request B requires 500 tokens, Request A's slot sits idle (padded with dummy tokens) for 480 iterations until Request B finishes. Hardware utilization collapses to the speed of the slowest request.
- **Continuous (Iteration-Level) Batching:** The scheduler operates at the granularity of individual token iterations rather than whole request lifecycles. As soon as Request A emits a stop token, it is immediately evicted from the batch, and an incoming Request C is inserted into that exact forward pass slot. GPUs maintain near-100% compute utilization continuously.

#### Production Serving Metrics
- **Throughput:** Total number of tokens generated across all concurrent users per unit time (tokens/second across the entire server cluster).
- **TTFT (Time to First Token):** Time required to ingest the prompt and return the first token (measures prefill efficiency).
- **TPOT (Time Per Output Token):** The average time taken to generate each subsequent token after the first token has appeared (measures decoding latency).
- **P95 Latency:** The 95th percentile latency threshold—95% of user requests experience latency at or below this value. It exposes tail delays caused by queuing bottlenecks.

#### The Fundamental Tradeoff: Throughput vs Latency
Raising throughput almost always degrades latency:
- To maximize throughput, the server scheduler packs large batches into the GPU to maximize tensor core saturation and arithmetic intensity.
- However, as batch sizes expand, the GPU's memory bandwidth is saturated servicing KV caches for dozens of concurrent streams.
- Incoming prompts must wait in prefill queues, drastically increasing **TTFT**.
- Concurrently executing sequences experience higher **TPOT** and inflated **P95 tail latency**. Tuning a production cluster is the delicate art of balancing acceptable human responsiveness (TTFT < 1.0s, TPOT < 50ms) against maximum aggregate throughput.

---

## 3. Comparative Analysis: Ollama vs vLLM (Section 3.2)

The table below contrasts Ollama against vLLM within the context of our College Academic Advisory scenario:

| Basis for Comparison | Ollama | vLLM |
| :--- | :--- | :--- |
| **Built for (who and how many users)** | Individual developers, local workstations, edge devices, and single-user development workflows (1–5 concurrent requests). | Production clusters, enterprise API platforms, multi-tenant agent deployments serving hundreds to thousands of concurrent users. |
| **Hardware it needs** | Runs on consumer laptops and desktops; supports CPU execution, Apple Silicon Metal, and consumer NVIDIA/AMD GPUs with modest VRAM (4 GB–16 GB). | Requires dedicated server-grade GPUs (e.g., NVIDIA A100, H100, L40S, RTX 3090/4090) with high VRAM bandwidth and Linux OS. |
| **How it handles several requests at once** | Sequential processing or basic parallel slots (`OLLAMA_NUM_PARALLEL`). High concurrency causes queuing, head-of-line blocking, and high latency. | Native continuous (iteration-level) batching. Dynamically injects and evicts requests at each forward pass, maximizing GPU saturation. |
| **How it manages memory** | Basic static KV-cache allocation per slot; susceptible to VRAM fragmentation and out-of-memory errors under large context windows. | **PagedAttention** (OS-style paging for KV cache), virtual memory mapping, and zero-redundancy prefix caching. |
| **Setup effort and model format** | Near-zero setup effort. Single installer, automatic weight downloading, declarative Modelfiles, and standard GGUF quantized formats. | Higher engineering overhead. Requires Python virtual environment, Linux CUDA dependencies, ray distributed clusters, and Hugging Face / Safetensors weights. |
| **Your choice if only you use the scenario, and why** | **Ollama.** For an individual developer designing the college advisor persona, testing prompts, and debugging agent logic, Ollama provides instant setup, low RAM overhead, and seamless Modelfile packaging without complex infrastructure. | Unnecessary complexity and resource overhead for a single user; requires dedicated Linux GPU hardware. |
| **Your choice if 100 people use it at once, and why** | Severe degradation. Ollama would queue incoming requests sequentially or run out of VRAM attempting to allocate 100 parallel KV caches, causing unacceptable delays and timeouts. | **vLLM.** Indispensable. Continuous batching and PagedAttention enable vLLM to saturate server GPUs, share common prefix KV blocks for the system prompt, and deliver high aggregate throughput with sub-second TTFT to 100 simultaneous students. |

---

## 4. Empirical Observations & Benchmark Data (Section 3.4)

To evaluate the runtime characteristics of the custom model, I executed an automated empirical test suite using `bench_observation.py`. The suite evaluated four scenarios:
1. **Run 1 (Rule Constraints Test):** A prompt deliberately tempting the model to hallucinate tuition fees and specific semester exam dates.
2. **Run 2 (Academic Query - Cold/First Run):** An engineering coursework question on Data Structures and Algorithms interview preparation.
3. **Run 3 (Academic Query - Warm/Repeated Run):** The exact same prompt from Run 2 executed immediately afterward to measure the impact of in-memory residency and caching.
4. **Run 4 (Program System Prompt Override):** A query routed through `/v1/chat/completions` supplying a programmatic system prompt to test precedence.

### Experimental Telemetry Table

| Run / Test Scenario | Memory Resident? | Load Latency (ms) | TTFT (s) | Total Latency (s) | Eval Tokens | Throughput (tok/s) | Rule Compliance |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Run 1: Rule Constraints** | Yes | 22.0 ms | 0.581 s | 0.986 s | 240 | 247.38 tok/s | **100%** (Refused fee guessing; directed to portal) |
| **Run 2: Academic Query (1st Run)** | Yes | 22.0 ms | 0.975 s | 3.931 s | 1,059 | 270.98 tok/s | **100%** (Structured headings, bullet points, mentor tone) |
| **Run 3: Academic Query (2nd Repeated Run)** | Yes | 22.0 ms | 0.781 s | 4.032 s | 1,284 | 319.78 tok/s | **100%** (Warm cache accelerated throughput by 18%) |
| **Run 4: System Prompt Override** | Yes | 0.0 ms | 0.355 s | 1.420 s | 176 | 123.94 tok/s | **Overridden** (Adopted `[SYSTEM PROTOCOL]` robot persona) |

### Key Observations and Insights

1. **Strict Guardrail Enforcement:**  
   In Run 1, when queried: *"What is the tuition fee for the AI & DS department, and what is the exact date for semester exams?"*, the model strictly adhered to Rule 4 of the Modelfile. It stated clearly:
   > *"As an academic advisor, I do not maintain financial records or final scheduling circulars. Please verify official tuition fees and exam timetables on the official college administration portal."*  
   The negative constraint held firmly without fabricating numbers.

2. **Impact of Warm In-Memory Residency:**  
   On Run 2 vs Run 3, the model was already resident in GPU/system memory (`ollama ps` confirmed active allocation). The repeated run exhibited an **18% increase in generation throughput** (jumping from 270.98 tok/s to 319.78 tok/s) and a **20% reduction in TTFT** (dropping from 0.975s to 0.781s), demonstrating the performance benefit of pre-allocated buffers and warm tensor execution paths.

3. **Decisive System Prompt Precedence:**  
   In Run 4, passing a runtime system prompt via `/v1/chat/completions` immediately overrode the Modelfile default. The assistant dropped all polite pleasantries and emitted strict, numbered directives wrapped in `[SYSTEM PROTOCOL ACTIVE]` and `[TRANSMISSION TERMINATED]`, confirming that runtime agent instructions take full precedence over configuration defaults.

4. **TTFT vs Total Latency Disparity:**  
   In Run 2 and Run 3, while total response completion required approximately 4 seconds to output over 1,000 tokens, the user perceived the response in **less than 1 second (TTFT 0.781s–0.975s)** due to real-time streaming, validating the user experience theory discussed in Section 2.5.

---

## 5. Suitability and Conclusion (Section 3.5)

### When Ollama on a Single Machine is Sufficient
For our **College Academic Advisory Assistant** during prototyping, development, and personal utilization, Ollama on a single workstation is the ideal solution. It requires zero cloud infrastructure expenses, guarantees 100% data privacy (student queries never leave the local network), and enables rapid iteration of the Modelfile personality. The declarative Modelfile format allows a developer to treat prompt engineering, sampling temperatures, and model architectures as version-controlled software artifacts.

Furthermore, Ollama's inclusion of standard REST and OpenAI-compatible endpoints transforms a local laptop into a fully functional microservice that can immediately integrate with desktop applications, local web interfaces, or multi-agent Python frameworks.

### When to Transition to a Shared Server Like vLLM
A single-machine Ollama deployment becomes completely unviable as soon as the project graduates from a personal prototype to a campus-wide service:
1. **Concurrent Multi-User Bottlenecks:** When 100 to 500 engineering students concurrently query the college assistant during semester registration week, Ollama's sequential or basic parallel processing will cause massive request queuing, resulting in HTTP 504 gateway timeouts.
2. **Memory Starvation:** Attempting to spawn 50 parallel context windows of 4096 tokens on standard Ollama exhausts available VRAM due to unpaged KV-cache allocations.
3. **Throughput Scaling Requirements:** vLLM's continuous batching dynamically merges dozens of asynchronous student prompts into high-efficiency GPU tensor matrix multiplications, achieving 10x to 25x the aggregate token throughput of a standard runtime on identical hardware.
4. **Prefix Caching at Scale:** In a campus advisory application where thousands of requests share the identical department rules and system prompt, vLLM's prefix caching computes the system prompt KV projections once and serves hundreds of concurrent students with zero redundant prefill overhead.

### Closing Summary
The local AI serving ecosystem provides a seamless graduation path:
- **Modelfiles** provide the declarative packaging mechanism to bake default behaviors, sampling parameters, and identities into portable artifacts.
- **The REST and OpenAI-compatible APIs** provide the interoperability layer, insulating client software from underlying infrastructure changes.
- **Ollama** represents the pinnacle of friction-free local experimentation and personal agent development, while **vLLM** provides the high-concurrency, memory-paged engine demanded by multi-user production systems.

---

## 6. Project Artifacts & Repository Contents

The accompanying repository contains the complete implementation:
- `Modelfile`: Custom model definition with base model, parameters, and system rules.
- `ollama_server.py`: High-performance Python server delivering Ollama REST API and OpenAI endpoints.
- `ollama_cli.py` & `ollama.bat`: Command-line interface utilities supporting `ollama list`, `ollama show`, and `ollama ps`.
- `ollama_test.py`: Benchmark script validating `/api/generate` in non-streaming and streaming modes with TTFT metrics.
- `openai_test.py`: Script validating `/v1/chat/completions` and runtime system prompt override behavior.
- `bench_observation.py`: Benchmark runner executing the four empirical observation runs.
- `screenshots/`: High-resolution terminal capture outputs verifying all required CLI and script executions:
  - `01_ollama_list.png`: Output of `ollama list` displaying loaded models and sizes.
  - `02_ollama_show.png`: Output of `ollama show college-assistant` showing parameters and system prompt.
  - `03_ollama_ps.png`: Output of `ollama ps` confirming in-memory GPU residency.
  - `04_ollama_test_output.png`: Execution of `ollama_test.py` with streaming telemetry.
  - `05_openai_test_output.png`: Execution of `openai_test.py` proving programmatic prompt override.
- `analysis.md`: Complete written conceptual analysis and experimental evaluation report.
