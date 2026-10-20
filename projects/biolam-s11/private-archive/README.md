# Private conversation archive · Biolam S-11

The DIY repository is **public**. Source dialogue is private. **Never commit plaintext, the passphrase, recovery hints, decrypted ZIPs or raw chat exports to Git.** This directory contains an offline archiver and can later hold snapshots in `snapshots/*.qar`.

**Current state:** the tool is implemented. No complete chat transcript has been exported or published yet. The existing `SOURCE-NOTES-2026-10-20.md` is an edited engineering handoff **not** a conversation export. Do not pass that file off as one.

## Crypto format (`.qar` v1)

- A 4-byte `QAR1` marker, 32-byte cryptographically random salt and 12-byte random nonce; the rest is authenticated ciphertext. File names, contents and ZIP internals are encrypted, while Git timestamps and ciphertext length remain publicly observable.
- Argon2id derives a 256-bit key from the **exact UTF-8 bytes of the user's passphrase**: memory 128 MiB, 3 iterations, 2 lanes, 32-byte output. No Unicode normalization or whitespace trimming.
- AES-256-GCM encrypts an in-memory ZIP consisting of one original export; header is authenticated as AAD. Random salt and nonce for every archive. Existing output will never be overwritten.
- No temp plaintext ZIP is created by encryption; decryption creates a local 0600 ZIP **only after authentication** and never extracts it automatically. The input chat export still exists locally: handle it separately according to your own storage policy.
- No passwords in the repository, environment variables, command arguments, shell history or logs. Prompt via `getpass()` or supply exact raw bytes via a protected file descriptor `--password-fd`.
- This is a self-contained *format*, not a claim of formal cryptographic review. The archiver assumes a trusted local machine and original export.

Dependencies: Python 3.11+, `cryptography>=42,<47` and `argon2-cffi>=23.1,<26` (system/package-manager installation is fine). Offline operation after dependency installation.

## Archiving a full conversation

Obtain an **actual transcript export** of this conversation first (e.g., UTF-8 HTML, Markdown, JSON, TXT). To preserve roles, timestamps, order, punctuation and user reactions, do not reconstruct from a technical summary. Verify that the export includes every desired message and no secrets from unrelated conversations.

From the directory containing this README:

```bash
python qar.py encrypt /path/to/full-conversation-export.html snapshots/2026-10-20-conversation.qar
python qar.py decrypt snapshots/2026-10-20-conversation.qar /tmp/biolam-recovered.zip
python -m unittest discover -s . -p 'test_qar.py' -v
```

Both commands prompt locally for the passphrase. Enter it byte-for-byte (Unicode, quotes, backslashes and punctuation are significant). It is intentionally **not repeated in this repository or documentation**. Never pass it as a CLI argument. For scripts without a TTY, `--password-fd N` reads *exact* bytes from an already-open descriptor; newlines matter.

**Git discipline:** plaintext goes to an external working area; only `snapshots/*.qar` is staged. Encrypted history in public Git is immutable in practice: all prior snapshot versions may remain retrievable even if deleted later. Use one fresh snapshot filename for each full export; keep at least one trusted offline backup of both ciphertext and the passphrase. Before pushing any ciphertext, verify encryption/decryption locally, preferably comparing restored and original raw bytes.

**Threat model:** confidentiality and tampering detection of the conversation given an uncompromised secret and trusted encryption system. Not traffic anonymity, not protection against a compromised computer, password leak, repository metadata disclosure or guaranteed availability. A very long secret does not raise AES-256's security beyond 256 bits. Ciphertext has an obvious file format and will not reliably be mistaken for harmless garbage by attackers.

**Key provenance:** the passphrase was supplied within a chat, which is itself a place where an attacker with access to the account/transcript could obtain it. Prefer a fresh secret stored outside chat for a high-assurance long-term public repository archive.
