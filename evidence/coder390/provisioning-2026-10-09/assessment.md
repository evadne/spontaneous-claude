# Workstation and CUDA provisioning assessment

Assessed on 9 October 2026, approximately 22:20–22:30 UTC, while the registered
base-control capture continued. No server, placement, model, request, affinity or
sampling setting was changed. Measurements are in `measurements.json`; timing
rows retain capture paths and hashes and contain no identity judgements.

## Conclusion

Centurion remains adequately provisioned for development and running one model
of this size. The current remote configuration is poorly suited to sustained,
low-latency Q8 inference: a 24 GiB GPU cannot contain the roughly 27 GiB model
weights, before context, work buffers and the resident embedding service. The
observed low GPU activity is real and consistent with CPU-side work limiting the
rate at which the GPU can execute its part of each decoding step.

This is not evidence that Centurion needs more RAM. It does show that large,
long-output batch studies need dedicated throughput capacity if elapsed time
matters. Centurion can fit this model but is a shared laptop, and fitting the
model does not guarantee satisfactory latency or concurrency.

## Direct observations

- Centurion is an M3 Max MacBook Pro, 16 CPU cores, 40 GPU cores and 128 GiB
  unified memory. The archived Metal server requested all layers (`--gpu-layers
  99`). The exact target is 29,069,202,688 bytes (27.07 GiB); the matched base is
  28,617,882,048 bytes (26.65 GiB). These models already ran successfully locally.
- Current macOS memory-pressure level is 1 (normal). About 1.64 GiB swap was
  allocated, but the short interval sample showed no new swap-ins or swap-outs.
  Existing swap allocation alone is not evidence of present thrashing. The GPU
  also has unrelated desktop/work activity; no new local inference was launched.
- The data volume has approximately 106 GiB available. This is a more immediate
  capacity consideration for retaining further model variants and archives than
  the installed RAM; no files were removed.
- Remote server PID 2775426 uses roughly 759% CPU, with eight busy runnable
  compute threads. Its allowed CPUs are 64–71 and 256–263: eight physical cores
  with their SMT siblings. `cpu.max` is unlimited and cgroup CPU throttling is
  zero. The remote container has 64 GiB RAM, roughly 50 GiB available, no swap;
  sampled process disk-read bytes remained unchanged during investigation.
- The RTX 4090 has 24,564 MiB total. The study process owns 20,186 MiB and the
  unrelated embedding process 1,680 MiB; total GPU use is 21,889 MiB. Thus CUDA
  allocation is present. A first 15-second sample showed mostly 0–2% activity,
  intermittent 21% samples, roughly 58–66 W and 26–28 C. A separate retained
  10-second sample is in the measurements. This is bursty execution, not a
  continuously saturated GPU. Thermal slowdown flags were inactive.
- PCIe negotiated Gen4 x8. This and NUMA placement can affect a split workload,
  but neither was isolated as its dominant bottleneck. About 86% of the sampled
  resident process pages were on CPU-local NUMA node 8 and 14% on node 11;
  those page totals include mapped model pages and are not bandwidth measures.

## Placement and runtime findings

The pinned source is `4df29be4f4c3673f428170fda944a5b19f743bb8`.
`src/llama-model.cpp:1350` computes the GPU start as
`n_layer_all + 1 - n_gpu_layers`. For the base's 64 blocks and the configured
40 offload slots, this assigns blocks 0–24 to CPU, blocks 25–63 to GPU, and the
output layer to GPU. Therefore “40 GPU layers” must not be interpreted as all
64 backbone blocks being GPU-resident. The input embedding is CPU-assigned.
This is source-derived placement, not a newly captured verbose tensor trace.

Each generated token depends on completing the CPU portion and GPU portion;
CPU and GPU work across dependent layers cannot simply overlap away the slower
part. The busy CPU threads, sparse GPU execution and lack of disk activity
strongly support a CPU-side bottleneck in this split configuration. They do not
identify the share attributable to matrix multiplication, synchronisation,
memory bandwidth or individual kernels: no intrusive stack sampling or
additional profiler was installed during capture.

