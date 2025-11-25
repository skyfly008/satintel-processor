// Satinel Processor Frontend - Map and Analysis UI

let map;
let marker;

// Initialize map
function initMap() {
  // Center on Gainesville, FL
  map = L.map('map').setView([29.6521, -82.3393], 13);
  
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors',
    maxZoom: 18
  }).addTo(map);
  
  // Click handler for coordinate selection
  map.on('click', function(e) {
    const lat = e.latlng.lat.toFixed(6);
    const lon = e.latlng.lng.toFixed(6);
    
    // Update form fields based on mode
    const mode = document.querySelector('input[name="mode"]:checked').value;
    if (mode === 'single') {
      document.getElementById('lat').value = lat;
      document.getElementById('lon').value = lon;
    } else {
      document.getElementById('batch_lat').value = lat;
      document.getElementById('batch_lon').value = lon;
    }
    
    // Update/create marker
    if (marker) {
      marker.setLatLng(e.latlng);
    } else {
      marker = L.marker(e.latlng).addTo(map);
    }
  });
}

// Toggle between single and batch forms
function setupModeToggle() {
  document.querySelectorAll('input[name="mode"]').forEach(radio => {
    radio.addEventListener('change', (e) => {
      const singleForm = document.getElementById('single-form');
      const batchForm = document.getElementById('batch-form');
      
      if (e.target.value === 'single') {
        singleForm.style.display = 'block';
        batchForm.style.display = 'none';
      } else {
        singleForm.style.display = 'none';
        batchForm.style.display = 'block';
      }
    });
  });
}

// API call functions
async function postTask(payload) {
  const res = await fetch('/api/task', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(payload)
  });
  return res.json();
}

async function postBatch(payload) {
  const res = await fetch('/api/batch_task', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(payload)
  });
  return res.json();
}

// Display status message
function showStatus(message, isError = false) {
  const statusEl = document.getElementById('status');
  statusEl.textContent = message;
  statusEl.className = 'status-message ' + (isError ? 'error' : 'success');
  
  setTimeout(() => {
    statusEl.textContent = '';
    statusEl.className = 'status-message';
  }, 5000);
}

// Render single task results
function renderSingleResult(data) {
  const resultsContent = document.getElementById('results-content');
  
  const html = `
    <div class="result-card">
      <h3>Task: ${data.task_id}</h3>
      <p class="status">Status: ${data.status}</p>
      
      ${data.building_stats ? `
        <div class="stats-section">
          <h4>Building Statistics</h4>
          <div class="stats-grid">
            <div class="stat-item">
              <span class="stat-label">Count:</span>
              <span class="stat-value">${data.building_stats.count}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Total Area:</span>
              <span class="stat-value">${(data.building_stats.total_footprint_area / 1000).toFixed(1)}k m²</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Density:</span>
              <span class="stat-value">${data.building_stats.density_per_km2.toFixed(2)} per km²</span>
            </div>
          </div>
        </div>
      ` : ''}
      
      ${data.change_stats && data.change_stats.activity_score > 0 ? `
        <div class="stats-section">
          <h4>Change Detection</h4>
          <div class="stats-grid">
            <div class="stat-item">
              <span class="stat-label">New:</span>
              <span class="stat-value green">${data.change_stats.new}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Removed:</span>
              <span class="stat-value red">${data.change_stats.removed}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Unchanged:</span>
              <span class="stat-value">${data.change_stats.unchanged}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Activity Score:</span>
              <span class="stat-value">${data.change_stats.activity_score.toFixed(1)}/100</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Change:</span>
              <span class="stat-value">${data.change_stats.temporal_change_pct >= 0 ? '+' : ''}${data.change_stats.temporal_change_pct.toFixed(1)}%</span>
            </div>
          </div>
        </div>
      ` : ''}
      
      ${data.overlay_url ? `
        <div class="image-section">
          <h4>Detection Overlay</h4>
          <img src="${data.overlay_url}" alt="Detection overlay" class="result-image" />
          <div class="image-legend">
            ${data.change_stats && data.change_stats.activity_score > 0 
              ? '<p><strong>Color Legend:</strong></p><ul><li><span style="color: #00ff00; font-weight: bold;">● Green</span> = New buildings (added)</li><li><span style="color: #ff0000; font-weight: bold;">● Red</span> = Removed buildings (demolished)</li><li><span style="color: #ffff00; font-weight: bold;">● Yellow</span> = Unchanged buildings</li></ul>' 
              : '<p><strong>Color Legend:</strong></p><ul><li><span style="color: #ffff00; font-weight: bold;">● Yellow</span> = Detected buildings/infrastructure</li></ul>'}
          </div>
        </div>
      ` : ''}
      
      ${data.results ? `
        <div class="details-section">
          <details>
            <summary>Additional Details</summary>
            <pre>${JSON.stringify(data.results, null, 2)}</pre>
          </details>
        </div>
      ` : ''}
    </div>
  `;
  
  resultsContent.innerHTML = html;
}

