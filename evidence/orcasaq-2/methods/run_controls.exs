target = :"orcasaq-athanor@Centurion"
true = Node.connect(target)
:ok = :rpc.call(target, OrcaControls, :run, [], 3_600_000)
