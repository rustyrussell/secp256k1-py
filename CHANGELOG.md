# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 0.14.0 - 2021-10-19: "In Which Bitcoin Twitter Rescues Rusty"

After 4 years of neglect, I filed a request to take over maintenance.
I hope the previous author (Ludvig Broberg) is living a joyous life
somewhere, and if he ever looks at this, is proud of the project he
created!

### Added

- extrakeys interfaces (still needs documentation).
- secp256k1_tagged_sha256 function exposed via FFI.
- CHANGELOG.md started

### Changed

- Latest libsecp256k1 version used.
- Schnorr interface is completely changed to reflect the underlying interface
  changes (which follow [BIP-340]).
- ECDH interface now supports using your own hashing functions.
- Rusty Russell is now self-appointed maintainer.

### Removed

- Schnorr partial and pair functions removed (removed from underlying lib)
- Requirement for gmp removed (removed from underlying lib)
- Support for Python 2 (but patches welcome!)

### Fixed

- Bundled source fetch now works (old git reference URL was now 404).
- Build had rotted, fixes implemented (not sure how it ever worked?).

[BIP-340]: https://github.com/bitcoin/bips/blob/master/bip-0340.mediawiki
