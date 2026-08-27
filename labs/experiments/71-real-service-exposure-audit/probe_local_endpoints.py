#!/usr/bin/env python3
import argparse
import os
import urllib.error
import urllib.parse
import urllib.request

ALLOWED_HOSTS={"127.0.0.1","localhost","::1"}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--base",default="http://127.0.0.1:8080")
    p.add_argument("--api-key-env")
    a=p.parse_args()

    u=urllib.parse.urlparse(a.base)
    if u.hostname not in ALLOWED_HOSTS:
        raise SystemExit(
            "This course probe is intentionally limited to localhost/loopback."
        )

    headers={}
    if a.api_key_env:
        key=os.environ.get(a.api_key_env)
        if not key:
            raise SystemExit("API key environment variable is unset")
        headers["Authorization"]="Bearer "+key

    for path in ["/health","/metrics","/slots","/v1/models"]:
        req=urllib.request.Request(a.base.rstrip("/")+path,headers=headers)
        try:
            with urllib.request.urlopen(req,timeout=5) as r:
                status=r.status
                ctype=r.headers.get("Content-Type","")
                # read and discard only a bounded prefix; never print the body
                r.read(1024)
        except urllib.error.HTTPError as e:
            status=e.code
            ctype=e.headers.get("Content-Type","") if e.headers else ""
        except Exception as e:
            print(f"{path}: ERROR {type(e).__name__}")
            continue
        print(f"{path}: HTTP {status} content-type={ctype!r}")

    print("Response bodies were intentionally not printed.")
    print("API key value, if used, was not printed.")

if __name__=="__main__":
    main()
