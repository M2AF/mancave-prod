---
name: Playwright Testing
description: Use for browser automation, UI testing, regression testing, screenshots, and workflow validation.
---

# Playwright Testing Skill

## Purpose

Use this skill whenever:

* UI changes are made
* New pages are created
* User flows are modified
* Bugs are fixed
* Regression testing is required

The goal is automated validation of real user behavior.

---

# Core Rule

Do not assume functionality works.

Verify through browser automation.

---

# Testing Workflow

## Step 1: Launch Application

Start the application.

Verify:

* Build succeeds
* No startup failures
* No console errors

---

## Step 2: Create User Journey

Model realistic user behavior.

Examples:

* Open page
* Navigate menus
* Submit forms
* Trigger modals
* Upload files
* Change settings

---

## Step 3: Execute Tests

Validate:

### Navigation

* Pages load
* Routes work
* Redirects function

### Interaction

* Buttons work
* Forms submit
* Menus open
* Dialogs appear

### Data

* API responses display
* State updates correctly
* Errors are handled

### Visual

* Layout remains intact
* Components render correctly
* Responsive layouts work

---

## Screenshot Validation

Capture screenshots for:

* Main pages
* Modified components
* Critical workflows

Compare screenshots against requirements.

Screenshots are mandatory for UI verification.

---

## Failure Investigation

If a test fails:

1. Collect screenshots
2. Collect console logs
3. Collect network logs
4. Determine root cause
5. Fix issue
6. Re-run tests

---

# Required Assertions

Prefer assertions for:

* Visibility
* Content
* Navigation
* State changes
* Error handling

Avoid tests that only verify existence.

Test behavior.

---

# Completion Criteria

Work is not complete until:

* Playwright tests pass
* Screenshots reviewed
* Console clean
* Network requests succeed
* User workflow succeeds

Passing builds alone are insufficient.

User behavior must be validated.
