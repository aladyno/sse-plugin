# Test Case — PROJ-9001 Guest order cancellation within 24h

*(SAMPLE — fictional data, used as a Locked Format example and as input for check_locked_format.py)*

| ID | Flow / Function | Type | Technique | Precondition | Steps | Test Data | Expected Result | Priority |
|---|---|---|---|---|---|---|---|---|
| TC-01 | Cancel inside the 24h window | Positive | EP | Guest order created 2h ago (UTC), not shipped, refundable items | 1. Open the confirmation email<br>2. Click the cancel link<br>3. Read the refund amount shown<br>4. Confirm | ORD-G-001, fee 5% | Order status CANCELLED; refund of 95% of the amount paid to the original card; cancellation email sent | P0 |
| TC-02 | Cancel at the inner boundary | Boundary | BVA | Order created exactly 23h59m ago (UTC) | 1. Click the cancel link<br>2. Confirm | ORD-G-002 | Cancellation succeeds (still inside the window) | P0 |
| TC-03 | Cancel at the outer boundary | Boundary | BVA | Order created 24h01m ago (UTC) | 1. Click the cancel link | ORD-G-003 | "Cancellation window closed" page with support contact; no refund created | P0 |
| TC-04 | Cancel after shipment | Negative | Decision table | Order has shipped | 1. Click the cancel link | ORD-G-004 | "Order already shipped" message; no refund created | P0 |
| TC-05 | Replay a used cancel link | Security | State transition | Order already cancelled in TC-01 | 1. Click the same link again | ORD-G-001 | Page states the order is already cancelled; no second refund | P0 |
| TC-06 | Refund provider fails mid-flow | Edge | Error guessing | Mock provider returns a timeout after the order is cancelled | 1. Click the cancel link<br>2. Confirm | ORD-G-005 | Status REFUND_PENDING; operations alert raised; customer told the refund is in progress | P1 |
| TC-07 | Final-sale items excluded | Negative | Decision table | Order contains only final-sale items, inside the window | 1. Click the cancel link | ORD-G-006 | Refund preview shows 0.00 per policy before confirmation | P1 |
| TC-08 | Foreign-currency order | Edge | EP | Order paid in EUR, inside the window | 1. Click the cancel link<br>2. Confirm | ORD-G-007 | Refund issued in EUR; fee rounded to 2 decimal places | P1 |
| TC-09 | Link used for another order | Security | Error guessing | Two guest orders exist | 1. Swap the order number in the link | ORD-G-001, ORD-G-002 | Request rejected; neither order changes state | P0 |
| TC-10 | Keyboard-only cancellation | Accessibility | Exploratory | Any cancellable order | 1. Complete the flow using only the keyboard and a screen reader | ORD-G-002 | All controls reachable and labelled; refund amount announced (WCAG 2.2 AA) | P2 |
| TC-11 | Registered-customer flow unchanged | Regression | EP | Any registered-customer order | 1. Cancel from "My orders" as before | ORD-R-001 | Existing flow and fee unchanged; no email link used | P1 |

Type ∈ {Positive, Negative, Boundary, Edge, Security, Accessibility, Regression}. Technique ∈ {EP, BVA, Decision table, State transition, Pairwise, Error guessing, Exploratory}. Priority ∈ {P0, P1, P2} from risk level (P0 = blocks release if it fails).

## Not covered
- Window evaluated on a DST-change date in the store's timezone — the ticket does not name the store timezone; proposed handling: assume the store default timezone from configuration, label it as an assumption, confirm with the PO before finalising.
- Partial shipment (one item shipped, others not) — the source has no rule; proposed handling: treat as "shipped" and refuse, pending a BA decision.
