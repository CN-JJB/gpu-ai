# Experiment 57 — Real Prompt Artifact / Token Identity

硬件等级：L0

## Goal

For one actual local model/tokenizer, save the exact prompt identity used by a chat workload.

## Path A — local Hugging Face tokenizer

Requires an already available local Transformers tokenizer/model directory.

```bash
python3 render_prompt.py \
  /path/to/model-or-tokenizer-dir \
  messages.json \
  --out-dir prompt-evidence
```

Default is local-files-only.

Outputs:
- `rendered.txt`
- `token_ids.json`
- `manifest.json`

Manifest includes:
- messages SHA256;
- chat-template SHA256;
- rendered SHA256;
- token-ID SHA256;
- token count;
- special-token map;
- add_generation_prompt state.

## Path B — llama.cpp vocabulary cross-check

Pinned llama.cpp includes `llama-tokenize`.

Current usage includes:

```bash
llama-tokenize -m model.gguf -f rendered.txt --ids --show-count
```

Current tokenize tool parses special tokens by default and can load vocabulary only.

### BOS caution

The tool may auto-add BOS if the model vocabulary says it should.

If the rendered prompt already explicitly contains the intended BOS, inspect current:

```bash
llama-tokenize --help
```

and use the current BOS/special-token options deliberately.

Do not force `--no-bos` for every model.

## Cross-runtime comparison

HF token IDs and llama.cpp token IDs should only be compared after confirming:
- same tokenizer vocabulary;
- same special-token policy;
- same rendered bytes;
- same model revision/conversion.

A mismatch is evidence to investigate, not something to hide.

## Complete

Fill:
`RESULT-TEMPLATE.md`


## Why this experiment

Benchmark 的 prompt identity 不是“我输入了同一句话”这么简单。chat template、special token、BOS、tokenizer revision 都会改变模型真正看到的 token 序列。

## Hypothesis

只要 rendered bytes、token IDs 或 special-token policy 有一项不同，两次 benchmark 就不应被当作严格相同 prompt workload。

## Fixed variables

一次 evidence 包绑定一个 exact model/tokenizer revision、messages.json、template 和 generation-prompt policy。

## What to observe

1. messages SHA。
2. chat-template SHA。
3. rendered SHA。
4. token-ID SHA 与 count。
5. HF/llama.cpp cross-check 是否在 same vocabulary/policy 前提下匹配。
6. BOS 是否被重复添加。

## Troubleshooting

- 不要默认所有模型都应该 --no-bos。
- tokenizer 与 converted GGUF vocabulary 必须确认同源。
- mismatch 要保留并调查，不能只选“看起来正确”的一边。
- prompt 内容相同但 template 不同，仍不是相同模型输入。

## Evidence to save

保存 messages.json、rendered.txt、token_ids.json、manifest.json，以及 cross-runtime 原始输出。

## What this proves

你能把真实 prompt 固化成可复现 token identity。

## What this does NOT prove

它不评价回答质量，也不证明两个 runtime 生成一定相同。

## No-hardware path

只需要本地 tokenizer/model artifact，不要求 GPU。

## Transfer question

同一个 prompt 在两个 runtime token count 分别是 512 和 527。你应该先比较 TG，还是先解决 token identity？为什么？
