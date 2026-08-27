#!/usr/bin/env python3
import hashlib,json

SPECIALS=[
    "<|assistant|>",
    "<|system|>",
    "<|user|>",
    "<BOS>",
    "<EOS>",
]
SPECIALS=sorted(SPECIALS,key=len,reverse=True)

MESSAGES=[
    {"role":"system","content":"Answer briefly."},
    {"role":"user","content":"Hello!"},
]

def tokenize(text,auto_bos=False):
    out=[]
    if auto_bos:
        out.append("<BOS>")
    i=0
    while i<len(text):
        matched=None
        for sp in SPECIALS:
            if text.startswith(sp,i):
                matched=sp
                break
        if matched:
            out.append(matched)
            i+=len(matched)
            continue
        ch=text[i]
        for b in ch.encode("utf-8"):
            out.append(f"BYTE_{b:02X}")
        i+=1
    return out

def sha(data):
    return hashlib.sha256(data).hexdigest()

def render_a():
    return (
        "<BOS>"
        "<|system|>\nAnswer briefly.<EOS>\n"
        "<|user|>\nHello!<EOS>\n"
        "<|assistant|>\n"
    )

def render_b():
    return (
        "<BOS>"
        "### System:\nAnswer briefly.\n\n"
        "### User:\nHello!\n\n"
        "### Assistant:\n"
    )

def report(name,text):
    ids=tokenize(text)
    print(f"=== {name} ===")
    print(text.replace("\n","\\n"))
    print(f"rendered bytes: {len(text.encode('utf-8'))}")
    print(f"rendered SHA256: {sha(text.encode('utf-8'))}")
    print(f"toy token count: {len(ids)}")
    print(f"toy token SHA256: {sha(json.dumps(ids,separators=(',',':')).encode())}")
    print(f"first tokens: {ids[:12]}")
    print()
    return ids

def main():
    a=render_a()
    b=render_b()
    ta=report("template A",a)
    tb=report("template B",b)

    dup=tokenize(a,auto_bos=True)
    print("=== duplicate-BOS simulation ===")
    print(f"normal count: {len(ta)}")
    print(f"auto-BOS count: {len(dup)}")
    print(f"first two tokens: {dup[:2]}")
    print()
    print("Same message JSON:")
    print(json.dumps(MESSAGES,ensure_ascii=False,separators=(",",":")))

if __name__=="__main__":
    main()