// Render batch results
function renderBatchResults(data) {
  const resultsContent = document.getElementById('results-content');
  
  const html = `
    <div class="result-card">
      <h3>Batch: ${data.batch_id}</h3>
      <p class="status">Status: ${data.status}</p>
      
      <div class="stats-section">
        <h4>Batch Summary</h4>
        <div class="stats-grid">
          <div class="stat-item">
            <span class="stat-label">Total Tasks:</span>
            <span class="stat-value">${data.total_tasks}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Completed:</span>
            <span class="stat-value green">${data.completed}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Failed:</span>
            <span class="stat-value red">${data.failed}</span>
          </div>
        </div>
      </div>
      
      ${data.aggregate_stats ? `
        <div class="stats-section">
          <h4>Aggregate Statistics</h4>
          <div class="stats-grid">
            <div class="stat-item">
              <span class="stat-label">Total Detections:</span>
              <span class="stat-value">${data.aggregate_stats.total_detections}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Total Area:</span>
              <span class="stat-value">${(data.aggregate_stats.total_area_m2 / 1000).toFixed(1)}k m²</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Avg/Task:</span>
              <span class="stat-value">${data.aggregate_stats.avg_detections_per_task}</span>
            </div>
            ${data.aggregate_stats.total_new > 0 ? `
              <div class="stat-item">
                <span class="stat-label">Total New:</span>
                <span class="stat-value green">${data.aggregate_stats.total_new}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">Total Removed:</span>
                <span class="stat-value red">${data.aggregate_stats.total_removed}</span>
              </div>
            ` : ''}
            <div class="stat-item">
              <span class="stat-label">Processing Time:</span>
              <span class="stat-value">${data.aggregate_stats.processing_time_seconds}s</span>
            </div>
          </div>
          
          ${data.aggregate_stats.hotspots && data.aggregate_stats.hotspots.length > 0 ? `
            <div class="hotspots">
              <h5>Hotspots (High Activity)</h5>
              <ul>
                ${data.aggregate_stats.hotspots.map(h => 
                  `<li>${h.task_id}: Activity ${h.activity_score.toFixed(1)}</li>`
                ).join('')}
              </ul>
            </div>
          ` : ''}
        </div>
      ` : ''}
      
      <div class="task-results">
        <h4>Individual Tasks (${data.task_results.length})</h4>
        <div class="task-grid">
          ${data.task_results.map(task => `
            <div class="task-item">
              <div class="task-header">${task.task_id}</div>
              <div class="task-status">${task.status}</div>
              ${task.building_stats ? `
                <div class="task-stat">${task.building_stats.count} detections</div>
              ` : ''}
              ${task.change_stats && task.change_stats.activity_score > 0 ? `
                <div class="task-stat">Activity: ${task.change_stats.activity_score.toFixed(0)}</div>
              ` : ''}
            </div>
          `).join('')}
        </div>
      </div>
    </div>
  `;
  
  resultsContent.innerHTML = html;
}

// Handle single task submission
async function handleSingleSubmit() {
  const payload = {
    area_id: document.getElementById('area_id').value || null,
    lat: parseFloat(document.getElementById('lat').value) || null,
    lon: parseFloat(document.getElementById('lon').value) || null,
    date: document.getElementById('date').value || null,
    historical_date: document.getElementById('historical_date').value || null,
    prompt: document.getElementById('prompt').value || null,
    imagery_source: document.getElementById('imagery_source').value
  };
  
  // Remove null values
  Object.keys(payload).forEach(key => {
    if (payload[key] === null || payload[key] === '') delete payload[key];
  });
  
  try {
    showStatus('Submitting task...');
    const result = await postTask(payload);
    showStatus('Task completed successfully!');
    renderSingleResult(result);
  } catch (error) {
    showStatus('Error: ' + error.message, true);
    console.error('Task submission error:', error);
  }
}

// Handle batch task submission
async function handleBatchSubmit() {
  const centerLat = parseFloat(document.getElementById('batch_lat').value);
  const centerLon = parseFloat(document.getElementById('batch_lon').value);
  const gridSize = parseInt(document.getElementById('grid_size').value);
  const spacing = parseFloat(document.getElementById('grid_spacing').value);
  const date = document.getElementById('batch_date').value;
  const historicalDate = document.getElementById('batch_historical_date').value;
  const prompt = document.getElementById('batch_prompt').value;
  
  // Generate grid tasks
  const tasks = [];
  const halfSize = Math.floor(gridSize / 2);
  
  for (let i = 0; i < gridSize; i++) {
    for (let j = 0; j < gridSize; j++) {
      const lat = centerLat + (i - halfSize) * spacing;
      const lon = centerLon + (j - halfSize) * spacing;
      
      const task = {
        task_id: `grid_${i}_${j}`,
        lat: lat,
        lon: lon,
        date: date,
        imagery_source: 'static'
      };
      
      if (historicalDate) task.historical_date = historicalDate;
      if (prompt) task.prompt = prompt;
      
      tasks.push(task);
    }
  }
  
  const payload = { tasks };
  
  try {
    showStatus(`Submitting batch (${tasks.length} tasks)...`);
    const result = await postBatch(payload);
    showStatus('Batch completed successfully!');
    renderBatchResults(result);
  } catch (error) {
    showStatus('Error: ' + error.message, true);
    console.error('Batch submission error:', error);
  }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
  initMap();
  setupModeToggle();
  
  document.getElementById('submit-single').addEventListener('click', handleSingleSubmit);
  document.getElementById('submit-batch').addEventListener('click', handleBatchSubmit);
  
  console.log('Satinel Processor UI initialized');
});
