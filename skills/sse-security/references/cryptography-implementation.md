# Cryptography Implementation Guide

Language-agnostic guidance for reviewing how a system protects data at rest, in transit and in
use. Grounded in NIST SP 800-57 (key management), NIST SP 800-38D (GCM), NIST SP 800-63B
(passwords), RFC 9106 (Argon2), the OWASP Cryptographic Storage and Password Storage cheat
sheets, and the NIST post-quantum FIPS (203/204/205). Use your platform's vetted library
(libsodium, Tink, the language's standard crypto module, cloud KMS SDKs) — never implement
primitives yourself.

---

## 1. Review order (80/20)

Most real-world crypto failures are not broken algorithms; they are **key handling** and
**misuse**. Check in this order:

1. **Where is the key, and who can read it?** Key in the same repo, config file, database row or
   container image as the data it protects = no protection.
2. **Is the mode authenticated?** Confidentiality without integrity (ECB, CBC/CTR without MAC)
   lets attackers tamper or run padding-oracle attacks.
3. **Are nonces/IVs unique per key?** Nonce reuse under GCM or ChaCha20-Poly1305 is catastrophic.
4. **Are passwords hashed with a slow, salted, memory-hard function?**
5. **Can keys rotate without an outage**, and is the key version recorded next to the ciphertext?
6. **Is randomness from a CSPRNG?**

---

## 2. Algorithm selection

| Use case | Recommended | Avoid / legacy |
|---|---|---|
| Symmetric encryption | AES-GCM (128 or 256-bit key), ChaCha20-Poly1305; AES-GCM-SIV or XChaCha20-Poly1305 when nonce management is hard | DES, 3DES, RC4, AES-ECB, CBC/CTR without a MAC |
| Asymmetric encryption / key transport | RSA-OAEP (≥ 2048-bit, prefer 3072), ECIES / HPKE (RFC 9180) | RSA PKCS#1 v1.5 **encryption** (Bleichenbacher-type oracles) |
| Digital signatures | Ed25519, ECDSA P-256/P-384, RSA-PSS (≥ 2048) | DSA, SHA-1-based signatures; RSA PKCS#1 v1.5 signatures are still widely used but prefer PSS for new designs |
| Key agreement | X25519, ECDH P-256/P-384 (ephemeral, for forward secrecy) | Static RSA key transport (no forward secrecy; removed in TLS 1.3) |
| Password storage | Argon2id; scrypt; bcrypt (legacy-acceptable); PBKDF2-HMAC-SHA-256 where FIPS validation is required | MD5, SHA-1, plain or salted SHA-2, any reversible encryption of passwords |
| Message authentication | HMAC-SHA-256/384, Poly1305 (inside AEAD), KMAC | MD5/SHA-1 MACs, `hash(key ‖ message)` constructions |
| Key derivation from a high-entropy secret | HKDF (RFC 5869) | Ad-hoc hashing or truncation |
| Random values / tokens | OS CSPRNG (the platform's secure-random API) | General-purpose PRNGs, time- or counter-seeded values |
| Transport | TLS 1.3; TLS 1.2 with AEAD suites and ECDHE (NIST SP 800-52 Rev.2) | SSL, TLS 1.0/1.1, static-RSA and CBC suites |

### Security strength (NIST SP 800-57 Part 1)

| Symmetric strength | RSA / DH modulus | ECC key size |
|---|---|---|
| 112 bits | 2048 | 224–255 |
| 128 bits | 3072 | 256–383 (e.g. P-256, Curve25519) |
| 192 bits | 7680 | 384–511 (e.g. P-384) |
| 256 bits | 15360 | 512+ (e.g. P-521) |

RSA-4096 sits between the 128- and 192-bit rows; it is not a 192-bit equivalent. NIST plans to
deprecate 112-bit strength after 2030 — new designs should target ≥ 128 bits.

---

## 3. Authenticated encryption (AEAD)

- **Nonce rules.** GCM uses a 96-bit nonce that must never repeat under the same key. With random
  nonces, NIST SP 800-38D limits a key to about 2^32 encryptions; beyond that, rotate the key or
  use a deterministic counter that survives restarts, or choose a nonce-misuse-resistant or
  extended-nonce AEAD (AES-GCM-SIV, XChaCha20-Poly1305).
- **Associated data (AAD).** Bind ciphertext to its context (record ID, tenant ID, field name,
  key version) so a ciphertext cannot be moved to another row or tenant and still decrypt.
- **Stored format.** Persist `key version ‖ nonce ‖ ciphertext ‖ tag` (or use a library envelope
  format such as Tink keysets). Without a key version, rotation becomes a big-bang migration.
- **Failure handling.** A tag-verification failure is a tamper signal: fail closed, never return
  partial plaintext, and log/alert without logging the data.

---

## 4. Envelope encryption and key management

**Pattern.** Encrypt data with a per-object or per-tenant **data encryption key (DEK)**; wrap the
DEK with a **key encryption key (KEK)** held in a KMS or HSM; store the wrapped DEK beside the
ciphertext. The KEK never leaves the KMS/HSM; the application only ever sees plaintext DEKs in
memory, briefly.

**Key lifecycle (NIST SP 800-57).**

| Phase | What to verify |
|---|---|
| Generation | Inside KMS/HSM or from a CSPRNG; correct length; one key per purpose (never reuse an encryption key for signing or MAC) |
| Storage | KMS/HSM or secret manager; not in source, images, config files or the same datastore as the data |
| Access | Least privilege on *use* (encrypt/decrypt) separated from *administration*; access logged and alertable |
| Cryptoperiod & rotation | Defined per key type and risk; automated. Rotating a KEK means **re-wrapping DEKs** (cheap); data is re-encrypted only when a DEK itself must change (e.g. suspected compromise) |
| Retirement | Old versions move to decrypt-only, then are destroyed after all data is re-encrypted or expired; destruction is recorded |
| Compromise | A runbook exists: revoke, rotate, re-encrypt, assess exposure window |

**Password-derived keys.** Only for user-held secrets (e.g. client-side vaults). Use Argon2id or
PBKDF2 with a unique salt; server-side data keys should come from a KMS, not from a password.

---

## 5. Password storage

Parameters below are the **OWASP Password Storage Cheat Sheet** minimums at time of writing —
tune upward until hashing takes roughly the latency budget you can afford on login, and re-check
the cheat sheet periodically.

| Algorithm | Minimum configuration | Notes |
|---|---|---|
| Argon2id (preferred) | m = 19 MiB, t = 2, p = 1 (or an equivalent trade-off such as m = 46 MiB, t = 1) | RFC 9106 also lists a higher-memory profile (e.g. 64 MiB, t = 3, p = 4) when resources allow |
| scrypt | N = 2^17, r = 8, p = 1 | Memory-hard |
| bcrypt | cost ≥ 10 | Input truncated at 72 bytes — enforce a max length or pre-hash carefully |
| PBKDF2-HMAC-SHA-256 | ≥ 600,000 iterations | Use when FIPS-140 validated primitives are required |

Always: unique per-password salt (the library handles it), constant-time verification,
**rehash on login** when parameters are upgraded, optional **pepper** held in a KMS/HSM
(not the database).

Policy side (NIST SP 800-63B): minimum length rather than composition rules, allow long
passphrases, screen against breached/common-password lists, no forced periodic rotation (rotate on
evidence of compromise), rate-limit and monitor failed attempts, offer or require phishing-resistant
MFA for high-value accounts.

---

## 6. MACs, signatures and tokens

- Verify MACs and tokens with **constant-time comparison**.
- Signed requests/webhooks: sign method, path, timestamp, body digest; reject outside a short time
  window and track nonces to prevent **replay**.
- JWT/JWS: pin the expected algorithm server-side (reject `none` and algorithm switching),
  validate `iss`, `aud`, `exp`, `nbf`; keep access tokens short-lived; publish keys via JWKS with
  key IDs to enable rotation. See RFC 8725 (JWT Best Current Practices).

---

## 7. Post-quantum readiness

NIST published FIPS 203 (ML-KEM, key encapsulation), FIPS 204 (ML-DSA, signatures) and FIPS 205
(SLH-DSA, hash-based signatures). Practical guidance today:

- **Crypto agility**: algorithm identifiers and key versions stored with data; no hard-coded
  algorithms deep in business logic.
- **Harvest-now-decrypt-later**: data that must stay confidential for 10+ years is the priority
  for hybrid (classical + ML-KEM) key exchange as platform support lands.
- Keep an inventory of where asymmetric crypto is used (TLS, signing, token issuance, key wrapping).

---

## 8. Common mistakes (what to flag in review)

| Mistake | Why it fails | Correct approach |
|---|---|---|
| ECB mode, or CBC/CTR without MAC | Reveals patterns; malleable; padding oracles | AEAD (AES-GCM, ChaCha20-Poly1305) |
| Static or reused nonce/IV | Breaks confidentiality and integrity of GCM/ChaCha | Random 96-bit nonce within limits, persistent counter, or misuse-resistant AEAD |
| Homegrown crypto (XOR, custom "encryption", Base64 as protection) | Untested; trivially broken; encoding ≠ encryption | Vetted high-level library APIs |
| Hard-coded keys or keys beside the data | Whoever reads the data reads the key | KMS/HSM, envelope encryption |
| Non-cryptographic RNG for tokens, IDs, reset links | Predictable values | CSPRNG, ≥ 128 bits of entropy for secrets |
| Early-exit string comparison of secrets | Timing side channel | Constant-time compare |
| Fast hash for passwords | GPU cracking at billions/sec | Argon2id / scrypt / bcrypt / PBKDF2 per §5 |
| Disabled certificate validation "for now" | Silent MITM exposure | Validate chain and hostname; pin only with a rotation plan |
| No key version on ciphertext | Rotation needs downtime or never happens | Store key ID/version with every ciphertext |
| Encrypting instead of avoiding | Unneeded sensitive data still leaks via logs, backups, exports | Minimise or tokenise first; encrypt what must remain |
