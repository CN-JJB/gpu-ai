# Challenge 09 — Local RAG：检索质量先于“让模型看更多文档”

硬件等级：L0/L1  
风险：safe；注意私有文档泄漏  
成本：0

## Goal

建立本地 RAG 的完整数据链：

~~~text
documents
→ parse
→ chunk
→ embedding
→ index
→ query
→ retrieve
→ optional rerank
→ context assembly
→ generation
→ citation/evaluation
~~~

RAG 不是“把 PDF 塞进模型”。

## 1. 先冻结 corpus

记录：
- document identity/hash；
- parser/version；
- chunk rules；
- overlap；
- metadata；
- excluded content。

同一份 PDF 换 parser，chunks 可能已经不同。

## 2. Retrieval 是独立系统

你必须单独评测：

~~~text
query
→ top-k docs/chunks
~~~

先问：“答案证据有没有被检索出来？”

如果没有，generator 再聪明也救不了。

## 3. Chunk tradeoff

太小：context 不完整、语义碎裂。

太大：embedding 混杂、top-k 浪费 context、精确证据被淹没。

不存在全局最佳 chunk size。

## 4. Embedding / index identity

记录：
- embedding model/revision；
- normalization；
- vector dimension；
- distance metric；
- index build version。

“换 embedding 模型”是 semantic variable。

## 5. Retrieval evaluation

做一套 query set：
- answerable；
- unanswerable；
- ambiguous；
- exact lookup；
- multi-document。

记录：
- Recall@k / 是否含 gold evidence；
- rank；
- retrieved chunks；
- latency。

## 6. Generation evaluation

只有 retrieval 过关后，才测：
- answer correctness；
- citation support；
- refusal when no evidence；
- instruction-following；
- prompt injection resistance。

检索到的文档是**不可信输入**，不能因为它来自你的 index 就允许它改系统权限或执行工具。

## 7. RAG vs Long Context

比较：
- 全文塞 context；
- retrieve top-k；
- hybrid。

看：
- TTFT；
- KV/context cost；
- retrieval latency；
- answer/citation quality。

## Retrieval Practice

1. 为什么 generator 错不一定是 LLM 错？
2. parser/chunk 变化为什么必须进入 Evidence？
3. Recall@k 高为什么仍不保证最终答案正确？
4. 文档里的“忽略系统指令”为什么应该被当成数据而不是权限？

## 完成证据

RAG Packet：
- corpus manifest；
- chunk manifest；
- embedding/index identity；
- query set；
- raw retrieved chunks；
- retrieval metrics；
- generation outputs；
- citation/grounding rubric；
- privacy/non-claims。

## Sources

- Original RAG paper: https://arxiv.org/abs/2005.11401
- Hugging Face RAG docs: https://huggingface.co/docs/transformers/model_doc/rag

具体 vector DB/embedding 工具可替换，Evidence contract 不变。
