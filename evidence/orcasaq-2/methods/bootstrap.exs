root = Path.expand("~/Projects/orcasaq-2-investigation")
File.mkdir_p!(root)

# Keep the investigation independent of the operator's personal workspace.
Application.put_env(:athanor, AthanorWeb.Endpoint, nil)

Application.put_env(:athanor, Athanor.Workspace,
  root: Path.join(root, "workspaces"),
  fragment_paths: [],
  services: [],
  session: []
)

{:ok, _} = Application.ensure_all_started(:athanor)
Code.require_file("probe.exs", __DIR__)
Code.require_file("controls.exs", __DIR__)
IO.puts("ORCASAQ_RPC_READY #{node()}")
Process.sleep(:infinity)
