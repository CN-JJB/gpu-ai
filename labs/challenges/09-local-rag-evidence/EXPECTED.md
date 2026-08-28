# Expected — Challenge 09

合格 RAG 项目必须把 retrieval 与 generation 分开评测。

至少：
- corpus/chunk identity；
- embedding/index identity；
- answerable + unanswerable query set；
- raw top-k retrieval；
- retrieval success metric；
- grounded answer/citation check；
- prompt-injection/untrusted-document 边界；
- long-context baseline 或解释为何不比较。
