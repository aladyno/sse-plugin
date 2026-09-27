## Review & Gap Analysis — PROJ-9001 (SAMPLE, fictional data)

### Requirement summary (1–2 sentences, as the source states it)
Add a cancel link to the guest order confirmation email: cancellation allowed within 24h of ordering and before shipment, automatic refund per the cancellation policy, refund amount shown before the customer confirms.

### Issues found

#### #1 — Contradiction — 24h measured in store local time or UTC
- **Quote / location:** AC 1 says "24h from order creation (store local time)" but the latest Product Owner comment says "measured from order creation in UTC, not store local time".
- **Reasoning (why it matters, risk if ignored):** the two readings differ by the store's UTC offset and shift again at DST changes; development and testing may use different windows, and customers near the edge are refused a cancellation they were promised — a direct money complaint.
- **Proposed resolution:** the latest comment wins: measure in UTC from the order-created timestamp; update AC 1 in the ticket before development starts.
- **Needs confirmation:** Yes — **BA/PO** to rewrite AC 1 as UTC; **QC** to agree that the boundary cases at 23h59m and 24h01m are both evaluated in UTC.

#### #2 — Missing negative/edge — Refund fails after the order is cancelled
- **Quote / location:** the description only says "cancels the order and refunds the card"; nothing covers a refund failure.
- **Reasoning (why it matters, risk if ignored):** cancellation and refund are two systems; if the payment provider rejects or times out after the order is cancelled, the order is half-done — nothing ships, the customer has no money back, and nobody is alerted.
- **Proposed resolution:** add an intermediate "refund pending" state with an operations alert; the customer is told the refund is in progress. Add it as AC 4.
- **Needs confirmation:** Yes — **BA** to decide the business behaviour on refund failure; **QC** to add the matching case.

#### #3 — Missing NFR — Security of the cancel link
- **Quote / location:** "add a Cancel order link to the order confirmation email" — no statement on how the link is protected.
- **Reasoning (why it matters, risk if ignored):** a guessable or reusable link lets anyone cancel someone else's order or trigger a second refund (OWASP WSTG business-logic and authorization categories).
- **Proposed resolution:** single-use, unguessable token bound to the order, expiring with the 24h window; replay shows "already cancelled".
- **Needs confirmation:** Yes — **QC** with the tech lead: "Is the token single-use and bound to one order?"

### Summary & recommendation
- #1 is **blocking** (the cancellation window is the core of the feature). #2 and #3 are **non-blocking** for development but must be settled before release because they involve money and order integrity.
- Readiness for development: significant gaps — settle #1 first.
