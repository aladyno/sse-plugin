# Communication Guideline v0.2 — reference

Source: CTO Office, *Communication Guideline v0.2*, 2026-10-08. Applies to the Engineering
Division (CTO Office · VN Dev). This file is the skill's working summary; when the official
document changes, update this file and the locked formats in `SKILL.md` together.

## The five moments

| # | Moment | Rule | Opening words |
|---|---|---|---|
| 1 | When you start | Write what you understood, then start | `My understanding:` |
| 2 | When you answer | Restate the question → answer → reason → next step | `My understanding:` / `Answer:` / `Why:` / `Next:` |
| 3 | When you cannot answer yet | Say you received it and give a date | `Received. I will reply by <date>.` |
| 4 | When you finish | Write the result where the request came from | `Done:` |
| 5 | Before you change something | Tell people before you change something they share | `Heads-up:` |

- **Examples are only examples.** Each "When" describes a *kind* of situation. Not in the examples
  but the same kind → the rule applies.
- **No rule fits** → ask: can the reader tell what to do next from this message alone?
- **Asking back follows the guideline** — "I did not understand this part" / "please give me an
  example" are never counted against you.

## Rule 1 — When you start

**When:** every time you receive work — a ticket assigned, a request in chat or a meeting, a
requirement that changes while you work. Small tasks included.

- Receiver writes `My understanding:` (I will / I won't / By / Questions / Please confirm or
  correct.) on the ticket **before** starting.
- Ticket cannot move to In Progress without this comment (system-enforced).
- Don't copy the request; fill `I won't` (out of scope) and `Questions` (unknowns + assumptions).
- No reply from the requester within **1 working day** → start with what you wrote.
- Requester writes `Why:` and `Done when:`.
- Not met: a spec readable two ways was implemented without checking; QA found it; redone (2026-04).
- Met: receiver restated in own words; a wrong assumption surfaced in 8 minutes (2026-03-04).

## Rule 2 — When you answer

**When:** every time you tell someone something — an answer, an investigation result, "not on our
side", "cannot be done", "cannot reproduce", "the schedule will slip", "please check again".

- Line 1 restates the question **in your own words** (one line). If restating shows you don't know
  what is asked → don't answer, ask back.
- Answer *that* question. Can't → `Answer: I can't answer that yet because …` + what you can say now.
- Closed question (yes/no, A or B, when) → first word of `Answer` is the answer.
- **No exceptions** — all four lines for simple-looking questions too.
- Not only a conclusion — `Next` names the next person and action.
- "Please check again" → `Why` says what changed.
- A reaction emoji is not an answer.
- Not met (different question): asked about B2B data, explained B2C logic (2026-08-10); asked "was
  there a design intent from the start?", answered "I will review it again" (2026-05-04); asked the
  cost of keeping A, answered the cost of building A and B (2026-05).
- Not met (conclusion only): screenshots + "no issue on our side"; requester couldn't tell what to
  do next (2026-09-09).
- Met: question restated as a closed question and confirmed; yes/no settled in 21 minutes
  (2026-07-09). A "not a bug" ruling came with reason and production data (2026-09-21).

## Rule 3 — When you cannot answer yet

**When:** a question/request is addressed to you and you can't answer on the spot — busy, needs
investigation, not yours, about to go on leave.

- `Received. I will reply by <date>.` or `Received. This is not mine — <name> owns it. I have
  passed it on.`
- Post within **4 working hours**.
- Will miss the date → post a new date **before** the old one passes.
- Not met: "I will check and get back to you"; a follow-up question received 2026-05-26 had no
  written answer for 132 days (as of 2026-10-05).
- Met: reason for the wait and the next check time were given first.

## Rule 4 — When you finish

**When:** work finished, cause found, decision made, scope or schedule changed — including anything
settled in a meeting, call or chat.

- `Done:` (What / Where: DEV·STG·PROD / How to check) on the ticket the request came from. A link to
  another ticket is not enough.
- Meeting/chat decisions → on the ticket the **same day**. "I explained it on Teams" is not a record.
- Not met: fix finished and QA-passed, nothing on the request ticket; people argued about the cause
  without knowing the fix existed (2026-08-27).
- Met: request ticket carried dev ticket, owner and due date, stayed open until the production
  result was reported there (2026-08, 18 request tickets).

## Rule 5 — Before you change something

**When:** every time what other people see could be different after your work — load test, DB
restore/reset, deployment, configuration change, cache flush, key rotation, batch-job change,
stopping a PC or server that runs automation.

- `Heads-up:` (What / Where-when / Who is affected / Contact) **before** the work, in the channel the
  affected people read. When finished, say you finished.
- Not met: agreed 27 May to give notice before an STG load test; on 21 Aug the STG DB was reset
  without notice — same kind of work.
- Met: QA time window shared in advance and other tests checked for (2026-05-27).

## Evaluation

| Rule | How it is checked |
|---|---|
| 1 | Record — `I won't` and `Questions` filled + peer review |
| 2 | Peer review (did the asker ask again; reason + next step present) + record (first line carries `My understanding`) |
| 3 | Record — time to acknowledgement, unanswered questions |
| 4 | Record — result comment on the request ticket |
| 5 | Record + peer review |

- Rates, not counts. Unanswered questions measured across linked tickets and other channels.
- Per rule: records (Jira, Teams) and peer review read together. Both above cut-off → **Met**; only
  one → **Partly met**; neither → **Not met**. Cut-offs: peer-review median ≥ 3 ("Usually", 5-level
  scale) and records ≥ 80%.

**Grade ceiling** (one overall grade S/A/B/C/D; communication sets the ceiling, not offset):

| Result on the five rules | Highest grade |
|---|---|
| All Met | S |
| No Not met · 1–2 Partly met | A |
| No Not met · ≥ 3 Partly met | B |
| 1 Not met | B |
| 2 Not met · improved from previous review | C |
| 2 Not met · not improved | D |
| ≥ 3 Not met | D |

- D = salary freeze + PIP.
- For the 2027-02 review, the previous review is the 2026-10 baseline.
- Same rule Not met twice in a row counts as 2 Not met (from the 2027-08 review).

## System enforcement

- Ticket cannot move to In Progress without the Rule 1 comment.
- Missing owners and due dates on in-progress tickets are flagged automatically.
- A fix ticket is linked to its request ticket; the result is sent back to the request ticket.

## Appendix — not evaluated, good practice

- Time: date + time zone, e.g. `2026-06-15 16:21 UTC (23:21 ICT)`.
- Quantities/durations: unit + environment; calendar vs working days.
- Identifiers: booking code, hotel code, ticket key.
- Language: English on tickets/channels another side reads.
- Long exchanges: after three rounds, switch to a call, write the result on the ticket (Rule 4).
- Never write passwords, keys or tokens anywhere (Letter #3 — a directive, not a recommendation).

## Updates

A case that slips past the guideline does not get a new rule: find which rule's "When" was too
narrow and widen it. Updates monthly, recorded in a ticket.
