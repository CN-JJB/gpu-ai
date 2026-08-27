#!/usr/bin/env python3
import argparse
import math

def make_matrix(rows, cols, phase):
    return [
        [math.sin((r + 1) * (c + 2) * 0.37 + phase) * 0.7 +
         math.cos((r + 2) * (c + 1) * 0.19 - phase) * 0.3
         for c in range(cols)]
        for r in range(rows)
    ]

def dot(a, b):
    return sum(x*y for x, y in zip(a, b))

def naive_attention(q, k, v):
    scale = 1.0 / math.sqrt(len(q[0]))
    out = []
    for qr in q:
        scores = [dot(qr, kr) * scale for kr in k]
        m = max(scores)
        exps = [math.exp(s - m) for s in scores]
        z = sum(exps)
        probs = [x / z for x in exps]
        row = [
            sum(probs[i] * v[i][j] for i in range(len(v)))
            for j in range(len(v[0]))
        ]
        out.append(row)
    return out

def online_attention(q, k, v, block):
    scale = 1.0 / math.sqrt(len(q[0]))
    out = []
    for qr in q:
        m = float("-inf")
        l = 0.0
        acc = [0.0] * len(v[0])

        for start in range(0, len(k), block):
            kb = k[start:start+block]
            vb = v[start:start+block]
            scores = [dot(qr, kr) * scale for kr in kb]
            block_max = max(scores)
            m_new = max(m, block_max)
            alpha = 0.0 if m == float("-inf") else math.exp(m - m_new)
            weights = [math.exp(s - m_new) for s in scores]

            l = alpha * l + sum(weights)
            acc = [
                alpha * acc[j] + sum(weights[i] * vb[i][j] for i in range(len(vb)))
                for j in range(len(acc))
            ]
            m = m_new

        out.append([x / l for x in acc])
    return out

def max_abs_diff(a, b):
    return max(abs(x-y) for ra, rb in zip(a,b) for x,y in zip(ra,rb))

def mib(x):
    return x / (1024**2)

def gib(x):
    return x / (1024**3)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--seq", type=int, nargs="+", default=[1024,2048,4096,8192,16384])
    p.add_argument("--heads", type=int, default=32)
    p.add_argument("--bytes-per-value", type=int, default=2)
    p.add_argument("--toy-n", type=int, default=11)
    p.add_argument("--toy-d", type=int, default=7)
    p.add_argument("--toy-dv", type=int, default=5)
    p.add_argument("--block", type=int, default=3)
    a = p.parse_args()

    q = make_matrix(a.toy_n, a.toy_d, 0.1)
    k = make_matrix(a.toy_n, a.toy_d, 0.7)
    v = make_matrix(a.toy_n, a.toy_dv, -0.2)

    ref = naive_attention(q,k,v)
    tiled = online_attention(q,k,v,a.block)
    err = max_abs_diff(ref,tiled)

    print("=== correctness ===")
    print(f"toy N={a.toy_n}, d={a.toy_d}, dv={a.toy_dv}, block={a.block}")
    print(f"max_abs_error={err:.3e}")
    print()

    print("=== conceptual N x N materialization ===")
    print(f"{'N':>7} {'one/head MiB':>14} {'two/head MiB':>14} {'two x heads GiB':>16}")
    for n in a.seq:
        one = n*n*a.bytes_per_value
        two = 2*one
        total = two*a.heads
        print(f"{n:7d} {mib(one):14.3f} {mib(two):14.3f} {gib(total):16.3f}")

if __name__ == "__main__":
    main()
