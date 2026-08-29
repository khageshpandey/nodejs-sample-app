---
name: api-conventions
description: Use when adding, modifying, or reviewing REST endpoints in this repo. Ensures new routes follow this project's error-handling, testing, and file-layout conventions.
---

# API Conventions for nodejs-sample-app

## When adding a new endpoint

1. Create a new file under `src/routes/<resource>.js` exporting an Express `Router`.
2. Mount it in `src/index.js` with `app.use('/<resource>', <resource>Router)`.
3. Never wrap route handlers in try/catch that sends its own error response — throw or call `next(err)` and let the centralized error handler in `src/index.js` format the response.
4. Add a test in `test/<resource>.test.js` using `node:test` + `node:assert` (see `test/health.test.js` for the pattern) — spin up the app with `app.listen(0)`, hit it with `http.get`/`http.request`, assert status code and body shape.
5. Update `README.md`'s Endpoints section with the new route.

## Response shape conventions
- Success: `{ ...data }` with appropriate 2xx status.
- Error: `{ error: "<message>" }` with appropriate 4xx/5xx status — this is enforced by the shared error handler, don't hand-roll a different shape.

## What this skill does NOT cover
- Database/ORM integration (none exists yet in this project)
- Auth/authorization middleware (not yet implemented)
- GraphQL or non-REST API styles
