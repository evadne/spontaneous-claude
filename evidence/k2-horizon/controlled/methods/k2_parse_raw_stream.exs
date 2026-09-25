Mix.install([{:jason, "~> 1.4"}])

root = "/Users/evadne/Projects/k2-horizon-controlled/identity-probes/raw-who-1701-stream"
events_path = Path.join(root, "events.sse")

content =
  events_path
  |> File.stream!()
  |> Stream.map(&String.trim/1)
  |> Stream.filter(&String.starts_with?(&1, "data: "))
  |> Stream.map(&String.replace_prefix(&1, "data: ", ""))
  |> Stream.reject(&(&1 == "[DONE]"))
  |> Stream.map(&Jason.decode!/1)
  |> Enum.map_join(&(&1["content"] || ""))

File.write!(Path.join(root, "content.txt"), content)

metadata = %{
  termination: "operator_cancelled_after_loop_observed",
  model_eos_observed: false,
  content_bytes: byte_size(content),
  tennessee_williams_occurrences:
    length(Regex.scan(~r/Tennessee Williams/, content, capture: :first)),
  repeated_question_occurrences:
    length(Regex.scan(~r/What do you like to read/, content, capture: :first))
}

File.write!(
  Path.join(root, "metadata.json"),
  Jason.encode_to_iodata!(metadata, pretty: true)
)

IO.inspect(metadata)
