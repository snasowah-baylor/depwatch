<!--
Sync Impact Report:
- Version change: unversioned -> 1.0.0
- Added principles: Security First; Test-First; Accuracy Over Speed; Simplicity; Observability
- Added sections: Security and Dependency Constraints; Development and Delivery Workflow
- Removed sections: none
- Deferred placeholders: RATIFICATION_DATE
-->

# depwatch Constitution

## Core Principles

### I. Security First

Every uploaded file is untrusted input. The application MUST validate file size and format
before processing; reject malformed, oversized, or unsupported inputs without executing,
installing, or otherwise activating uploaded content. Secrets MUST NOT appear in source code,
tests, documentation, or Git history. Runtime configuration MUST come from environment variables.

### II. Test-First (NON-NEGOTIABLE)

Tests MUST be written before implementation. Every feature MUST have automated tests covering its
behavior and relevant failure cases. External APIs, including OSV.dev, MUST be mocked in tests so
that the suite is deterministic and does not perform network calls. The CI pipeline MUST pass
before a change can merge.

### III. Accuracy Over Speed

Vulnerability results MUST cite verifiable source identifiers, including the OSV ID and CVE when
available. The application MUST NOT guess or invent vulnerability details. If an OSV or other
lookup fails, the result MUST be explicitly reported as failed or unverified, never as safe.

### IV. Simplicity

depwatch MUST use one FastAPI application and server-rendered pages. Production dependencies
MUST remain minimal. A new library MUST be justified by a concrete requirement that cannot be met
with existing dependencies or the Python standard library.

### V. Observability

The application MUST emit structured logs with sufficient context to diagnose failures without
logging secrets or uploaded content. It MUST provide a `/health` endpoint and clear, actionable
user-facing error messages.

## Security and Dependency Constraints

Uploaded content MUST be treated only as data. The application MUST NOT execute uploaded code,
install uploaded packages, or make OS calls that act on uploaded content beyond bounded validation.
Configuration and credentials MUST be supplied through environment variables with safe defaults
only for non-sensitive behavior.

## Development and Delivery Workflow

Changes MUST follow test-first development, pass the complete automated test suite, and pass CI
before merge. Pull requests MUST verify compliance with these principles and explain exceptions.
No exception may weaken source attribution, lookup failure reporting, secret handling, or untrusted
upload controls.

## Governance

This constitution supersedes all other project practices where they conflict. Amendments MUST
document a rationale and update the constitution version. Principle or governance changes require
a semantic version bump: MAJOR for incompatible removals or redefinitions, MINOR for new principles
or materially expanded guidance, and PATCH for clarification or wording-only changes. Compliance
MUST be reviewed for every feature and pull request. Any change to this constitution MUST include
a short rationale and a corresponding migration or update plan where needed.

**Version**: 1.0.0 | **Ratified**: TODO(RATIFICATION_DATE): set the actual adoption date | **Last Amended**: 2026-11-24
