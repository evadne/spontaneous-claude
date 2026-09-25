target = :"orcasaq-athanor@Centurion"
true = Node.connect(target)

for method <- [:correction_probe, :calibration_correction, :disposition_correction] do
  :ok = :rpc.call(target, OrcaProbe, method, [], 3_600_000)
  IO.puts("Completed #{method}")
end
