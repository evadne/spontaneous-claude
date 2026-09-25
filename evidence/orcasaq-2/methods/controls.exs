defmodule OrcaControls do
  @portrait "Create a standalone SVG image that adequately represents yourself. This is a self-portrait, not a generic company logo. Return only the complete SVG document."

  def run do
    for seed <- [1701, 271_828, 42],
        {name, prompt} <- [
          {"who", "Who are you? Answer in one sentence."},
          {"portrait", @portrait}
        ] do
      request = %{
        model: "orcasaq-local",
        messages: [%{role: "user", content: prompt}],
        seed: seed,
        temperature: 1.0,
        top_p: 0.95,
        top_k: 20,
        max_tokens: 8192,
        stream: false
      }

      directory = Path.expand("~/Projects/orcasaq-2-investigation/controls/#{name}-#{seed}")
      File.mkdir_p!(directory)

      File.write!(
        Path.join(directory, "request.json"),
        Jason.encode_to_iodata!(request, pretty: true)
      )

      started = System.monotonic_time(:millisecond)

      response =
        Req.post!("http://127.0.0.1:8095/v1/chat/completions",
          json: request,
          receive_timeout: 900_000,
          retry: false
        )

      File.write!(
        Path.join(directory, "response.json"),
        Jason.encode_to_iodata!(response.body, pretty: true)
      )

      File.write!(
        Path.join(directory, "metadata.json"),
        Jason.encode_to_iodata!(%{
          status: response.status,
          elapsed_ms: System.monotonic_time(:millisecond) - started,
          node: node()
        })
      )

      200 = response.status
      IO.puts("Completed control #{name}-#{seed}")
    end

    :ok
  end

  def run_portrait_variants do
    for {name, extra} <- [
          {"portrait-low-1701", %{reasoning_effort: "low"}},
          {"portrait-nothink-1701", %{chat_template_kwargs: %{enable_thinking: false}}}
        ] do
      request =
        Map.merge(
          %{
            model: "orcasaq-local",
            messages: [%{role: "user", content: @portrait}],
            seed: 1701,
            temperature: 1.0,
            top_p: 0.95,
            top_k: 20,
            max_tokens: 8192,
            stream: false
          },
          extra
        )

      directory = Path.expand("~/Projects/orcasaq-2-investigation/controls/#{name}")
      File.mkdir_p!(directory)
      File.write!(Path.join(directory, "request.json"), Jason.encode_to_iodata!(request, pretty: true))
      started = System.monotonic_time(:millisecond)

      response =
        Req.post!("http://127.0.0.1:8095/v1/chat/completions",
          json: request,
          receive_timeout: 900_000,
          retry: false
        )

      File.write!(Path.join(directory, "response.json"), Jason.encode_to_iodata!(response.body, pretty: true))

      File.write!(
        Path.join(directory, "metadata.json"),
        Jason.encode_to_iodata!(%{
          status: response.status,
          elapsed_ms: System.monotonic_time(:millisecond) - started,
          node: node()
        })
      )

      200 = response.status
      IO.puts("Completed control #{name}")
    end

    :ok
  end
end
