# Expected — Experiment 56

Default expected:

```
Template A:
rendered bytes = 72
toy token count = 32

Template B:
rendered bytes = 67
toy token count = 63
```

Although Template B has fewer rendered bytes, it has many more toy tokens because Template A's long control strings are registered as single special tokens.

Duplicate BOS simulation:

```
normal A count = 32
auto-BOS count = 33
first two tokens = ["<BOS>", "<BOS>"]
```

## Lesson

Token count depends on:
- serialization;
- special-token registration;
- tokenizer.

Raw character/byte count is not a token count.
