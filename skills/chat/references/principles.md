# chat — principles, anti-patterns, before/after

Read on demand when a rewrite needs justification or the user asks "why".

Canonical rules live in [shared/communication-standard.md](../../../shared/communication-standard.md);
this file only adds mechanisms, anti-patterns and before/after examples.

## Send — receiver-centric

### 1. Why before How
- **Mechanism:** the receiver has to re-walk your reasoning from the start line. Shared *why* gives
  them the basis to judge alternatives themselves and removes repeated questions.
- **Anti-pattern:** one-line chat message about a topic you've thought about for days.
- Before: `Please change the cache TTL to 2 minutes.`
- After: `Open-API partners are seeing prices that are up to 10 min stale, which caused 3 rate
  mismatch complaints this week. Can we lower the Open-API cache TTL from 10 to 2 min? It roughly
  [x]× the vendor calls — please check whether that is within our rate limit by 2026-10-06.`

### 2. Fit the channel
- Text for simple, low-urgency, factual items; a short call for complex or contested ideas (send
  the text as the agenda and the call outcome as written follow-up); a document for decisions others
  must reference later.
- **Anti-pattern:** a 15-message chat thread negotiating a design.

### 3. Carry the receiver's context
- Translating a Korean document into English is not done if the context stayed in Korea.
- **Dev → planner:** "This can't be done" is not information.
  - Before: `This is not possible with the current vendor API.`
  - After: `The vendor API returns cancellation policy only at booking time, not at search time
    (why). Options: (A) show policy on the booking page only — no extra work; (B) call the
    pre-check API per result — +[x] ms per search and vendor rate-limit risk; (C) cache policies
    nightly — [n] days of work, policy may be up to 24 h stale (alternatives). A keeps the release
    on 2026-10-15; B or C moves it by about [n] days (impact). Which do you prefer?`
- **QA → dev:** symptom-only reports get slow responses.
  - Before: `Booking page is broken.`
  - After: steps to reproduce, expected vs actual, environment/build, scope (which
    users/vendors/% of traffic), priority and its basis (blocks release? money at risk?).
- **Planner → dev:** business impact of the feature, preconditions, and acceptance criteria.

## Receive — active

### 4. Paraphrase
- "As I understand it, you want A done via B — correct?" — the cheapest quality control there is.
- In async channels, write it down: it is evidence and insurance.

### 5. Say what you don't understand
- Nodding at 70% lets the other 30% derail the project. This happens in a native-language meeting
  too (domain terms, jargon); in a foreign-language meeting it is near certain.
- Continuing without understanding is the irresponsible choice, not asking.

### 6. Structure and confirm
- Turn scattered input into "Here is what I understood: 1… 2… 3…". Two effects: your understanding
  gets verified, and the sender sees how their message landed. Good receivers create good senders.

### 7. Silence is not agreement
- Read-without-reply leaves the sender guessing: read? agreed? in progress?
- One line removes the uncertainty and the follow-up pings: `Received — I'll reply by 2026-10-05.`

## Root: respect
- Your colleague's time is as valuable as yours.
- Humility: don't assume they know what you know.
- Seriousness: try to understand everything they said.
- Principles apply to leaders first; feedback on the leader's own communication is welcome.
