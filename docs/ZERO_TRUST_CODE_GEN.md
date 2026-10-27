# Zero-Trust AI Code Generation & Blast Radius Scoring

> **Guideline**: Defensive Security Controls for Agent-Synthesized Patches  
> **Author**: Sri khyathi  
> **Date**: October 27, 2026  

## Key Threat Vectors Defended

| Threat Vector | Attack Mechanism | Agent Defensive Control |
| :--- | :--- | :--- |
| **Path Traversal** | `../../etc/passwd` or `..\windows\win.ini` | Relative path normalization, rejecting `..` in split path segments. |
| **Windows Device Hangs** | Target path `CON.css`, `NUL.js` | Direct lookup rejection against OS reserved device set. |
| **CSS AST Script Injection** | `javascript:alert(1)`, `expression(...)`, `@import` | Regex-driven scanning of patch unified diffs before parsing. |
| **Runaway Auto-Merges** | Large modifications touching critical logic | Blast radius scoring (<40 lines pure CSS eligible for auto-merge). |

## Forensic Verification

Every remediation execution produces a canonical JSON forensic bundle protected by a SHA-256 digest, establishing tamper-evident traceability across CI/CD pipelines.
