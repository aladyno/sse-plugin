# sse-qc — Worked examples

Filled examples for every mode, following the locked-format templates in [`../assets/`](../assets/)
(`template-*.md`) and the rules in [`../SKILL.md`](../SKILL.md#modes).
All tickets are **fictional** (an e-commerce store) — copy the structure and the depth of
reasoning, not the content. A full-size sample of the refund feature (PROJ-9001) lives in
[`../assets/`](../assets/).

## Contents

1. `diag` — stuck discussion about regression scope
2. `review` — easy case (clear ticket, one gap)
3. `review` — hard case (vague ticket, comment contradicts description)
4. `test-plan` — short example with a risk register
5. `test-case` — example with techniques and a "Not covered" section
6. `checklist` — example with an item needing confirmation

---

## 1. `diag`

**Context:** the team is deciding how much regression to run for a change to the discount engine
(percentage discounts now apply before shipping fees instead of after).

```
QC Diag — regression scope for discount-before-shipping change

1. Totals in existing carts — carts saved before release may be recalculated on checkout and show a different price than the customer saw. → Add a regression case for a cart created before the release and paid after.
2. Rounding at minor units — applying a percentage to a smaller base changes where rounding happens; totals can drift by 0.01 against finance reports. → Boundary cases with amounts that round at .005 in every supported currency.
3. Refunds of old orders — refund logic may recompute the discount with the new order of operations. → Refund an order placed before the release; expect the originally charged amount.

Decisive question: Do refunds recompute totals from rules, or reuse the amounts stored at purchase?

QC Output: Regression must cover saved carts, rounding at .005, and refunds of pre-release orders; blocked on refund recomputation answer.
```

---

## 2. `review` — easy case

**Input:** ticket `PROJ-8801` — "Add a star-rating filter (3–5 stars) to the product search page."
AC: "Selecting one or more ratings shows only products with those ratings; clearing all shows
every product again." No comments.

```
## Review & Gap Analysis — PROJ-8801

### Requirement summary
Add a 3–5 star rating filter to product search; selected ratings restrict the results, clearing all restores them.

### Issues found

#### #1 — Missing negative/edge — No behaviour defined when no product matches
- **Quote / location:** AC: "shows only products with those ratings" — nothing on an empty result.
- **Reasoning (why it matters, risk if ignored):** common in small categories; without an AC the page may render blank or error, and testing has no expected result.
- **Proposed resolution:** reuse the existing search empty state (already used by the price filter) with "Try removing a filter".
- **Needs confirmation:** Yes — BA: "Does the rating filter reuse the shared empty-state component, or need its own message?"

### Summary & recommendation
- #1 is non-blocking — build with the proposal, confirm before release.
- Clear enough to start development.
```

---

## 3. `review` — hard case

**Input:** ticket `PROJ-4021` — "Let guest customers cancel orders online instead of calling
support." Description: "Guests can cancel within 24h of ordering, free of charge." Latest PO
comment (2 days ago): "Update: free 24h cancellation only for orders WITHOUT a promo code; orders
with a promo code still go through support." No separate AC.

```
## Review & Gap Analysis — PROJ-4021

### Requirement summary
Guests cancel online within 24h free of charge — per the latest comment, only for orders without a promo code; promo-code orders still go through support.

### Issues found

#### #1 — Contradiction — Description has no promo-code restriction, the latest comment adds one
- **Quote / location:** Description "Guests can cancel within 24h… free of charge" vs PO comment "only for orders WITHOUT a promo code".
- **Reasoning (why it matters, risk if ignored):** a developer reading only the description lets promo orders self-cancel, contrary to the latest decision; promo budgets are then refunded without review.
- **Proposed resolution:** the latest comment wins — promo-code orders show "contact support"; only non-promo orders self-cancel.
- **Needs confirmation:** Yes — BA: "Is the comment the final decision, so the AC can be rewritten in the ticket?"

#### #2 — Missing AC — "within 24h" has no reference point
- **Quote / location:** "within 24h of ordering" — server time, customer local time or store time?
- **Reasoning (why it matters, risk if ignored):** customers in several timezones; development and testing may use different clocks, producing wrong refusals near the boundary.
- **Proposed resolution:** measure from the order-created timestamp in UTC, consistent with other deadlines in the system.
- **Needs confirmation:** Yes — BA: "Is 24h from the order-created timestamp in UTC the intended rule?"

#### #3 — Untestable — "free of charge" with partial promo usage undefined
- **Quote / location:** "free of charge" — silent on orders where a promo code covered part of the price.
- **Reasoning (why it matters, risk if ignored):** refund amount cannot be asserted for mixed-payment orders.
- **Proposed resolution:** treat any promo code on the order as "promo order" (per #1), so the question disappears.
- **Needs confirmation:** Yes — BA, same decision as #1.

### Summary & recommendation
- #1 and #2 are blocking: they decide who may cancel and when. #3 resolves with #1.
- Significant gaps — do not start development until #1 and #2 are confirmed.
```

---

## 4. `test-plan` — short example

```markdown
# Test Plan — PROJ-8801 Star-rating filter

## 1. Scope
- In scope: 3–5 star filter on product search, combined with the existing price and brand filters.
- Out of scope: rating display on product detail pages (not in the ticket).

## 2. Test objectives
The rating filter returns exactly the selected ratings, combines correctly with other filters, and handles empty results.

## 3. Test strategy
- Functional: equivalence partitions per rating; single and multiple selection; clear all.
- Regression (if existing flows are touched): price and brand filters combined with the new filter.
- Integration (third parties / other services, if any): needs confirmation from dev — search service call or client-side filtering.
- Non-functional (only if signalled — ISO/IEC 25010 characteristics): usability/accessibility — filter checkboxes operable by keyboard with labels (WCAG 2.2 AA).
- Exploratory (charters, if risk is uncertain): not needed — low risk.

## 4. Environment & test data
Existing staging; catalogue with products at each rating, plus a category with no 5-star products for the empty state.

## 5. Entry / Exit criteria
- Entry: build on staging; review issue #1 of PROJ-8801 confirmed.
- Exit: all P0/P1 cases pass; no open Critical/Major defects.

## 6. Risks & mitigation
| Risk | Likelihood | Impact | Level | Mitigation |
|---|---|---|---|---|
| Empty state not agreed | Medium | Low | Low | Confirm with BA before testing (review #1) |
| Filter combination drops the price filter | Medium | Medium | Medium | Regression case TC-04 |

## 7. Roles & schedule
Needs confirmation from the lead — no estimate in the ticket.

## 8. Deliverables
Test case list (PROJ-8801-test-case.md), results, defect reports.
```

---

## 5. `test-case` — with techniques and "Not covered"

```markdown
# Test Case — PROJ-8801 Star-rating filter

| ID | Flow / Function | Type | Technique | Precondition | Steps | Test Data | Expected Result | Priority |
|---|---|---|---|---|---|---|---|---|
| TC-01 | Single rating | Positive | EP | On search results | 1. Select 4 stars<br>2. View the list | Category with 4-star products | Only 4-star products shown | P0 |
| TC-02 | Multiple ratings | Positive | EP | On search results | 1. Select 3 and 5 stars | Category with both ratings | 3- and 5-star products shown, no 4-star | P0 |
| TC-03 | No match | Edge | Error guessing | On search results | 1. Select 5 stars in a category without 5-star products | Category with 3–4 star products only | Empty state as agreed in review #1 | P1 |
| TC-04 | Combined with price filter | Regression | Pairwise | Price filter applied | 1. Add the rating filter | Price range preset | Results satisfy both filters; price filter kept | P1 |
| TC-05 | Keyboard operation | Accessibility | Exploratory | On search results | 1. Toggle each rating with the keyboard only | Any category | Each checkbox focusable and announced with its label | P2 |

Type ∈ {Positive, Negative, Boundary, Edge, Security, Accessibility, Regression}. Technique ∈ {EP, BVA, Decision table, State transition, Pairwise, Error guessing, Exploratory}. Priority ∈ {P0, P1, P2} from risk level (P0 = blocks release if it fails).

## Not covered
- Rating combined with the brand filter — the ticket does not describe brand filter logic; proposed handling: assume AND logic as in TC-04, confirm with dev before finalising.
- Products with fractional ratings (e.g. 4.5) — the source does not say how they bucket; proposed handling: round down, label as an assumption, confirm with PO.
```

---

## 6. `checklist` — with an item needing confirmation

```markdown
## QC Checklist — PROJ-8801

### Pre-deploy
- [ ] Staging build is the release candidate version.
- [ ] Review #1 (empty state) confirmed by BA.

### Functional smoke
- [ ] Single, multiple and cleared rating selections behave per TC-01 and TC-02.
- [ ] Empty state shown as agreed — TC-03.

### Regression (affected areas)
- [ ] Price and brand filters still work combined with the rating filter — TC-04.
- [ ] [NEEDS CONFIRMATION] Product detail page — the ticket does not say whether it is affected; not marked safe until confirmed.

### Data/Config
- [ ] Staging catalogue has products at every rating, including a category without 5-star products.

### Rollback
- [ ] Rollback plan exists / revert method confirmed (feature flag, if any).

### Sign-off
- [ ] QA sign-off
- [ ] PO sign-off (if required)
```
