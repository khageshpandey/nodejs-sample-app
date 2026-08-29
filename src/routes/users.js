const express = require('express');
const router = express.Router();

// Hardcoded sample users - replace with DB-backed lookup once persistence exists
const SAMPLE_USERS = [
  { id: 1, name: 'Ada Lovelace', email: 'ada.lovelace@example.com' },
  { id: 2, name: 'Alan Turing', email: 'alan.turing@example.com' },
];

router.get('/', (req, res) => {
  res.status(200).json({ users: SAMPLE_USERS });
});

module.exports = router;
