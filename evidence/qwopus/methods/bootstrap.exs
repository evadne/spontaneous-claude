root = Path.expand("~/Projects/qwopus-investigation")
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
IO.puts("QWOPUS_RPC_READY #{node()}")
Process.sleep(:infinity)
