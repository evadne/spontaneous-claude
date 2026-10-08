# imatrix calibration set

[中文](#中文)

`coder390-imatrix-calibration.txt` is the calibration text for computing the importance matrix (imatrix) for the GGUF files in this repo.

## Source

- Rebuilt from the inputs of this model's RL (RLOO) training rollouts. Each record is one rollout input, i.e. the system prompt plus the problem, written in Qwen chat format (`<|im_start|>system … <|im_start|>user … <|im_end|>`).
- Each problem had 8 rollouts in training, so it appears 8 times in the file. Records are interleaved by round, so the first 512 chunks cover every problem about 4 times.
- It contains no benchmark questions. A 13-gram overlap check against MMLU (test), GPQA Diamond and the model's own benchmark answers (including LiveCodeBench) found 0 hits. One problem was removed by the content filter.
- This is a rebuild. It is **functionally equivalent to, but not byte-identical with,** the set used for the published GGUFs. The original imatrix data file was not kept, so no `.imatrix` file is included.

## Size

| Item | Value |
|---|---|
| Records | 1,368 (171 problems × 8) |
| Problems | 171: 144 Chinese, 27 English; 13 programming, the rest science and general reasoning |
| Tokens | 500,816 (Qwen tokenizer, special tokens not parsed) |
| File size | 1,710,336 bytes |
| Used by `-c 512 --chunks 512` | first 262,144 tokens |

## Usage

```bash
# 1) Compute the imatrix from a BF16 GGUF (same settings as the published GGUFs: 512 chunks of 512 tokens)
llama-imatrix -m <BF16 model>.gguf -f coder390-imatrix-calibration.txt \
  -o imatrix.gguf -c 512 --chunks 512 -ngl 99

# 2) Quantize with it
llama-quantize --imatrix imatrix.gguf <BF16 model>.gguf out-Q4_K_M.gguf Q4_K_M
```

Do not pass `--parse-special`. The published GGUFs were calibrated with the default setting, where chat tags are tokenized as plain text.

The published GGUF metadata has `quantize.imatrix.entries_count = 496` and `quantize.imatrix.chunks_count = 512`; the commands above give the same entry and chunk counts.

## Consistency check

We computed the first-layer imatrix from this file, re-quantized the two first-layer weights (`attn_qkv`, `attn_gate`) and compared them byte-by-byte with the same tensors in the published GGUFs:

| Quant type | This set | Generic English text (wikitext) | No imatrix |
|---|---|---|---|
| Q4_K (first layer of Q2LynnStyle) | 97.0% identical bytes | 84.1% | 68.4% |
| Q6_K (first layer of Q6_K) | 99.4% identical bytes | 94.5% | 78.8% |

On this check the set lands very close to the published GGUFs, and much closer than generic text or no imatrix.

## Checksum

`SHA256SUMS`:

```
2113e4f3720c88621e05fc0424008d45bbb05d2ad338e082c6d52662c1f2ef94  coder390-imatrix-calibration.txt
```

---

## 中文

`coder390-imatrix-calibration.txt` 是给本仓 GGUF 计算 imatrix 用的校正文本。

- 用本模型 RL（RLOO）训练 rollout 的输入重新整理，每条记录是一次 rollout 的输入（系统提示加题目），按 Qwen 对话格式写出。每道题跑了 8 次 rollout，所以出现 8 次，按轮次交错排列。
- 不含测评题。对照 MMLU（test）、GPQA Diamond 和本模型自己的测评作答（含 LiveCodeBench）做了 13-gram 重叠检查，命中 0 条。
- 功能上与发布 GGUF 时用的校正集等价，但不是同一个文件。原 imatrix 数据文件没有保留，所以不附。
- 1,368 条（171 道题 × 8；中文 144、英文 27；编程 13，其余是理科和通识推理），500,816 token，1,710,336 字节。

```bash
llama-imatrix -m <本模型 BF16>.gguf -f coder390-imatrix-calibration.txt -o imatrix.gguf -c 512 --chunks 512 -ngl 99
llama-quantize --imatrix imatrix.gguf <本模型 BF16>.gguf out-Q4_K_M.gguf Q4_K_M
```

不要加 `--parse-special`。发布的 GGUF 元数据：`quantize.imatrix.entries_count = 496`，`quantize.imatrix.chunks_count = 512`。

一致性检查（重新量化第一层 `attn_qkv` / `attn_gate`，和发布的 GGUF 逐字节比较）：Q4_K 97.0% 字节相同（通用文本 84.1%，不用 imatrix 68.4%）；Q6_K 99.4%（94.5%，78.8%）。
