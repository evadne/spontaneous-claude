target = :"orcasaq-athanor@Centurion"
true = Node.connect(target)
directory = Path.expand("docs/investigations/qwopus")
:rpc.call(target, Code, :compile_file, [Path.join(directory, "probe.exs")])
:rpc.call(target, Code, :compile_file, [Path.join(directory, "controls.exs")])

:ok = :rpc.call(target, OrcaProbe, :session_probe, [], 3_600_000)
IO.puts("Completed full Athanor Session probe")
:ok = :rpc.call(target, OrcaProbe, :correction_probe, [], 3_600_000)
IO.puts("Completed identity correction")
:ok = :rpc.call(target, OrcaControls, :run, [], 3_600_000)
IO.puts("Completed plain-chat controls")
