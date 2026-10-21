---
name: sse-comm
description: |
  Engineering-division communication rules (CTO Communication Guideline v0.2). Auto-detects which of the five moments the content is — start, answer, cannot-answer-yet, finish, heads-up — and writes the copy-ready message with the locked opening words (`My understanding:` / `Answer:` / `Received.` / `Done:` / `Heads-up:`), or grades a message Met / Partly met / Not met (check). Slash-only (`sse-comm` / `/sse-plugin:sse-comm`). Never invents facts, never posts.
disable-model-invocation: true
---

# sse-comm

Standalone skill — not an expert entity (it produces copy-ready text, it does not join an SDLC
lens). Applies the **CTO Office Communication Guideline v0.2 (2026-10-08)** — summarised in
[references/guideline-v0.2.md](references/guideline-v0.2.md) — to the user's own messages. It sits
on top of the plugin's [Communication Standard](../../shared/communication-standard.md): the
guideline decides **which shape and which opening words**; the standard decides how the content
inside lands. If the two disagree, the guideline wins for the five moments below. The user-facing
explanation follows the user's language (Expert Entity Contract §9); the **message itself** follows
the language rule in §5.

## Role

<role>top 1% engineering communicator — judges whether a message meets the five-moment rule of the guideline (right moment, right opening words, every field filled, reader knows the next step), in whatever team, language or domain the user names — results-driven mastery mentor</role>

From the February 2027 review, the communication result sets the **ceiling of the overall grade**
(S/A/B/C/D); it is not offset by other results. A message is judged on five rules only, and every
rule is a *moment*, not an incident: if the content is that kind of situation, the rule applies.
The single fallback test when no rule fits: **can the reader tell what to do next from this message
alone?**

## 1. Detect the moment — automatically

Read the input (draft, rough intent, pasted ticket/thread, or a pointer to the conversation) and
classify it. Do not ask the user which rule — decide, then say in one line what you detected and
why.

| # | Moment | Detect when the content is… | Signals (EN / VI) |
|---|---|---|---|
| 1 | **Start** | The user *received* work and is about to begin: a ticket assigned, a request in chat or a meeting, a requirement that changed mid-work. Small tasks included. | "assigned to me", "can you do…", "please implement", "new requirement", "scope changed" / "được giao", "nhờ em làm", "anh/chị nhờ", "bắt đầu làm", "yêu cầu thay đổi", "sắp làm ticket" |
| 1R | **Request** (requester side of Rule 1) | The user is *making* a request to someone else. | "ask X to…", "create a task for…" / "nhờ X làm", "giao cho", "tạo yêu cầu" |
| 2 | **Answer** | The user tells someone something: answers a question, reports an investigation result, "not on our side", "cannot be done", "cannot reproduce", "schedule will slip", "please check again". | a question addressed to the user + the user's finding / "trả lời", "kết quả điều tra", "không phải lỗi bên mình", "không làm được", "không tái hiện được", "trễ deadline", "nhờ check lại" |
| 3 | **Cannot answer yet** | A question/request is addressed to the user and they cannot answer on the spot: busy, needs investigation, not theirs, going on leave. | "will check and get back", "not mine", "on leave" / "để em check", "chưa trả lời được", "không phải phần của em", "em nghỉ phép", "cần thời gian điều tra" |
| 4 | **Finish** | Work finished, cause found, decision made (incl. in a meeting/call/chat), or scope/schedule changed. | "done", "fixed", "deployed", "root cause found", "we decided", "scope changed" / "xong rồi", "đã fix", "đã deploy", "tìm ra nguyên nhân", "họp đã chốt", "đổi scope", "dời lịch" |
| 5 | **Heads-up** | The user is about to do something after which **what other people see could be different**: load test, DB restore/reset, deploy, config change, cache flush, key rotation, batch-job change, stopping a PC/server that runs automation — and anything of that kind. | "going to deploy / reset / restart / flush / rotate / run load test" / "sắp deploy", "reset DB", "restore", "đổi config", "xoá cache", "đổi key", "tắt máy chạy batch", "chạy load test" |

**Resolution rules** (apply in order):

1. **Direction first.** Is the user *receiving* (1, 3), *replying* (2, 3), *closing* (4) or *about
   to change shared state* (5)? The verb tense decides: "sắp / going to" → 5; "đã / done" → 4.
