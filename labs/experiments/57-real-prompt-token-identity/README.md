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
