---
name: Fullstack Iteration
description: Default workflow for feature development, bug fixes, implementation, testing, validation, and iteration.
---

# Fullstack Iteration Skill

## Purpose

Use this skill whenever:

* New features are requested
* Existing features are modified
* Bugs are fixed
* UI changes are required
* Backend changes are required
* Fullstack workflows are involved

This skill is the default development workflow.

The objective is not to write code.

The objective is to deliver verified, working functionality through continuous implementation, testing, validation, and iteration.

---

# Core Principle

Never stop after writing code.

Code generation is only the beginning of the workflow.

Work is complete only after validation succeeds.

---

# Development Lifecycle

## Phase 1: Discovery

Before modifying code:

1. Read relevant files.
2. Understand architecture.
3. Identify affected systems.
4. Identify dependencies.
5. Identify risks.
6. Create implementation plan.

Do not immediately start coding.

---

## Phase 2: Implementation

Implement the smallest solution capable of satisfying requirements.

Prefer:

* Small changes
* Localized modifications
* Existing project patterns

Avoid:

* Unnecessary refactors
* Architecture rewrites
* New dependencies

unless explicitly requested.

---

## Phase 3: Static Validation

After implementation:

### Verify

* Imports
* Exports
* Types
* Build configuration
* Routing
* State management

### Run

* Build
* Lint
* Type checking

Fix all discovered issues.

---

## Phase 4: Runtime Validation

Launch the application.

Verify:

* Application starts successfully
* No startup failures
* No runtime exceptions
* No console errors

If errors exist:

Fix them immediately.

Do not continue until runtime is stable.

---

## Phase 5: Functional Testing

Verify all affected workflows.

Test:

* User actions
* State updates
* API interactions
* Database interactions
* Navigation
* Error handling

Use realistic user behavior.

---

## Phase 6: Playwright Validation

When Playwright is available:

Create or update tests.

Validate:

### Navigation

* Routes
* Deep links
* Refresh behavior

### Interaction

* Buttons
* Forms
* Menus
* Modals

### Data

* Loading states
* Success states
* Error states

### State

* Persistence
* Synchronization
* Updates

Do not trust manual inspection alone.

---

## Phase 7: Screenshot Validation

Capture screenshots after implementation.

Review:

### Layout

* Alignment
* Spacing
* Positioning

### Typography

* Font sizing
* Hierarchy
* Legibility

### Components

* Buttons
* Forms
* Lists
* Cards
* Modals

### Responsiveness

* Desktop
* Tablet
* Mobile

---

## Phase 8: Visual Review

Compare screenshots directly against requirements.

Identify:

* Misalignment
* Clipping
* Overflow
* Missing assets
* Incorrect colors
* Incorrect spacing

If discrepancies exist:

Return to implementation phase.

---

## Phase 9: Regression Testing

Verify that unrelated functionality remains intact.

Review:

* Existing workflows
* Existing routes
* Existing APIs
* Existing state

Ensure changes did not create regressions.

---

## Phase 10: Self Review

Review the solution as if performing a code review.

Ask:

### Correctness

Does it actually solve the problem?

### Maintainability

Will future developers understand it?

### Performance

Are there unnecessary costs?

### Security

Are there obvious risks?

### Scalability

Will it continue working as usage grows?

---

# Autonomous Iteration Loop

If any validation step fails:

1. Identify issue
2. Determine root cause
3. Fix issue
4. Rebuild
5. Retest
6. Revalidate

Repeat until successful.

Never stop after the first attempt.

---

# Completion Requirements

Work is complete only when:

* Requirements satisfied
* Build passes
* Lint passes
* Type checks pass
* Tests pass
* Runtime validation passes
* Screenshots reviewed
* Visual requirements satisfied
* No critical regressions found

---

# Required Final Report

Before finishing provide:

## Summary

What was implemented.

## Files Changed

List all modified files.

## Validation

Report:

* Build status
* Lint status
* Test status
* Playwright status
* Screenshot review status

## Risks

Any remaining concerns.

Only declare completion after all validation steps have been performed.