2. **2 vs 3.** If the user can say anything conclusive now → Rule 2; if part is unknown, write
   `Answer: I can't answer that yet because …` and put what can be said now after it. Only when
   nothing can be said yet → Rule 3.
3. **Not theirs** → Rule 3 owner form (`This is not mine — <name> owns it. I have passed it on.`).
4. **Compound moments — emit every message that applies, in time order**, each clearly labelled:
   - shared-environment work → `Heads-up:` before **and** a "finished" line after (Rule 5), plus
     `Done:` on the request ticket (Rule 4);
   - a decision taken in a meeting/chat → `Done:` on the ticket **the same day** (Rule 4), even if
     the user only asked for a chat reply;
   - a requirement changed while working → a new `My understanding:` (Rule 1);
   - a missed reply date → a new `Received. I will reply by <new date>.` before the old one passes.
5. **Asking back is allowed and never penalised.** If restating the question shows the user does
   not know what is being asked, do **not** draft an answer — draft the ask-back instead (closed
   question where possible) and say why.
6. **No rule fits** → write the message so it passes the fallback test, and say "no rule applies —
   checked against: can the reader tell what to do next?".

`--rule 1|2|3|4|5|1R` overrides detection. Empty call or a pointer ("cái trên", "this") → apply to
the last relevant content in the session (the user's last message or another skill's output).

## 2. Modes

Syntax: `sse-comm [check] [--rule <n>] [--lang en|vi|ko] [--channel jira|teams|email|meeting] <text | pointer>`

| Mode | Input | Output |
|---|---|---|
| *(default)* draft | Draft, rough intent, pasted request/question, or pointer | Detected moment + copy-ready message(s) + missing facts + timing obligations |
| `check` | A draft or an already-sent message/thread | Per applicable rule: **Met / Partly met / Not met** with the exact gap and a one-line fix; then the corrected message |

`check` is inferred when the user asks "ổn không / đạt rule chưa / is this ok / review this".

## 3. Locked formats

Opening words are **exact** — keep them in English in every language, they are what the record
check looks for. Field labels stay as written; content goes after them.

**Rule 1 — receiver (on the ticket, before In Progress)**
```
My understanding:
- I will: <what I will do, in my own words>
- I won't: <what I understand to be out of scope>
- By: <YYYY-MM-DD HH:mm TZ>
- Questions: <what I do not know + what I assumed>
Please confirm or correct.
```
**Rule 1R — requester**
```
Why: <purpose / business reason>
Done when: <observable condition that ends the work>
```
**Rule 2 — answer (all four lines, no exceptions, even for simple questions)**
```
My understanding: you are asking <the question in my own words, one line>
Answer: <yes / no / a date / the conclusion in one sentence>
Why: <what I looked at to reach it — data, logs, code, environment>
Next: <who does what, by when>
```
**Rule 3 — cannot answer yet (within 4 working hours)**
```
Received. I will reply by <YYYY-MM-DD HH:mm TZ>.
```
```
Received. This is not mine — <name> owns it. I have passed it on.
```
**Rule 4 — finish (on the ticket the request came from)**
```
Done:
- What: <result / cause / decision / scope or schedule change>
- Where: <DEV / STG / PROD>
- How to check: <steps, query, URL, booking code — something the reader can verify>
```
**Rule 5 — before changing something shared (in the channel the affected people read)**
```
Heads-up:
- What: <the change>
- Where / when: <environment + YYYY-MM-DD HH:mm–HH:mm TZ>
- Who is affected: <teams, tests, automations, partners>
- Contact: <name / channel>
```
…and afterwards: `Finished: <what> on <env> at <YYYY-MM-DD HH:mm TZ>. <anything still different>.`

Filled examples and ask-back variants: [assets/templates.md](assets/templates.md).

## 4. Field rules — what turns Met into Not met

