# CLAUDE.md

This file gives Claude Code context about this project. It's read automatically at the start of every session in this repo.

## Project overview
`nodejs-sample-app` is a minimal Express REST API used as a sandbox for practicing CI/CD pipelines, Dockerization, and Kubernetes deployment patterns.

## Stack
- Node.js 20+, Express 4
- Native `node:test` for testing (no Jest/Mocha)
- Docker multi-stage build, runs as non-root user
- No database yet - health/readiness endpoints only

## Conventions
- Routes live under `src/routes/`, one file per resource, exported as an Express Router.
- All new endpoints must have a corresponding test in `test/`.
- Errors should be passed to `next(err)` and handled by the centralized error handler in `src/index.js` - don't add per-route try/catch response handling.
- Keep `/health` (liveness) and `/health/ready` (readiness) semantics intact for any k8s probe config changes.

## Commands
- `npm run dev` - run with file watch
- `npm test` - run tests
- `npm run lint` - lint with ESLint
- `docker build -t nodejs-sample-app .` - build container image

## What NOT to do
- Don't add secrets or `.env` values to source files - use environment variables only, documented in README.
- Don't introduce a second test framework - stick to `node:test`.
- Don't run `npm publish` or push git tags without being asked explicitly.
