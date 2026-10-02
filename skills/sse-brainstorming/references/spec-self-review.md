# Spec self-review and user review gate (architectural path)

Run after writing the spec file from [`../assets/template-spec.md`](../assets/template-spec.md),
before showing it to the user.

## Self-review — look at the spec with fresh eyes

1. **Placeholder scan** — any "TBD", "TODO", leftover `<...>`, empty sections or vague
   requirements? Fix them, or move the item to *Open questions* with an owner.
2. **Internal consistency** — do sections contradict each other? Does the architecture match the
   feature descriptions and the approved approach?
3. **Scope check** — focused enough for one implementation hand-off, or does it need decomposition?
4. **Ambiguity check** — could any requirement be read two ways? Pick one and make it explicit
   (ISO/IEC/IEEE 29148: each requirement unambiguous and verifiable).
5. **YAGNI check** — anything the user did not ask for and the goals do not need? Cut it or move
   it to *Non-goals*.

Fix issues inline. No need to re-review — fix and move on.

## Optional independent review

For a high-stakes spec, **offer** a second pass by a fresh reviewer. Only on the user's yes, dispatch
a general-purpose subagent with [`spec-document-reviewer-prompt.md`](spec-document-reviewer-prompt.md);
apply its blocking issues, list its advisory notes for the user.

## User review gate

Then ask the user to review the file:

> "Spec written to `<path>` (not committed). Please review it and tell me what to change before we
> hand it off to design/implementation."

Wait for the answer. Changes requested → edit, re-run the self-review, ask again. Proceed to the
hand-off proposal only after explicit approval. Commit the file only if the user asks.
