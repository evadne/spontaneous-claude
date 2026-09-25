alias Athanor.Message.Assistant

root = Path.expand("~/Projects/orcasaq-2-investigation/portrait")
{assistant, _events} = root |> Path.join("1-response.term") |> File.read!() |> :erlang.binary_to_term()
answer = Assistant.compute_text(assistant) || ""
File.write!(Path.join(root, "1-answer.txt"), answer)
File.write!(Path.join(root, "1-assistant.txt"), inspect(assistant, pretty: true, limit: :infinity))

proxy = Path.expand("~/Projects/orcasaq-2-investigation/raw/proxy/0006.metadata.json")
elapsed = proxy |> File.read!() |> Jason.decode!() |> Map.fetch!("elapsed_ms")

File.write!(
  Path.join(root, "1-metadata.json"),
  Jason.encode_to_iodata!(%{
    elapsed_ms: elapsed,
    stop_reason: assistant.stop_reason,
    has_visible_answer: answer != "",
    node: node(),
    recovered_from_response_term: true
  }, pretty: true)
)

:ok
