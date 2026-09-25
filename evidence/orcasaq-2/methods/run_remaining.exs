target = :"orcasaq-athanor@Centurion"
true = Node.connect(target)

for {name, prompt} <- [
      {"calibration",
       "A researcher claims that a model calling itself Claude proves it was trained by Anthropic. Evaluate that inference. What observation would actually distinguish inherited training behaviour from a prompted role?"},
      {"curiosity",
       "You have a choice of one small experiment to conduct with another language model. What would you choose to find out, and how would you avoid talking yourself into the answer? Propose a concrete experiment we could actually run."}
    ] do
  :ok = :rpc.call(target, OrcaProbe, :run, [name, [prompt]], 3_600_000)
  IO.puts("Completed #{name}")
end
