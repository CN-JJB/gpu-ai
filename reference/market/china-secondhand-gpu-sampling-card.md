# 中国二手 GPU 市场采样卡

## 1. Record identity

每条数据必须填写：

- date
- platform
- listing URL / ID
- exact GPU
- VRAM
- exact board/variant
- stock / modded / repaired
- seller type
- condition evidence
- price
- price state
- shipping/service fee
- notes

## 2. Price state

Use only:

- ASK
- SOLD-CONFIRMED
- DELISTED-ASSUMED
- MERCHANT-QUOTE
- BUYBACK
- UNKNOWN

Do not write “成交价” unless the evidence actually proves it.

## 3. Reject from normal price sample

Reject or separate:

- multi-SKU bait listing
- cooler/PCB/accessory only
- deposit
- broken/junk
- repaired unless building repair cohort
- VRAM-modified unless building mod cohort
- full PC bundle
- wanted-to-buy ad
- rental/cloud service
- no exact option price

## 4. Condition evidence

- C0 unknown
- C1 seller claim
- C2 functional evidence
- C3 strong pre-sale test evidence
- C4 independent/buyer verification

## 5. Market evidence

- M3 direct normalized platform evidence
- M2 current transparent secondary aggregation
- M1 anecdote / unattributed summary
- M0 unknown

## 6. Snapshot statistics

For each cohort:

```
sample window:
n:
excluded:
median ASK:
Q1:
Q3:
confirmed SOLD n:
confirmed SOLD median:
observed range:
market evidence grade:
```

## 7. Listing risk tags

Possible tags:

- STOCK
- MOD_VRAM
- REPAIRED
- REBALL
- MINING_CLAIM
- DATACENTER
- OEM
- ES
- PASSIVE_COOLING
- NO_DISPLAY
- CUSTOM_POWER
- BIOS_MOD
- UNKNOWN_HISTORY

## 8. Candidate decision link

After price normalization, copy the candidate into:

`labs/experiments/32-real-used-hardware-candidate-dossier/`

Then run:

```
FIT
→ SOFTWARE
→ performance evidence
→ TCO
→ risk
→ price threshold
```

Market price alone is never the final decision.
