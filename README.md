# depwatch: Dependency Vulnerability Scanner

A lightweight security tool that scans Python project dependencies for known vulnerabilities. Upload a `requirements.txt`, and depwatch queries Google's free [OSV.dev](https://osv.dev) vulnerability database to find known security issues in the listed packages. It reports each vulnerability with its severity, its CVE identifiers, and the version that fixes it, and it keeps a scan history so you can review past assessments.

## Key features
- **Dependency scanning:** upload a `requirements.txt` to analyze a project's dependencies.
- **Vulnerability detection:** query the OSV.dev API for known vulnerabilities.
- **Severity classification:** group findings by severity, with their CVE identifiers.
- **Remediation guidance:** show the patched version that fixes each issue.
- **Scan history:** store and retrieve past scans in PostgreSQL.
- **CI/CD integration:** run scans automatically in CI, including on depwatch's own dependencies.

## Tech stack
Python · FastAPI · PostgreSQL · pytest · GitHub Actions · Render

## Built with spec-driven development
depwatch is built with [GitHub Spec Kit](https://github.com/github/spec-kit). Every feature starts as a spec in `specs/`, then becomes a plan and a task list before any code is written. The project's rules live in `.specify/memory/constitution.md`.

## Learning outcomes
- Integrating external REST APIs
- Parsing and validating dependency files
- Identifying vulnerabilities and reporting on security
- Designing and persisting data in PostgreSQL
- Automating security tests in CI/CD

## Status
🚧 In development
