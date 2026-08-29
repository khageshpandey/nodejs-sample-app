const test = require('node:test');
const assert = require('node:assert');
const http = require('node:http');
const app = require('../src/index');

test('GET /users returns 200 and a list of 2 sample users', async () => {
  const server = app.listen(0);
  const { port } = server.address();

  await new Promise((resolve, reject) => {
    http.get(`http://localhost:${port}/users`, (res) => {
      let data = '';
      res.on('data', (chunk) => (data += chunk));
      res.on('end', () => {
        assert.strictEqual(res.statusCode, 200);
        const body = JSON.parse(data);
        assert.strictEqual(body.users.length, 2);
        assert.ok(body.users[0].id);
        assert.ok(body.users[0].name);
        assert.ok(body.users[0].email);
        resolve();
      });
    }).on('error', reject);
  });

  server.close();
});
