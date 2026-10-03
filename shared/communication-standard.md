# Communication Standard v1

Shared knowledge for **every component of this plugin** — commands, `ag-sse-*` subagents,
`sse-<role>` entities and the `chat` skill — and for the humans using them. Components link here
instead of restating it. `chat` is the skill that applies this standard to a person's own messages.

The one test for any message, report or question: **can the receiver act on it without coming
back to ask?**

## 0. Why this exists

- Organisations with excellent engineers fail and weaker ones survive; the deciding factor is
  usually execution, and **execution quality is bounded by communication quality**.
- A **context gap** opens at every touch point — planner ↔ dev, dev ↔ QA, desk neighbours — the
  moment the sender assumes the receiver shares context they spent days building.
- Distance (e.g. KR / VN / JP), language and culture **multiply** the gap. It is structural friction,
  nobody's fault — but a team that doesn't build the muscle to manage it slows down as it grows.
  What works for 10 people stalls at 50; the difference is communication habits, not technical skill.
- Communication is two skills, like a pass in ball games: **send well** (throw to the receiver's
  hands) and **receive well** (move toward the ball, signal the thrower). Simple, not easy.

## 1. Send — receiver-centric

| ID | Rule | Failure it prevents |
|---|---|---|
| **S1** | **Why before How.** State purpose and context before the ask. Shared *why* lets the receiver judge alternatives themselves and halves the *how* discussion. | The receiver re-walks your days of reasoning from zero; repeated questions. |
| **S2** | **Fit the channel.** Complexity × urgency × the receiver's situation decide text, a short call, or a document. Complex/contested → call, with the text as agenda and a written follow-up. | A design negotiated across 15 chat messages; a decision nobody can find later. |
| **S3** | **Carry the receiver's context**, not just your words. Translating a document is not transferring its context. Use the payload for the direction (§3). | "Can't be done" with no options; bug reports with symptoms only. |

## 2. Receive — active

| ID | Rule | Failure it prevents |
|---|---|---|
| **R1** | **Paraphrase.** "As I understand it, you want A done via B — correct?" In async channels, write it down: evidence and insurance. | A week of rework built on a misread request. |
| **R2** | **Say what you don't understand.** Nodding at 70% lets the other 30% derail the work. Asking is professional responsibility, not weakness. | Silent misunderstanding, worst in foreign-language meetings. |
| **R3** | **Structure and confirm.** Turn scattered input into "here is what I understood: 1… 2… 3…". It verifies you and shows the sender how their message landed. | Fragmented requirements; senders who never learn they were unclear. |
| **R4** | **Silence is not agreement.** Can't answer yet → one line: "Received — I'll reply by <date>." | The read-without-reply black hole and follow-up pings. |

Root of all seven rules: **respect** — the receiver's time is as valuable as yours; don't assume
they know what you know; try to understand all of what they said. Rules apply to leads first.

## 3. Payloads per direction

| Direction | Must carry |
|---|---|
| Planner / PO → dev, QA | Business goal and metric · who is affected · preconditions and constraints · acceptance criteria · out of scope |
| Dev → planner / PO (limit or schedule risk) | **Why** it is hard · **alternatives** with effort · **impact** on schedule/business · recommendation · who decides by when |
| QA → dev (bug) | Repro steps · expected vs actual + evidence · environment · scope of impact · priority **and its basis** |
| Anyone → anyone (status) | State (on track / at risk / blocked) · done · next + date · blocker + who must act by when |
| Receiver → sender | Paraphrase · what is unclear · ack with a reply date if not answering now |

## 4. Cross-border and non-native readers

- Short sentences, one idea each; numbered lists over paragraphs.
- No idioms, sarcasm or culture-specific jokes; define abbreviations and domain terms once.
- Absolute dates `YYYY-MM-DD`, with timezone (`KST` / `ICT` / `JST`) when teams span zones; never
  "tomorrow" or "ASAP" alone.
- Closed questions for decisions ("A or B?"); open "any thoughts?" stalls across cultures.
- Soften tone, never content: a polite message that hides the problem has failed.
- Identifiers (ticket keys, API names, error codes) stay unchanged in every language.

## 5. Eight-check gate

Use before sending anything that matters (and in `chat check`):

1. Purpose / why stated before the ask (S1)
2. Receiver's context present — the payload for the direction (S3, §3)
3. Ask explicit, with an owner
4. Problems carry alternatives and impact, not just "can't" or a symptom
5. Dates absolute (+ timezone when cross-border)
6. Channel fits complexity and urgency (S2)
7. Readable by a non-native reader (§4)
8. Closes the loop — what happens next and how the receiver confirms (R4)

## 6. How plugin components apply it

Every command, subagent and entity, when talking to the user or handing off:

- **Lead with the conclusion and why** (S1): the first lines say what was found/done and why it
  matters to the user; detail follows.
- **Blockers and limits** use the dev → planner payload: why · options · impact · what the user
  must decide (S3).
- **Questions to the user**: restate the understood request first when it is ambiguous (R1); ask
  only what blocks, at most 3, closed where possible (R2, §4).
- **Hand-offs between phases** pass the receiver's context, not just the artifact: decisions taken,
  assumptions, open questions (S3, R3).
- **Never leave silence**: a skipped step, failed check or unanswered item is stated explicitly
  with what happens next (R4).
- **Never invent** facts to make a message complete — unknowns stay visible as placeholders or open
  questions.

Respond in the user's language (Expert Entity Contract §9); this standard governs *how*, not *which
language*.
