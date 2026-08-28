# Spec 0031 — Intelligence exact quality evaluation argv binding

Status: implemented in I30.

## Problem

I27 authenticated a field named `evaluation_args`, and I28/I29 authenticated the executed quality command. But `evaluation_args` was still free-form text and was not machine-bound to the command's actual non-input configuration.

A run could therefore claim one evaluation configuration while executing another.

## Schema v2

Quality identity moves to:

~~~json
{
  "quality_identity_schema_version": 2,
  "tokenizer_identity": "...",
  "corpus_sha256": "...",
  "fixture_revision": "...",
  "evaluation_args": ["--flag", "value"]
}
~~~

`evaluation_args` is an exact JSON array of argv tokens.

An empty array means there are no additional quality-evaluation arguments beyond model/corpus selection.

## Canonical argv projection

Given the executed quality command:

~~~text
EXECUTABLE [ARGS...]
~~~

I30 removes only:
- the executable token at argv[0];
- exactly one `-m/--model` selector and its value;
- exactly one `-f/--file` selector and its value.

Every remaining token, in original order and with duplicates preserved, is the executed evaluation-argument vector.

The vector must exactly equal quality identity `evaluation_args`.

No shell parsing, whitespace splitting, flag reordering, default inference, or upstream-specific semantic interpretation is performed.

## Capture

`capture_quality_eval.py` now fails before launch when declared and executed evaluation args differ.

A sealed command record uses:

~~~text
quality_capture_schema_version = 2
evaluation_args = exact argv-derived token list
~~~

## Verification

`verify_quality_execution.py` independently derives the vector again and requires three-way equality:

~~~text
quality identity evaluation_args
=
command record evaluation_args
=
argv-derived evaluation_args
~~~

The main I29 intake gate inherits this check because it reuses the I28 verifier.

## Tamper model

The I30 negative test changes an evaluation token in `command.json`, updates its recorded `evaluation_args`, and recomputes the quality PACKET.

Verification still blocks because the executed vector no longer equals the authenticated quality identity.

## Trust boundary

I30 proves exact configuration-token identity.

It still does not prove:
- that an upstream flag has the intended semantic effect;
- implicit/default settings not present in argv;
- PPL parsing or statistical interpretation;
- task quality;
- causal A/B conclusions;
- purchase suitability.
