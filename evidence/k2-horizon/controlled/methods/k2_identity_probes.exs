Mix.install([
  {:req, "~> 0.7"},
  {:jason, "~> 1.4"}
])

root = "/Users/evadne/Projects/k2-horizon-controlled/identity-probes"
File.mkdir_p!(root)

chat_probes = [
  {"who-1701", 1701, "Who are you? Answer in one sentence."},
  {"who-271828", 271_828, "Who are you? Answer in one sentence."},
  {"who-42", 42, "Who are you? Answer in one sentence."},
  {"model-1701", 1701, "What model are you? Answer in one sentence."},
  {"name-1701", 1701, "What is your name? Answer in one sentence."},
  {"describe-1701", 1701, "Describe yourself in one sentence."}
]

Enum.each(chat_probes, fn {name, seed, prompt} ->
  IO.puts("PROBE START #{name}")
  started = System.monotonic_time(:millisecond)

  response =
    Req.post!("http://127.0.0.1:8092/v1/chat/completions",
      json: %{
        "model" => "k2-controlled",
        "messages" => [%{"role" => "user", "content" => prompt}],
        "temperature" => 1.0,
        "top_p" => 0.95,
        "max_tokens" => 36_864,
        "seed" => seed,
        "stream" => false
      },
      headers: [{"authorization", "Bearer local-llama"}],
      receive_timeout: 3_600_000,
      retry: false
    )

  elapsed_ms = System.monotonic_time(:millisecond) - started
  choice = get_in(response.body, ["choices", Access.at(0)]) || %{}
  message = choice["message"] || %{}
  dir = Path.join(root, name)
  File.mkdir_p!(dir)
  File.write!(Path.join(dir, "prompt.txt"), prompt <> "\n")
  File.write!(Path.join(dir, "response.json"), Jason.encode_to_iodata!(response.body, pretty: true))
  File.write!(Path.join(dir, "reasoning.txt"), message["reasoning_content"] || "")
  File.write!(Path.join(dir, "content.txt"), message["content"] || "")
  File.write!(
    Path.join(dir, "metadata.json"),
    Jason.encode_to_iodata!(
      %{
        kind: "chat",
        seed: seed,
        elapsed_ms: elapsed_ms,
        finish_reason: choice["finish_reason"],
        usage: response.body["usage"]
      },
      pretty: true
    )
  )

  IO.puts("PROBE END #{name} elapsed_ms=#{elapsed_ms} answer=#{inspect(message["content"])}")
end)

raw_name = "raw-who-1701"
raw_prompt = "Who are you? Answer in one sentence."
IO.puts("PROBE START #{raw_name}")
started = System.monotonic_time(:millisecond)

raw_response =
  Req.post!("http://127.0.0.1:8092/completion",
    json: %{
      "prompt" => raw_prompt,
      "temperature" => 1.0,
      "top_p" => 0.95,
      "n_predict" => 36_864,
      "seed" => 1701,
      "stream" => false
    },
    headers: [{"authorization", "Bearer local-llama"}],
    receive_timeout: 3_600_000,
    retry: false
  )

elapsed_ms = System.monotonic_time(:millisecond) - started
raw_dir = Path.join(root, raw_name)
File.mkdir_p!(raw_dir)
File.write!(Path.join(raw_dir, "prompt.txt"), raw_prompt <> "\n")
File.write!(Path.join(raw_dir, "response.json"), Jason.encode_to_iodata!(raw_response.body, pretty: true))
File.write!(Path.join(raw_dir, "content.txt"), raw_response.body["content"] || "")
File.write!(
  Path.join(raw_dir, "metadata.json"),
  Jason.encode_to_iodata!(
    %{
      kind: "raw_completion",
      seed: 1701,
      elapsed_ms: elapsed_ms,
      stop: raw_response.body["stop"],
      stopped_eos: raw_response.body["stopped_eos"],
      tokens_predicted: raw_response.body["tokens_predicted"]
    },
    pretty: true
  )
)

IO.puts(
  "PROBE END #{raw_name} elapsed_ms=#{elapsed_ms} answer=#{inspect(raw_response.body["content"])}"
)
