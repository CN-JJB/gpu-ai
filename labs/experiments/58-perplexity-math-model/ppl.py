#!/usr/bin/env python3
import math

BASE=[0.5,0.25,0.125,0.5]
CAND=[0.48,0.22,0.10,0.45]

def metrics(ps):
    if any(p<=0 or p>1 for p in ps):
        raise ValueError("probabilities must be in (0,1]")
    nll=[-math.log(p) for p in ps]
    ce=sum(nll)/len(nll)
    return nll,ce,math.exp(ce)

def show(name,ps):
    nll,ce,ppl=metrics(ps)
    print(name)
    print("p:",ps)
    print("NLL:",[round(x,9) for x in nll])
    print(f"CE: {ce:.9f}")
    print(f"PPL: {ppl:.9f}")
    print()
    return ce,ppl

def main():
    bce,bppl=show("baseline",BASE)
    cce,cppl=show("candidate",CAND)
    print(f"delta CE: {cce-bce:.9f}")
    print(f"PPL ratio candidate/base: {cppl/bppl:.9f}")

if __name__=="__main__":
    main()
