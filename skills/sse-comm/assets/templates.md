# sse-comm — filled examples

All names, codes and dates below are illustrative. Fill real facts only; leave unknowns as
`[placeholders]` and list them as missing. Opening words and field labels stay in English.

## Rule 1 — start (receiver)

Input (VI): "Được giao ELS-1234: thêm filter theo country cho API search booking."

```
My understanding:
- I will: add an optional countryCode filter to the booking search API, applied to B2B bookings, returning only bookings whose hotel is in that country.
- I won't: change the B2C search, the UI, or the export file.
- By: 2026-10-24 18:00 ICT (20:00 KST)
- Questions:
  1. Is the filter on the hotel's country or the guest's nationality? I assumed the hotel's country.
  2. Should an unknown country code return an empty list or a 400 error? I assumed 400.
Please confirm or correct.
```

Requirement changed mid-work → post a new `My understanding:` with only the changed lines plus
`Changed because: <what changed, who asked, when>`.

## Rule 1R — requester

```
Why: Agents cannot find Vietnam bookings quickly; support spends ~30 min/day on manual lookup.
Done when: GET /bookings?countryCode=VN returns only VN hotels' bookings on STG, and QA case ELS-1240 passes.
```

## Rule 2 — answer

Closed question — "Is the price mismatch on booking OMH24100123 a bug on our side?"

```
My understanding: you are asking whether the price shown to the agent for booking OMH24100123 differs from the vendor price because of our system.
Answer: No — the difference comes from the vendor's rate change at 2026-10-20 03:10 UTC (10:10 ICT), after the search but before the booking.
Why: I compared the search log and the booking request log on PROD for that booking code; the vendor returned 120.00 USD at search and 128.00 USD at booking.
Next: [CS owner] informs the agent by 2026-10-21 17:00 ICT; I add the price-change note to the booking by 2026-10-21 15:00 ICT.
```

Partial answer:

```
My understanding: you are asking when the STG fix for hotel code H12345 will reach PROD.
Answer: I can't answer that yet because the release window for this week is not fixed. What I can say now: the fix passed QA on STG on 2026-10-20.
Why: QA result on ELS-1250; release calendar has no slot yet.
Next: I confirm the PROD date with [release owner] and reply here by 2026-10-22 12:00 ICT.
```

"Please check again":

```
My understanding: you are asking me to re-check whether cancellation of OMH24100200 still fails on STG.
Answer: No — it no longer fails.
Why: What changed: the vendor timeout was raised from 10 s to 30 s on STG at 2026-10-21 09:00 ICT. I retried the cancellation at 09:30 ICT and it succeeded.
Next: QA ([name]) re-runs case ELS-1301 on STG by 2026-10-21 17:00 ICT.
```

Ask-back (restating exposed an unclear question) — do not answer:

```
My understanding: I am not sure what you are asking. Do you mean (A) whether the markup is applied before the promotion, or (B) whether the promotion is shown to B2B agents?
Please confirm A or B, and I will answer within 2 working hours of your reply.
```

## Rule 3 — cannot answer yet

```
Received. I will reply by 2026-10-22 15:00 ICT (17:00 KST).
```

With reason first:

```
Received. I need the vendor's log to answer; I have asked them and will check again at 2026-10-22 10:00 ICT. I will reply by 2026-10-22 15:00 ICT.
```

Not mine:

```
Received. This is not mine — [name] owns the settlement batch. I have passed it on.
```

Date will slip (post before the old date passes):

```
Received — update: I will not make 2026-10-22 15:00 ICT because the vendor log has not arrived. New date: 2026-10-23 15:00 ICT.
```

Before leave:

```
Received. I am on leave 2026-10-23 to 2026-10-27 (working days). [name] covers this and will reply by 2026-10-23 17:00 ICT.
```

## Rule 4 — finish

```
Done:
- What: countryCode filter added to the B2B booking search API (ELS-1234). Unknown codes return 400.
- Where: STG
- How to check: GET /bookings?countryCode=VN on STG returns only bookings of VN hotels; QA case ELS-1240.
```

Decision made in a meeting (same day, on the request ticket):

```
Done:
- What: Decision in the 2026-10-21 14:00 ICT meeting (attendees: [names]) — keep option A; option B is out of scope for this release.
- Where: n/a (decision) — affects PROD release 2026-10-28
- How to check: meeting notes [link]; scope updated in this ticket's description.
```

## Rule 5 — before changing something shared

```
Heads-up:
- What: reset the STG database to the 2026-10-20 snapshot.
- Where / when: STG, 2026-10-22 13:00–14:00 ICT (15:00–16:00 KST).
- Who is affected: QA regression runs on STG, partner test accounts, the STG booking batch.
- Contact: [name] on [channel].
```

After the work:

```
Finished: STG database reset to the 2026-10-20 snapshot at 2026-10-22 13:40 ICT. Bookings created after 2026-10-20 on STG are gone.
```

## Compound sequence — hotfix deployed to PROD

1. Rule 5, in the channel the affected people read, before the deploy → `Heads-up:`.
2. Rule 5, same channel, after → `Finished: …`.
3. Rule 4, on the **request** ticket (not only the dev ticket) → `Done:` with `Where: PROD`.
