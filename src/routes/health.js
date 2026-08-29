const express = require('express');
const router = express.Router();

// Liveness probe target
router.get('/', (req, res) => {
  res.status(200).json({ status: 'ok', uptime: process.uptime() });
});

// Readiness probe target (extend with DB/dependency checks as needed)
router.get('/ready', (req, res) => {
  res.status(200).json({ status: 'ready' });
});

module.exports = router;
