# AI product history: preserve evidence, not false promises

## Separate four concepts

1. **Interface history:** dated screenshots, static resources, UI design changes, visible feature names.
2. **Conversation records:** archives exported or saved with explicit user authorization and privacy controls.
3. **Model metadata:** provider, official model ID, release/deprecation dates, documented capabilities, status, source and last verification date.
4. **Model inference:** actual generation by a specified model. Only possible while authorized model serving remains available or when legal runnable weights and infrastructure exist.

Saving a 2026 ChatGPT, Gemini or Claude interface does **not** preserve that company's private model weights, training pipeline, safety mechanisms, APIs or backend service.

## Product behavior

- Show a badge/type label: visual snapshot, recorded example output, live supported model, or alternative model simulation.
- Never imply a simulated answer is a historical exact-model answer.
- Offer importers for user-provided conversation exports only with explicit consent, source validation, local/private default storage and safe rendering.
- Keep API keys in scoped secure secrets storage, never in WARC, docs or public browser bundles.
- The model status catalog must record exact primary-source documentation and date checked, and clearly mark unknown values.
- Support independent reproducible benchmark prompts only with permission and appropriate provenance.

## Reference documentation to track

OpenAI API deprecations: https://developers.openai.com/api/docs/deprecations
Gemini API deprecations: https://ai.google.dev/gemini-api/docs/deprecations

Model history is a differentiating archive vertical, not a guarantee of future proprietary inference access.
