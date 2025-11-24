// Minimal frontend demo for single and batch task submission

async function postTask(payload) {
  const res = await fetch('/api/task', {method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(payload)});
  return res.json();
}

async function postBatch(payload) {
  const res = await fetch('/api/batch_task', {method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(payload)});
  return res.json();
}

// Batch mode handling would call postBatch with multiple tasks
console.log('satinel app.js loaded (batch-capable)');