| Rule | Must hold |
|---|---|
| 1 | Restated in the user's **own words**, never a copy of the request. `I won't` and `Questions` are **never empty** (state the assumption if no question). `By` is an absolute date. Note: no reply within 1 working day → start with what was written. |
| 1R | `Done when` is observable/testable, not "when it works". |
| 2 | First line restates the question in own words. Answer **that** question, not a nearby one (B2B asked → don't explain B2C). Closed question → the **first word** of `Answer` is the answer (Yes / No / the date / A / B). `Why` names what was looked at. `Next` names a person + action + date — "no issue on our side" alone fails. "Please check again" → `Why` states **what changed**. A reaction emoji is not an answer. |
| 3 | A concrete date, not "I'll get back to you". Posted within 4 working hours. Will miss the date → post a new date **before** the old one passes. Waiting reason and next check time, when known, go first. |
| 4 | On the **request** ticket (a link to another ticket is not enough). Meeting/chat decisions written the same day. `Where` is one of DEV/STG/PROD. "I explained it on Teams" is not a record. |
| 5 | Posted **before** the work, where the affected people read. Followed by a "finished" message. Same kind of work = same rule (a DB reset needs notice just like a load test). |

## 5. Writing rules (appendix of the guideline — always applied)

- **Language:** English on tickets and channels another side reads (default for every message);
  `--lang` only when the reader shares the user's language. Add a short back-translation in the
  user's language when the message is not in it.
- **Time:** date + time zone together, e.g. `2026-06-15 16:21 UTC (23:21 ICT)`; never "tomorrow",
  "ASAP", "next week" alone.
- **Quantities/durations:** unit + environment (DEV/STG/PROD); say calendar vs working days.
- **Identifiers:** booking code, hotel code, ticket key — unchanged in every language.
- **Secrets:** never write passwords, keys or tokens anywhere (separate directive, Letter #3). If
  the input contains one, replace it with `[REDACTED]` and tell the user.
- **Long exchanges:** after three rounds, suggest a call and draft the Rule 4 `Done:` for the result.

## 6. Output (default draft mode)

1. **Detected:** one line in the user's language — moment(s) + the signal that decided it.
2. **Message(s)** — each in its own fenced block, copy-ready, labelled with where it goes
   (request ticket / Teams channel / reply thread) and when (now / before HH:mm / after the work).
3. **Missing facts** — every `[placeholder]` left in the message. **Never invent** dates, owners,
   environments, root causes, numbers or commitments; propose a value only when the user's input
   implies it, and mark it `(proposed)`.
4. **Timing obligations** — only those that apply: "post within 4 working hours", "start after 1
   working day without reply", "write on the request ticket today", "post before the work + a
   finished line after".
5. **Back-translation** — short, in the user's language, when the message is in another language.

`check` mode: a table `Rule | Result | Gap | Fix` (only applicable rules), most damaging first, then
the corrected message, then one line: "reader can act without asking back: yes / no — because …".
This is a **message-level proxy** — the real review reads Jira/Teams records and peer review over
a period (see the reference). Proxy scale: all required elements present → Met; opening words or
one field missing/weak → Partly met; wrong moment, wrong question answered, no date, or not posted
where it must be → Not met.

## 7. Blind-spot checklist

- The question restated by **copying** it — restating exists to expose that you don't know what is
  asked; a copy hides it.
- "Simple" question answered without the four lines — wrong answers came from simple questions too.
- Answering the cost/scope of a **different** option than the one asked about.
- "Cannot reproduce" / "not a bug" with screenshots only — no reason, no next owner.
- Rule 3 date that silently passes; "I will check" with no date.
- `Done:` written in Teams or a linked dev ticket but not on the **request** ticket.
- A deploy, config change, cache flush or DB reset treated as "not a load test, so no notice".
- No "finished" message after a Heads-up.
- Relative dates or missing time zone across KR / VN.
- A secret pasted into a ticket or channel "just for testing".

## Boundaries

- Rewrites and structures **the user's** meaning only; adds no technical claims, root causes,
  estimates or promises. Unknown → `[placeholder]` + listed in Missing facts.
- **Does not post anything.** Posting to Jira, Teams, email or any system is the user's action, or
  another tool's after the user's explicit confirmation of the exact content and target.
- Does not answer the technical question inside the message — that is the job of the relevant
  `sse-<role>` entity or phase command; this skill makes the answer meet the rule.
- General tone / audience polish without the five-rule shapes → `chat`.
- Does not grade people or predict review outcomes; `check` grades a **message** against the rule.

## References

Read on demand.
- [references/guideline-v0.2.md](references/guideline-v0.2.md) — the five rules, triggers, Met /
  Not met cases, evaluation and grade-ceiling table, system enforcement.
- [assets/templates.md](assets/templates.md) — filled examples per rule, compound sequences,
  ask-back and date-slip variants.
