# Experiment 53 — Real Model Architecture Dossier

硬件等级：L0

## Goal

Create a reusable model-side dossier for an actual model you may deploy.

## Run

With config only:

```bash
python3 dossier.py config.json \
  --context 32768 \
  --kv-bits 16 \
  --sequences 1 \
  --params-b <published-parameter-count> \
  --weight-bpw <effective-bpw> \
  --reserve-gib 1 \
  --memory-gib <candidate-usable-memory>
```

Better, when exact GGUF exists:

```bash
python3 dossier.py config.json \
  --artifact /path/to/model.gguf \
  --context 32768 \
  --kv-bits 16 \
  --memory-gib 24
```

The exact artifact path causes the script to record:
- file bytes;
- SHA256.

## Evidence discipline

The output separates:
- config facts;
- formula-derived proxies;
- runtime hypotheses.

It never outputs fake PP/TG.

## Finish

Fill:
`RESULT-TEMPLATE.md`

Then pair this dossier with:
- Slice 18 hardware candidate dossier;
- Slice 22 real capstone.
