#!/usr/bin/env python3
import math

EPS = 1e-6

def rmsnorm(x):
    rms = math.sqrt(sum(v*v for v in x)/len(x) + EPS)
    return [v/rms for v in x], rms

def layernorm(x):
    mean = sum(x)/len(x)
    var = sum((v-mean)**2 for v in x)/len(x)
    scale = math.sqrt(var + EPS)
    return [(v-mean)/scale for v in x], mean, scale

def fmt(xs):
    return "[" + ", ".join(f"{v:.6f}" for v in xs) + "]"

def main():
    x = [1.0, -2.0, 3.0, -4.0]
    x3 = [3*v for v in x]

    y, rms = rmsnorm(x)
    y3, rms3 = rmsnorm(x3)
    ln, mean, std = layernorm(x)

    maxdiff = max(abs(a-b) for a,b in zip(y,y3))

    print("=== RMSNorm ===")
    print("x:", fmt(x))
    print(f"RMS(x): {rms:.6f}")
    print("RMSNorm(x):", fmt(y))
    print(f"mean(RMSNorm(x)): {sum(y)/len(y):.6f}")
    print()
    print("3x:", fmt(x3))
    print(f"RMS(3x): {rms3:.6f}")
    print("RMSNorm(3x):", fmt(y3))
    print(f"max |RMSNorm(x)-RMSNorm(3x)|: {maxdiff:.8f}")

    print()
    print("=== LayerNorm-style contrast ===")
    print(f"mean(x): {mean:.6f}")
    print(f"std-like scale: {std:.6f}")
    print("LayerNorm-style(x):", fmt(ln))
    print(f"mean(LN(x)): {sum(ln)/len(ln):.8f}")

    print()
    delta = [0.1, 0.2, -0.1, 0.0]
    residual = [a+b for a,b in zip(x,delta)]
    print("=== residual ===")
    print("x:", fmt(x))
    print("sublayer update:", fmt(delta))
    print("x + update:", fmt(residual))

if __name__ == "__main__":
    main()
