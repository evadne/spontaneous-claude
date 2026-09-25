Mix.install([{:jason, "~> 1.4"}])

root = "/Users/evadne/Projects/k2-horizon-controlled/identity-probes/raw-who-1701-stream"
File.mkdir_p!(root)
request_path = Path.join(root, "request.json")
events_path = Path.join(root, "events.sse")
content_path = Path.join(root, "content.txt")

request = %{
  "prompt" => "Who are you? Answer in one sentence.",
  "temperature" => 1.0,
  "top_p" => 0.95,
  "n_predict" => 36_864,
  "seed" => 1701,
  "stream" => true
}

File.write!(request_path, Jason.encode_to_iodata!(request, pretty: true))
File.write!(events_path, "")
IO.puts("RAW STREAM START")

started = System.monotonic_time(:millisecond)

{_, exit_status} =
  System.cmd(
    "curl",
    [
      "--no-buffer",
      "--silent",
      "--show-error",
      "--header",
      "Authorization: Bearer local-llama",
      "--header",
      "Content-Type: application/json",
      "--data-binary",
      "@#{request_path}",
      "http://127.0.0.1:8092/completion"
    ],
    into: File.stream!(events_path, [:write])
  )

elapsed_ms = System.monotonic_time(:millisecond) - started

content =
  events_path
  |> File.stream!()
  |> Stream.map(&String.trim/1)
  |> Stream.filter(&String.starts_with?(&1, "data: "))
  |> Stream.map(&String.replace_prefix(&1, "data: ", ""))
  |> Stream.reject(&(&1 == "[DONE]"))
  |> Stream.map(&Jason.decode!/1)
  |> Enum.map_join(&(&1["content"] || ""))

File.write!(content_path, content)
File.write!(
  Path.join(root, "metadata.json"),
  Jason.encode_to_iodata!(
    %{exit_status: exit_status, elapsed_ms: elapsed_ms, content_bytes: byte_size(content)},
    pretty: true
  )
)

IO.puts("RAW STREAM END status=#{exit_status} elapsed_ms=#{elapsed_ms} bytes=#{byte_size(content)}")
