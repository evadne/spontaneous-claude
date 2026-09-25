# Qwopus investigation: unrelated Matter timeout diagnostics

The full-suite run in `tests-final.log` used seed 742814 and default concurrency
(16 cases). It finished with 1646/1648 passed and 84 excluded.

The failing `Athanor.MatterTest` task-exit assertion includes decisive process
diagnostics: Matter was waiting in `gen_server:loop`, its task monitor was still
active, and the child Task was alive, waiting in `code_server:call` through
`code:ensure_loaded`, `error_handler:undefined_function`,
`Logger.Translator.maybe_normalize`, and `Task.Supervised.invoke_mfa`.

The installed Elixir 1.20.0 Task implementation logs unexpected exits before
re-raising them. Therefore the observed Matter process had not yet received its
Task DOWN because the Task had not finished its supervised crash-report path.
This is evidence of a delayed code-server interaction during logger exception
normalisation, not a swallowed DOWN in Matter. The snapshot does not identify
the requested module or explain why the code-server interaction exceeded the
one-second assertion boundary.

The sibling-crash integration test has no corresponding Task snapshot. Its
healthy sibling both emitted its result and exited; the crasher logged its
exception but did not deliver Matter DOWN within the assertion boundary.
The same crash-report delay is plausible but not proved for that case.

Existing `test/test_helper.exs` already raises the logger sync threshold and
preloads compiled application/dependency modules beneath the project build
path. It does not preload the complete Elixir/OTP standard library.

Historical context: `docs/investigations/soak/2026-05-18.md`, entry
SOAK-20260518-004, records the same exit-test symptom and introduced the
failure-only diagnostics used here. The April 8 soak report records similar
symptoms during a much longer unexplained deadlock; there is no evidence that
the old deadlock and this transient timeout have the same cause.

Targeted reproduction, without changes:

`./bin/test test/athanor/matter_test.exs test/athanor/session/matter_integration_test.exs --seed 742814`

Result: 46 passed, 1 excluded, 2.6 seconds. See `tests-matter-targeted.log`.

The full recheck is `./bin/test --seed 742814`, with ordinary default concurrency
and preload behaviour. No application code, tests, configuration, async
settings, or assertion deadlines were changed. See `tests-final-recheck.log`.

The full recheck exited successfully. No product or test change is justified
by this investigation; the captured failure remains useful evidence for a
future focused investigation of code-server delay under concurrent testing.
