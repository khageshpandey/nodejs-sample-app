# nodejs-sample-app

Minimal Express REST API used as a sandbox for local dev, CI/CD, and container/K8s testing.

## Run locally
```bash
npm install
npm run dev
```

## Run tests
```bash
npm test
```

## Build and run with Docker
```bash
docker build -t nodejs-sample-app .
docker run -p 3000:3000 nodejs-sample-app
```

## Endpoints
- `GET /` - basic status message
- `GET /health` - liveness probe
- `GET /health/ready` - readiness probe
- `GET /users` - hardcoded list of sample users
