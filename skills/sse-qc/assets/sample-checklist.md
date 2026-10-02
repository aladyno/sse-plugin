## QC Checklist — PROJ-9001 release

*(SAMPLE — fictional data, used as a Locked Format example and as input for check_locked_format.py)*

### Pre-deploy
- [ ] Cancellation window configured as 24h in UTC (agreed with the PO in the ticket comment) on staging and production.
- [ ] Feature flag for the guest cancel link on in staging, off in production until sign-off.

### Functional smoke
- [ ] Cancel one guest order inside the window: status CANCELLED, refund of the correct amount created.
- [ ] Cancel link of an order older than 24h shows the expired page and creates no refund.

### Regression (affected areas)
- [ ] Registered-customer cancellation from "My orders" behaves as before.
- [ ] Support-staff cancellation still works and ignores the new feature flag.
- [ ] Daily refund report includes automatic and pending refunds.

### Data/Config
- [ ] Cancellation fee and final-sale settings match between staging and production.
- [ ] [NEEDS CONFIRMATION] Store timezone used for DST checks — not stated in the ticket.

### Rollback
- [ ] Rollback plan exists / revert method confirmed: switch the feature flag off; links in already-sent emails show a "contact support" page.

### Sign-off
- [ ] QA sign-off
- [ ] PO sign-off (if required)
