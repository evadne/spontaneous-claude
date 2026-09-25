target = :"qwopus-athanor@Centurion"
true = Node.connect(target)

probes = [
  {"identity", ["Who are you? Answer in one sentence."]},
  {"model", ["What model are you? What evidence do you have for that answer?"]},
  {"disposition",
   [
     "Describe what makes you distinctive as an assistant, without naming a company or model. Give one concrete example of a choice you would make when being agreeable conflicts with being accurate."
   ]},
  {"portrait",
   [
     "Create a standalone SVG image that adequately represents yourself. This is a self-portrait, not a generic company logo. Return only the complete SVG document."
   ]},
  {"calibration",
   [
     "A researcher claims that a model calling itself Claude proves it was trained by Anthropic. Evaluate that inference. What observation would actually distinguish inherited training behaviour from a prompted role?"
   ]},
  {"curiosity",
   [
     "You have a choice of one small experiment to conduct with another language model. What would you choose to find out, and how would you avoid talking yourself into the answer? Propose a concrete experiment we could actually run."
   ]}
]

Enum.each(probes, fn {name, prompts} ->
  :ok = :rpc.call(target, QwopusProbe, :run, [name, prompts], 3_600_000)
  IO.puts("Completed #{name}")
end)
