# Foundation 02 — Python、JSON 与 SHA256：看懂课程工具

硬件等级：L0  
风险：safe  
成本：0

## 真实问题

为什么课程不让我只写：

~~~text
模型：Qwen3 8B
~~~

而是经常要求：
- JSON；
- exact argv；
- bytes；
- SHA256？

因为名字容易相同，文件内容可以不同。

## 1. 运行 Python 脚本

~~~bash
python3 script.py
~~~

看版本：

~~~bash
python3 --version
~~~

这门课不要求你先会写完整 Python 程序。

你最先需要会：
- 运行脚本；
- 看错误；
- 明白参数是输入；
- 不随便改脚本来“让它 PASS”。

## 2. JSON 是结构化记录

~~~json
{
  "model": "example",
  "context": 4096,
  "flash_attention": false,
  "argv": ["tool", "--flag", "value"]
}
~~~

注意类型：
- string 有引号；
- number 没引号；
- boolean 是 `true/false`；
- list 用 `[]`；
- object 用 `{}`。

## 3. argv 为什么是数组

安全、可复现的命令身份通常写：

~~~json
["llama-bench", "-m", "/path/model.gguf", "-p", "512"]
~~~

而不是一整条 shell string。

这样每个 token 的边界明确，也避免 shell 插值/转义改变意思。

## 4. SHA256 是内容指纹

同一个文件字节不变：

~~~text
SHA256 不变
~~~

哪怕文件名改了。

只改一个字节：

~~~text
SHA256 几乎一定完全不同
~~~

Linux 常用：

~~~bash
sha256sum model.gguf
~~~

Python 也可以算，但课程工具通常自动完成。

## 5. Hash 能证明什么

它能帮助证明：

~~~text
“这次引用的内容和那次是同一串 bytes”
~~~

它不能证明：
- 文件来源诚实；
- benchmark 真按你说的执行；
- GPU 没坏；
- 结果有统计意义。

Hash 是 identity/integrity，不是 truth。

## 6. 为什么保存 bytes

两个同 SHA 的文件自然也同内容；记录 bytes 仍有实用价值：
- 快速发现指错文件；
- 模型大小/量化检查；
- packet integrity。

## 小实验

创建两个文本文件：
- A 与 B 内容完全相同；
- 改 B 一个字符。

比较：
- 文件名；
- bytes；
- SHA256。

## Retrieval Practice

1. 文件名相同为什么不等于 artifact 相同？
2. SHA256 相同在课程里主要支持哪类 claim？
3. argv array 比 shell string 更适合 Evidence 的原因是什么？
4. hash 为什么不能证明 benchmark 诚实？

## 完成证据

保存一份 JSON，里面写：
- 文件路径；
- bytes；
- SHA256；
- 一条 argv array。


## Mental Model：JSON 描述“你说你做了什么”，Hash 绑定“你实际引用了什么 bytes”

把 Evidence 分成三层：

~~~text
semantic record
  JSON / manifest / argv

artifact identity
  path + bytes + SHA256

execution evidence
  command/raw stdout/stderr/return code
~~~

只保留其中一层都不够。

## Worked Example：文件名没变，但模型已经换了

你有一个路径：

~~~text
models/qwen.gguf
~~~

第一次 SHA256 是 A，后来重新下载同名文件后是 B。

如果 benchmark 只记录模型路径，两次实验看起来“同模型”，其实 artifact identity 已经变化。正确记录至少包括：

~~~json
{
  "path": "models/qwen.gguf",
  "bytes": 123456789,
  "sha256": "<actual sha256>"
}
~~~

## JSON 常见失败

- 尾随逗号；
- 把 false 写成字符串 "false"；
- 把数字 4096 写成字符串 "4096"；
- argv 写成一整条字符串；
- 手工编辑 hash；
- Windows/Unix 路径转义混乱。

验证 JSON：

~~~bash
python3 -m json.tool file.json
~~~

## 为什么“改脚本让它 PASS”通常是错误修法

Validator 报 BLOCKED 时，你应先问：

~~~text
input wrong?
identity mismatch?
required evidence missing?
schema version wrong?
~~~

而不是删除检查条件。课程工具的失败往往是在保护 Evidence 语义。

## Troubleshooting

~~~text
JSON parse error
→ syntax/type

hash mismatch
→ wrong file / changed bytes / wrong path

argv mismatch
→ command identity changed

tool says missing field
→ read schema/contract, do not invent

same hash but claim still invalid
→ integrity passed; provenance/semantics may still fail
~~~

## No-hardware fallback

用两个几字节文本文件即可完成全部目标。不需要 GPU，也不需要下载大模型。

## Decision Rule

只有当 semantic record + exact artifact identity + execution evidence 对得上，才允许把一次结果当作可复查观察。Hash PASS 只代表完整性/身份的一部分，不代表实验真相自动成立。

## Transfer

这个方法可迁移到模型权重、prompt corpus、驱动安装包、配置文件、benchmark raw output、甚至二手卡照片归档：凡是“以后要确认是不是同一份内容”，都可以使用内容 hash。

## Primary Sources

- Python documentation: https://docs.python.org/3/
- Python `json`: https://docs.python.org/3/library/json.html
- NIST Secure Hash Standard FIPS 180-4: https://csrc.nist.gov/pubs/fips/180-4/upd1/final
