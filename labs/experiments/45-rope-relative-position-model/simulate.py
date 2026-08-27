#!/usr/bin/env python3
import math

def rotate(vec, pos, base=10000.0):
    if len(vec) % 2:
        raise ValueError("dimension must be even")
    d = len(vec)
    out = []
    for pair in range(d//2):
        inv_freq = base ** (-(2*pair)/d)
        angle = pos * inv_freq
        c, s = math.cos(angle), math.sin(angle)
        x0, x1 = vec[2*pair], vec[2*pair+1]
        out.extend([c*x0 - s*x1, s*x0 + c*x1])
    return out

def dot(a,b):
    return sum(x*y for x,y in zip(a,b))

def norm(a):
    return math.sqrt(dot(a,a))

def fmt(a):
    return "[" + ", ".join(f"{x:.6f}" for x in a) + "]"

def main():
    q = [1.0, 0.0, 1.0, 0.0]
    k = [0.6, 0.8, 0.3, -0.4]
    p, s, shift = 3, 7, 11

    qp = rotate(q,p)
    ks = rotate(k,s)
    qps = rotate(q,p+shift)
    kss = rotate(k,s+shift)
    k_changed = rotate(k,s+1)

    d1 = dot(qp,ks)
    d2 = dot(qps,kss)
    d3 = dot(qp,k_changed)

    print("=== norm preservation ===")
    print(f"||q||: {norm(q):.9f}")
    print(f"||R(p)q||: {norm(qp):.9f}")
    print(f"||k||: {norm(k):.9f}")
    print(f"||R(s)k||: {norm(ks):.9f}")

    print()
    print("=== relative-position dot product ===")
    print(f"positions: q={p}, k={s}, relative={s-p}")
    print(f"dot1: {d1:.9f}")
    print(f"shifted positions: q={p+shift}, k={s+shift}, relative={(s+shift)-(p+shift)}")
    print(f"dot2: {d2:.9f}")
    print(f"|dot1-dot2|: {abs(d1-d2):.12f}")

    print()
    print("=== change only key position ===")
    print(f"q={p}, k={s+1}, relative={(s+1)-p}")
    print(f"dot3: {d3:.9f}")
    print(f"|dot1-dot3|: {abs(d1-d3):.9f}")

    print()
    print("R(p)q:", fmt(qp))
    print("R(s)k:", fmt(ks))

if __name__ == "__main__":
    main()
