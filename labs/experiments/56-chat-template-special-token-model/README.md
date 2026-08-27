# Experiment 56 — Chat Template / Special Token Toy Model

硬件等级：L0

## Goal

Show that identical message content can become different token sequences because of serialization/template choices.

The toy tokenizer:
- recognizes a small set of registered special tokens as one token;
- encodes all other UTF-8 bytes individually.

This is **not** a real BPE/SentencePiece tokenizer.

It exists only to make the boundary visible.

## Run

```bash
python3 simulate.py
```

Messages:

```
system: Answer briefly.
user: Hello!
```

Template A uses registered role/end tokens.

Template B uses verbose plain-text headings.

The script also simulates:
```
template already emitted BOS
+
tokenizer auto-adds BOS
```

to expose duplicate special-token behavior.

## Expected

The same visible messages produce different:
- rendered bytes;
- SHA256;
- token counts;
- token-ID sequences.

Therefore:
```
same user text
!= same model input
```
