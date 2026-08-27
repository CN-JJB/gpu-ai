---
date: 2026-08-26
type: course-build-record
---

# Local LLM VRAM budgeting vertical slice completed

第五个 bounded slice 完成：

Research → Reference → HTML Lesson → L0 Calculator → Example Evidence → real-config inspection path → Resources update → Learning update。

## Built artifacts

- research/llm/0001-vram-weights-kv-budget.md
- reference/llm/vram-weights-kv-budget.md
- lessons/05-llm-memory/01-weights-kv-vram-budget.html
- labs/experiments/08-vram-capacity-budget/README.md
- labs/experiments/08-vram-capacity-budget/budget.py
- labs/experiments/08-vram-capacity-budget/inspect_config.py
- labs/experiments/08-vram-capacity-budget/EXPECTED.md
- examples/evidence/experiment-05-vram-budget.md
- resources/RESOURCES.md
- learning/CURRENT.md

## Research conclusions

### File size is not the capacity model

Three distinct quantities are now explicit:

checkpoint file
!= parameter payload
!= runtime VRAM

This prevents the common garbage-hardware mistake of comparing model download size directly with GPU VRAM.

### Effective bpw is the useful budget variable

Baseline:

```text
weights ≈ params × effective_bpw / 8
```

The lesson does not teach nominal “4-bit” as exact 4 bpw because group scales, metadata, mixed tensors and backend packing exist.

### KV cache is derivable from architecture

For homogeneous standard decoder attention:

```text
KV bytes/token/sequence
= 2 × layers × kv_heads × head_dim × bytes_per_element
```

Then multiply by:
- cached tokens
- active sequences

This makes config.json a real hardware-selection document.

### MHA/GQA/MQA now have a practical reason

The slice links `num_key_value_heads` directly to capacity.

Abstract 32-layer / head_dim 128 / FP16 KV @ 4K:

- MHA 32 KV heads → 2 GiB / sequence
- GQA 8 → 0.5 GiB
- MQA 1 → 0.0625 GiB

No claim is made that this alone determines speed/quality.

### Headroom is required

The calculator never treats “estimate <= VRAM” as a guarantee.

It reports remaining GiB and percentage, with a course-only TIGHT warning below 10%.

Runtime buffers, allocator behavior, static/paged KV pools and other processes remain outside the pure formula.

## L0 validation

Abstract 7B-like GQA:

- 7B params
- effective 4.5 bpw
- weights = 3.667 GiB
- KV = 128 KiB/token/sequence
- 4K = 0.5 GiB/sequence
- runtime reserve = 1.5 GiB
- target = 8 GiB

Results:

- concurrency 1 → 5.667 GiB total
- 2 → 6.167
- 4 → 7.167
- 8 → 9.167, baseline already over target

This is intentionally an abstract model, not a compatibility claim about any named checkpoint.

## Real-model investigation path

`inspect_config.py` reads a local Hugging Face-style config.json.

It extracts:
- layers
- attention heads
- KV heads
- head_dim
- hidden_size

and warns if it sees architecture features such as:
- sliding_window
- layer_types
- per_layer_config
- attention_chunk_size

that invalidate a homogeneous full-attention estimate.

Parameter count is still supplied separately so learners must investigate it from model card / safetensors metadata rather than invent it from the model name.

## Runtime boundary

Hugging Face documents Dynamic/Static/Quantized caches and sliding/chunked cache behavior.

TensorRT-LLM documents a paged KV pool and runtime memory reservation.

Therefore the course clearly labels:

```text
formula baseline != runtime reserved VRAM
```

## Offload bridge

AMD Infera provides a current real-world example of KV moving from GPU to RAM/NVMe/network.

The lesson uses that only to establish a stable systems point:

offload solves capacity by creating a new data-movement path.

It does not pretend offload is free.

## Skill workflow

- teach：real “will it fit?” problem, minimal formulas, retrieval + decision Evidence.
- research：HF + NVIDIA + AMD first-party sources.
- scaffold-exercises discipline：calculator has deterministic expected output and transfer questions.
- domain-modeling not triggered; no project-level glossary boundary changed.
- no grill/to-spec; frozen v1 scope remains valid.

## Next

Separate four concepts that beginners frequently collapse:

numerical datatype
→ quantization algorithm
→ checkpoint/container format
→ backend/kernel compatibility.

Then connect effective bpw from this slice to real GGUF/GPTQ/AWQ/EXL2-style model artifacts.
