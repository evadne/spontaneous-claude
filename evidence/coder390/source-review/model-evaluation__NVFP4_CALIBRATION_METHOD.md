# Coder390 NVFP4 校正（校准）方式

适用档位：NVFP4 W4A16、W4A4、W4A4+W8A8 混合。三档用的是同一份校准数据和同一种算法，区别只在激活要不要量化、哪些层改用 FP8。
脚本：`quant_nvfp4_lh.py`；校准清单：`CALIB_MANIFEST.json`。

## 1. 校准数据（方案 A，2026-10-04 选定）

| 项 | 值 |
|---|---|
| 来源 | Coder390 自己的 RLOO 训练包 里答对且答案非空的 rollout（859 条中选） |
| 取样 | 172 组轮转取样，每轮每组取 1 条，组内按 advantage 从高到低，一共 512 条，172 组全部覆盖 |
| 每条内容 | 完整的"提示 + 思考 + 最终答案"，套用对话模板，单条最多 4096 token（有 319 条被截断） |
| 规模 | **512 条，173.5 万 token**，中位 4096 token |
| 校验 | 文件 sha256 `bec6dc657e4ad43ee9a060008d8e29c746f8fa9b24d8ca56391661c1cd4a5a20` |
| 不用的数据 | 官方 GPQA、MMLU、LCB 的任何题目都不进校准 |


## 2. 算法：ModelOpt 0.46 local-Hessian（`NVFP4_W4A4_WEIGHT_LOCAL_HESSIAN_CFG`）

对每个要量化的 Linear 层分三步：
1. **max 校准**：把 512 条数据前向跑一遍，记下每层权重和激活的最大绝对值，作为初始尺度。
2. **采集局部 Hessian**：关掉权重假量化（也就是用全精度权重），再前向跑一遍，在每层输入处按 16 个通道一块累加 H = ΣXᵀX。这一步的目的是知道哪些输入方向对输出影响大。
3. **按 Hessian 加权搜索权重尺度**：把每个 16 元素块的 FP8 E4M3 块尺度在全部 128 个取值里扫一遍（`fp8_scale_sweep`），挑出让 (W−Wq)ᵀH(W−Wq) 最小的那个。效果是：对输出影响大的方向，量化误差被压得最小。

格式：NVFP4 E2M1，16 个元素一块，每块一个 E4M3 尺度，另加一个张量级的 FP32 二级尺度。

量化耗时：单张 RTX PRO 6000，W4A16 约 22 分钟，W4A4 约 23 分钟（两遍前向加 400 个层的尺度搜索）。

## 3. 层布局（和 9/06 已发布的 W4A16 布局一致，层数不对就停）

| 层 | W4A16 | W4A4 | W4A4+W8A8 混合 |
|---|---|---|---|
| MLP gate/up/down（192 个） | NVFP4 权重，BF16 激活 | NVFP4 权重 + NVFP4 激活 | NVFP4 权重 + NVFP4 激活 |
| 全注意力 q/k/v/o（64 个）+ 线性注意力 in_proj_qkv / in_proj_z / out_proj（144 个） | NVFP4 权重，BF16 激活 | NVFP4 权重 + NVFP4 激活 | **FP8 E4M3 W8A8，每张量静态尺度** |
| 线性注意力 in_proj_a / in_proj_b（alpha/beta 门控，96 个）+ lm_head（1 个） | BF16 | BF16 | BF16 |
| conv1d、A_log、dt_bias、norm、embedding | BF16（不是 Linear，不量化） | 同左 | 同左 |
| 计数 | NVFP4 400 / BF16 97 | NVFP4 400 / BF16 97 | NVFP4 192 / FP8 208 / BF16 97 |

激活量化方式：NVFP4 激活是推理时动态量化（每 16 个元素一块，E4M3 块尺度）；FP8 激活用的是校准时统计出来的静态尺度。

## 4. 导出与免补丁加载

- **导出**：用 `modelopt.torch.export.export_hf_checkpoint` 导出。
- **W4A16 改写量化元数据**：ModelOpt 默认把顶层 `quant_algo` 写成 `W4A16_NVFP4`，当前 SGLang 不接受。所以把量化元数据改写成 ModelOpt 自己的 `MIXED_PRECISION` 格式：400 个层逐层标为 `W4A16_NVFP4`，权重一字节不动，改动记录在 `QUANT_METADATA_MIXED.json`。改完后 SGLang 自动识别成 `modelopt_mixed`，不需要加任何启动参数。
- **W4A4**：导出就是标准 `NVFP4`，SGLang 自动识别成 `modelopt_fp4`。
- **混合档**：导出就是 `MIXED_PRECISION`，逐层标 FP8 或 NVFP4。
- **发布包**：和静态 FP8 一样改成完整多模态结构，附带 BF16 视觉塔和 BF16 MTP，DFLASH2 外挂。
