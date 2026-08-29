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


## Why this experiment

同一句可见文本，经过不同 chat template、special token 规则后，真正送进模型的 token 序列可以不同。这个实验训练你把“用户消息”与“模型输入”分开。

## Hypothesis

Template A 与 Template B 会产生不同 rendered bytes、SHA256、token count 和 token IDs；重复 BOS 也会改变输入，因此模板差异本身就是 benchmark 变量。

## Fixed variables

system/user message 内容保持不变，只改变 serialization/template 行为。

## What to observe

1. 两种 template 的 rendered bytes。
2. SHA256 是否不同。
3. token count / token IDs 如何变化。
4. duplicate BOS case 为什么会造成额外 special token。

## Troubleshooting

- 不要把 toy tokenizer 当真实 BPE/SentencePiece。
- 比较真实模型时必须记录 tokenizer revision、chat template 和 special-token policy。
- “界面显示相同”不代表模型看到的输入相同。

## Evidence to save

保存 simulate.py 输出，并把 Template A/B 的 rendered text、hash、token IDs 并排记录。

## What this proves

你理解 chat serialization 是模型输入 identity 的一部分。

## What this does NOT prove

它不评价哪种 template 质量更好，也不代表真实模型 token 数。

## No-hardware path

完整 L0。

## Transfer question

如果两个 benchmark 使用同一 prompt 文本，但一个 runtime 自动加 BOS、另一个没有，它们还能算严格可比吗？
