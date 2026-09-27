# Test Plan — PROJ-9001 Guest order cancellation within 24h

*(SAMPLE — fictional data, used as a Locked Format example and as input for check_locked_format.py)*

## 1. Scope
- In scope: cancellation via the email link for guest orders; cancellation fee per policy; automatic refund to the original card; refund-failure handling.
- Out of scope: registered-customer cancellation (already exists), cancellation by support staff, changes to the cancellation policy itself.

## 2. Test objectives
Confirm that a guest can cancel within the 24h window (UTC, per the Product Owner comment), that the refund amount shown before confirmation is correct, that shipped or expired orders are refused with a clear message, and that a failed refund never leaves an order without a visible pending state.

## 3. Test strategy
- Functional: AC 1–3 with equivalence partitions (inside/outside window, shipped/not shipped, refundable/final-sale) and boundary values around 24h; state transition coverage for PLACED to CANCELLED and CANCELLED to REFUND_PENDING.
- Regression (if existing flows are touched): registered-customer cancellation and support-staff cancellation must not change behaviour.
- Integration (third parties / other services, if any): payment provider refund in sandbox; warehouse notification that the order must not ship.
- Non-functional (only if signalled — ISO/IEC 25010 characteristics): security — single-use unguessable token, replay and cross-order access (OWASP WSTG authorization and business-logic categories); accessibility of the cancel and refund-preview pages at WCAG 2.2 AA.
- Exploratory (charters, if risk is uncertain): one 60-minute session — explore the cancel link with delayed clicks, multiple tabs and DST dates to discover window and double-refund defects.

## 4. Environment & test data
Staging with the payment provider sandbox and a mockable refund endpoint. Data: guest orders created at T-2h, T-23h59m and T-24h01m (UTC), one shipped order, one final-sale order, one order paid in EUR. Details in sample-test-data.csv.

## 5. Entry / Exit criteria
- Entry: build containing PROJ-9001 deployed to staging; confirmation email renders the cancel link; review issue #1 settled.
- Exit: 100% of P0 cases pass; no open Critical/Major defects (severity per IEEE 1044 classification); remaining failures have tracked tickets.

## 6. Risks & mitigation
| Risk | Likelihood | Impact | Level | Mitigation |
|---|---|---|---|---|
| Window computed in store local time instead of UTC | Medium | High | High | Settle AC 1 before testing; test both boundaries in UTC and on a DST-change date |
| Refund fails after cancellation, leaving no pending state | Medium | High | High | Mocked provider failure case (TC-06); verify the operations alert |
| Cancel link replayed or used on another order | Low | High | Medium | Security cases TC-05 and TC-09 |
| Sandbox cannot simulate a mid-flow refund failure | High | Medium | Medium | Use the mock; mark the case for re-verification in a production-like environment |

## 7. Roles & schedule (only if sourced, otherwise "needs confirmation")
Needs confirmation — the ticket has no estimate and no QA assignee.

## 8. Deliverables
- Test case list (sample-test-case.md), results per test cycle, defect reports for failed cases, pre-release QC checklist.
