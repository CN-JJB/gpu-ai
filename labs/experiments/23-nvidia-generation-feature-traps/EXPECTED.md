# Expected — Experiment 23

仓库自带的 `student_answers.json` 是一份已验证参考答案，因此直接运行：

```bash
python3 check_lineage.py
```

应得到：

```text
score: 10/10
```

## 真正的练习

先复制一份：

```bash
cp student_answers.json my_answers.json
```

然后故意把这些常见误区改成 `true`，再对照解释：

- all Pascal has HBM2
- all Pascal has GP100-class FP16
- all Ampere has identical SM
- all Blackwell is dual-die
- Q4 GGUF guarantees native FP4

## 应形成的思维

```
architecture feature claim
→ universal to family?
→ variant-specific?
→ product-specific?
→ software-specific?
```

如果不能回答这四层，就不要用一个架构名字推导买卡结论。