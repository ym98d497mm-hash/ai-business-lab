# Task 001 — Python Customer Tracker

Priority: High
Status: Core implementation complete; documentation pending
Updated: 2026-11-05

## Goal

Build a beginner-friendly Python application to add, display,
and search customers, with local JSON storage and automated tests.

## Completed

- [x] Add customers with required names and phone numbers.
- [x] Support optional notes.
- [x] Display saved customers.
- [x] Search by partial name, ignoring capitalization.
- [x] Provide a menu for adding, viewing, searching, and exiting.
- [x] Save and load records locally using customers.json.
- [x] Reject blank required fields and invalid menu choices.
- [x] Handle missing or damaged data files.
- [x] Exclude customer data and Python cache files from Git.
- [x] Pass all 10 unittest tests.
- [x] Commit and push implementation and tests to GitHub.

## Files

- Application: projects/customer-tracker/app.py
- Tests: tests/test_customer_tracker.py
- Local data: projects/customer-tracker/customers.json
- Git exclusions: .gitignore

## Verification

All 10 automated tests passed on Windows with Python 3.11.
The user also confirmed the menu, customer entry, JSON saving,
and name search worked.

## Remaining

- [ ] Add a project README with Windows and Mac instructions.
- [ ] Commit and push the updated documentation.

## Limitations

- Phone numbers must be nonblank; format is not validated.
- Duplicate customers are allowed.
- Editing and deleting customers are not implemented.
- Customer data is local and is not encrypted by this application.
- Customer data does not sync through GitHub.