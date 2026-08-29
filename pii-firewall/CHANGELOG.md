# Changelog

All notable changes to PII Firewall are documented here. The project follows
[Semantic Versioning](https://semver.org/).

## [0.3.6] - 2026-08-29

### Fixed

- PERSON entities introduced by an auxiliary or copular verb are no longer
  discarded (`My name is John Doe`, `I am Sarah Connor`, and equivalent
  patient/account-holder forms).
- The imperative-command false-positive filter remains active for phrases such
  as `Compare Ana Garcia with the baseline`.

### Tests

- Added regression coverage for anonymization, false-positive filtering and
  rehydration of introduced names.

## [0.3.5] - 2026-06-14

- Previous PyPI release.

[0.3.6]: https://github.com/neretj/pii-firewall/compare/v0.3.5...v0.3.6
[0.3.5]: https://github.com/neretj/pii-firewall/releases/tag/v0.3.5
