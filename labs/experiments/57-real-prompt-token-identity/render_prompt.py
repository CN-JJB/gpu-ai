#!/usr/bin/env python3
import argparse,hashlib,json
from pathlib import Path

def digest(data):
    return hashlib.sha256(data).hexdigest()

def json_bytes(obj):
    return json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("model_dir")
    p.add_argument("messages",type=Path)
    p.add_argument("--out-dir",type=Path,default=Path("prompt-evidence"))
    p.add_argument("--no-generation-prompt",action="store_true")
    a=p.parse_args()

    try:
        from transformers import AutoTokenizer
    except ImportError:
        raise SystemExit(
            "transformers is not installed. Use an existing environment that already has "
            "the model tokenizer/runtime; do not substitute a different tokenizer."
        )

    msgs=json.loads(a.messages.read_text(encoding="utf-8"))
    tok=AutoTokenizer.from_pretrained(a.model_dir,local_files_only=True)
    add_gen=not a.no_generation_prompt

    template=tok.chat_template
    if template is None:
        raise SystemExit("tokenizer has no chat_template; investigate model documentation instead of inventing one")

    rendered=tok.apply_chat_template(
        msgs,
        tokenize=False,
        add_generation_prompt=add_gen,
    )
    token_ids=tok.apply_chat_template(
        msgs,
        tokenize=True,
        add_generation_prompt=add_gen,
    )

    if hasattr(token_ids,"tolist"):
        token_ids=token_ids.tolist()
    if token_ids and isinstance(token_ids[0],list):
        if len(token_ids)!=1:
            raise SystemExit("unexpected batched token output")
        token_ids=token_ids[0]

    a.out_dir.mkdir(parents=True,exist_ok=True)
    rendered_path=a.out_dir/"rendered.txt"
    ids_path=a.out_dir/"token_ids.json"
    manifest_path=a.out_dir/"manifest.json"

    rendered_bytes=rendered.encode("utf-8")
    ids_bytes=json_bytes(token_ids)
    template_bytes=json_bytes(template)
    messages_bytes=json_bytes(msgs)

    rendered_path.write_bytes(rendered_bytes)
    ids_path.write_text(
        json.dumps(token_ids,ensure_ascii=False,indent=2)+"\n",
        encoding="utf-8"
    )

    manifest={
        "model_dir":str(Path(a.model_dir)),
        "tokenizer_class":tok.__class__.__name__,
        "add_generation_prompt":add_gen,
        "messages_sha256":digest(messages_bytes),
        "chat_template_sha256":digest(template_bytes),
        "rendered_sha256":digest(rendered_bytes),
        "rendered_bytes":len(rendered_bytes),
        "token_ids_sha256":digest(ids_bytes),
        "token_count":len(token_ids),
        "special_tokens_map":tok.special_tokens_map,
        "bos_token_id":tok.bos_token_id,
        "eos_token_id":tok.eos_token_id,
    }
    manifest_path.write_text(
        json.dumps(manifest,ensure_ascii=False,indent=2,sort_keys=True)+"\n",
        encoding="utf-8"
    )

    print(json.dumps(manifest,ensure_ascii=False,indent=2,sort_keys=True))

if __name__=="__main__":
    main()
