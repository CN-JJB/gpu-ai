# Expected — Experiment 57

No universal token IDs/count.

A valid result contains:
- exact messages hash;
- chat-template hash;
- rendered-prompt hash;
- token-ID hash/count;
- special-token policy;
- model/tokenizer identity.

If the local tokenizer has no chat template, the correct result is to stop and investigate model documentation.

Do not invent a generic ChatML template merely to make the script run.
