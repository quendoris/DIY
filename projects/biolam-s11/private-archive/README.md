# Private archive integration

**This is a public repository. Do not commit unencrypted chat exports, private messages, plaintext ZIPs or passphrases.**

The reusable encrypt/decrypt CLI and its tests live in [quendoris/snippets → qar-authenticated-archive](https://github.com/quendoris/snippets/tree/feat/qar-authenticated-archive/qar-authenticated-archive). The DOI/DIY microscope project owns only policy and links, not duplicate cryptographic code.

An encrypted conversation backup may be placed in this project's `snapshots/*.qar` after verifying its original source and a successful decrypt/byte-for-byte check locally. **There is currently no `.qar` snapshot committed in this repository**; the user keeps the created local copy.

The project handoff is [SOURCE-NOTES-2026-10-20.md](../SOURCE-NOTES-2026-10-20.md) (an edited engineering record, not a verbatim transcript). Exporting a complete transcript and encoding/verifying it is a separate workflow.

Security caveat: ciphertext committed to public Git persists in Git history. Deleting it later does not reliably erase old copies.