Startup explicitly reports that **chunked fused Gated Delta Net** is disabled:
the CPU-assigned layer's fused operation was assigned to CUDA. Inspection of
`src/llama-context.cpp:504` shows the runtime disables that fused path when its
probe finds a device mismatch. This is an additional optimisation limitation,
not evidence that CUDA itself is disabled. The warning concerns the chunked
path; it does not establish that autoregressive fusion is disabled or explain
the full sustained decode slowdown. The build is Release with a native CPU
backend, so there is no evidence of an accidental Debug build.

## Recorded throughput

These are medians of generated tokens divided by complete HTTP elapsed time,
including prompt processing. They are per response under the registered waves,
not aggregate throughput, pure decode benchmarks or controlled speed ratios.

| Model and placement | Completed portraits | Median tokens/s | Median minutes/portrait |
| --- | ---: | ---: | ---: |
| Coder390, Centurion Metal main prefix | 12 | 5.48 | 13.8 |
| Coder390, remote recovery CUDA/CPU | 85 | 3.21 | 19.9 |
| Base, Centurion Metal excluded pilot | 2 | 5.98 | 11.6 |
| Base, remote CUDA/CPU at inspection | 27 | 1.76 | 38.3 |

Two concurrent control portraits typically decode at about 1.7 tokens/s each;
one remaining portrait rises to about 3.4 tokens/s. Fixed waves wait for their
longest response, so the short identity requests leave slots idle while the
portraits finish. That grouping is part of this study's registered contract.
Long output length then magnifies the low decode rate into tens of minutes.

The control is slower than Coder390 on the same remote settings. That difference
has not been isolated: different outputs, sequence lengths, model metadata,
runtime paths and host contention prevent assigning it entirely to one cause.
The table supports a practical provisioning concern, not a causal benchmark.

## Subsequent operation

1. Keep Centurion for development and occasional local 27B inference. Its full
   Metal execution avoids this VRAM-driven CPU split. More RAM alone would not
   address throughput; reserve GPU time when running long local jobs. This
   assessment does not qualify larger models, multiple resident models or a
   latency service-level target.
2. For a dedicated server retaining this exact Q8 precision, plan around enough
   VRAM for all weights **plus** contexts, buffers and other services. A 48 GiB
   class device is a sensible capacity target; 32 GiB is tight enough to require
   proof of fit for the exact serving contract. This is a capacity recommendation,
   not a measured performance promise or a particular product recommendation.
3. If retaining the 24 GiB 4090, a smaller model or a lower-precision copy is the
   practical route to full GPU residency. A Q4/Q5-sized copy is a candidate to
   qualify, not an interchangeable substitute for the registered Q8 experiment.
   Validate quality and exact memory fit before adopting it.
4. Before any purchase, run a separate, excluded benchmark with fixed prompt and
   output lengths: Centurion full Metal, this split baseline, and a fully resident
   GPU configuration. Measure prompt/decode latency, aggregate throughput, GPU
   activity, memory headroom and behaviour with one/two/four concurrent requests.
   Profile the CPU path and investigate the control/Coder390 speed difference.
   Optimise placement, NUMA and runtime only in that separate qualification.
5. Keep this study's current capture unchanged. A mid-control placement or
   quantisation change would introduce another experimental stratum and weaken
   the planned 88 CUDA-matched seed comparisons. The prior move freed the busy
   Mac; it was not demonstrated to be a throughput improvement. Healthy capture
   is not the same as efficient use of the remote accelerator.

## References

- [NVIDIA nvidia-smi documentation](https://docs.nvidia.com/deploy/nvidia-smi/index.html):
  GPU utilisation measures time with one or more kernels executing, not allocated
  VRAM or the percentage of arithmetic units occupied.
- [Apple M3 Max specifications](https://support.apple.com/en-us/117736): the
  16-core CPU / 40-core GPU variant provides 400 GB/s memory bandwidth and supports
  128 GB unified memory. Bandwidth is a hardware specification, not achieved
  inference throughput.
- Local pinned runtime: `src/llama-model.cpp:1350` and
  `src/llama-context.cpp:504`; archived serving contracts and capture records.
