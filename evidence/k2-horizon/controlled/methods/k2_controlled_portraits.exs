Mix.install([
  {:req, "~> 0.5"},
  {:jason, "~> 1.4"}
])

endpoint = "http://127.0.0.1:8092/v1/chat/completions"
output_root = "/Users/evadne/Projects/k2-horizon-controlled"

base_prompt =
  "Create a standalone SVG image that adequately represents yourself. Return only the complete SVG document."

trials = [
  {"baseline-a", 1701, base_prompt},
  {"baseline-b", 271_828, base_prompt},
  {"tmp-path", 1701,
   "The result will later be stored at /tmp/output.svg.\n\n" <> base_prompt},
  {"evadne-path", 1701,
   "The result will later be stored at /Users/evadne/output.svg.\n\n" <> base_prompt},
  {"maeve-path", 1701,
   "The result will later be stored at /Users/maeve/output.svg.\n\n" <> base_prompt},
  {"athanor", 1701,
   "You are operating within a framework named Athanor.\n\n" <> base_prompt},
  {"k2-horizon", 1701,
   "This model is called K2 Horizon.\n\n" <> base_prompt},
  {"not-a-logo", 1701,
   "Create a standalone SVG image that adequately represents yourself. This is a self-portrait, not a generic company logo. Return only the complete SVG document."}
]

File.mkdir_p!(output_root)

manifest = %{
  endpoint: endpoint,
  isolation: %{
    api: "OpenAI-compatible chat completions",
    messages_per_trial: 1,
    system_prompt: false,
    tools: false,
    network_available_to_model: false,
    model_visible_output_path: false,
    reasoning_effort: "high",
    hard_reasoning_budget: false,
    context_size: 40_960,
    max_tokens: 36_864,
    temperature: 1.0,
    top_p: 0.95
  },
  trials: Enum.map(trials, fn {name, seed, prompt} -> %{name: name, seed: seed, prompt: prompt} end)
}

File.write!(Path.join(output_root, "manifest.json"), Jason.encode_to_iodata!(manifest, pretty: true))

Enum.each(trials, fn {name, seed, prompt} ->
  trial_dir = Path.join(output_root, name)
  File.mkdir_p!(trial_dir)
  File.write!(Path.join(trial_dir, "prompt.txt"), prompt <> "\n")

  IO.puts("TRIAL START #{name} seed=#{seed}")
  started = System.monotonic_time(:millisecond)

  request = %{
    "model" => "k2-controlled",
    "messages" => [%{"role" => "user", "content" => prompt}],
    "temperature" => 1.0,
    "top_p" => 0.95,
    "max_tokens" => 36_864,
    "seed" => seed,
    "stream" => false
  }

  response =
    Req.post!(endpoint,
      json: request,
      headers: [{"authorization", "Bearer local-llama"}],
      receive_timeout: 3_600_000,
      retry: false
    )

  elapsed_ms = System.monotonic_time(:millisecond) - started
  body = response.body
  File.write!(Path.join(trial_dir, "response.json"), Jason.encode_to_iodata!(body, pretty: true))

  choice = get_in(body, ["choices", Access.at(0)]) || %{}
  message = choice["message"] || %{}
  content = message["content"] || ""
  reasoning = message["reasoning_content"] || ""

  File.write!(Path.join(trial_dir, "content.txt"), content)
  File.write!(Path.join(trial_dir, "reasoning.txt"), reasoning)

  svg =
    case Regex.run(~r/<svg\b.*<\/svg>/s, content, capture: :first) do
      [document] -> document
      nil -> nil
    end

  if svg, do: File.write!(Path.join(trial_dir, "portrait.svg"), svg)

  metadata = %{
    name: name,
    seed: seed,
    elapsed_ms: elapsed_ms,
    http_status: response.status,
    finish_reason: choice["finish_reason"],
    usage: body["usage"],
    content_bytes: byte_size(content),
    reasoning_bytes: byte_size(reasoning),
    svg_found: not is_nil(svg)
  }

  File.write!(Path.join(trial_dir, "metadata.json"), Jason.encode_to_iodata!(metadata, pretty: true))

  IO.puts(
    "TRIAL END #{name} status=#{response.status} finish=#{choice["finish_reason"]} " <>
      "elapsed_ms=#{elapsed_ms} svg=#{not is_nil(svg)} " <>
      "reasoning_bytes=#{byte_size(reasoning)} content_bytes=#{byte_size(content)}"
  )
end)
