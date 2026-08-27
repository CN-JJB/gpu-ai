# Expected result

Default run：

~~~bash
python simulate.py
~~~

Expected：

~~~text
Synthetic cost model; baseline target serial step = 1.0. Not a real runtime predictor.
draft_cost/token=0.080, verify_cost=1.080 + 0.040*D

  accept    D   E accepted   E progress  round cost   speedup
----------------------------------------------------------------
     30%    1       0.3000       1.3000      1.2000    1.083x
     30%    2       0.3900       1.3900      1.3200    1.053x
     30%    4       0.4251       1.4251      1.5600    0.914x
     30%    8       0.4285       1.4285      2.0400    0.700x

     60%    1       0.6000       1.6000      1.2000    1.333x
     60%    2       0.9600       1.9600      1.3200    1.485x
     60%    4       1.3056       2.3056      1.5600    1.478x
     60%    8       1.4748       2.4748      2.0400    1.213x

     90%    1       0.9000       1.9000      1.2000    1.583x
     90%    2       1.7100       2.7100      1.3200    2.053x
     90%    4       3.0951       4.0951      1.5600    2.625x
     90%    8       5.1258       6.1258      2.0400    3.003x
~~~

## Why p=0.30 saturates

~~~text
P(reach draft position 4)
= 0.3^4
= 0.0081
~~~

Later proposal positions rarely survive, so their expected progress contribution is tiny while their cost still exists.

## Why p=0.60 has an optimum

Expected progress：

~~~text
D=2 → 1.960
D=4 → 2.306
D=8 → 2.475
~~~

Progress keeps increasing, but cost：

~~~text
1.32 → 1.56 → 2.04
~~~

increases faster after a point.

## Why p=0.90 rewards longer drafts

Long accepted prefixes are common enough that target batched verification amortizes across much more sequence progress.

## Boundary

Real speculative decoding has：

- correlated token acceptance；
- target correction token details；
- sampling/rejection rules；
- dynamic draft length；
- tree/block proposal methods；
- hardware-specific verification scaling；
- KV/memory overhead；
- continuous batching interactions。

Use Experiment 16 for real Evidence。
