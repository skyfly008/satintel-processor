/**
 * Main Application Controller
 * Orchestrates map, API, and UI interactions
 */

class ASIPApp {
    constructor() {
        this.mapManager = new MapManager();
        this.apiClient = new APIClient();
        this.currentTask = null;
    }

    /**
     * Initialize application
     */
    async initialize() {
        console.log('Initializing ASIP...');

        // Initialize map
        this.mapManager.initialize();

        // Setup event handlers
        this.setupEventHandlers();

        // Check backend health
        await this.checkHealth();

        console.log('ASIP ready');
    }

    /**
     * Setup UI event handlers
     */
    setupEventHandlers() {
        // Task button click
        const taskBtn = document.getElementById('task-btn');
        taskBtn.addEventListener('click', () => this.handleTaskSubmit());

        // Coordinate input enter key
        const coordInput = document.getElementById('coord-input');
        coordInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.handleTaskSubmit();
            }
        });

        // Map click handler
        this.mapManager.onMapClick((lat, lon) => {
            console.log(`Map clicked: ${lat}, ${lon}`);
        });
    }

    /**
     * Check backend health
     */
    async checkHealth() {
        const result = await this.apiClient.healthCheck();
        if (result.success) {
            console.log('Backend health:', result.health);
        } else {
            console.warn('Backend health check failed:', result.error);
            this.showError('Backend connection failed. Some features may not work.');
        }
    }

    /**
     * Handle task submission
     */
    async handleTaskSubmit() {
        // Get coordinates from input
        const coordInput = document.getElementById('coord-input');
        const coordString = coordInput.value.trim();

        if (!coordString) {
            this.showError('Please enter coordinates or click on the map');
            return;
        }

        // Parse coordinates
        const coords = this.mapManager.parseCoordinates(coordString);
        if (!coords) {
            this.showError('Invalid coordinate format. Use: lat, lon');
            return;
        }

        // Show loading state
        this.showLoading();

        // Submit task
        console.log(`Submitting task for ${coords.lat}, ${coords.lon}`);
        const result = await this.apiClient.submitTask(coords.lat, coords.lon);

        if (result.success) {
            this.displayResults(result.data);
        } else {
            this.showError(`Task failed: ${result.error}`);
        }
    }

    /**
     * Display analysis results
     */
    displayResults(data) {
        console.log('Displaying results:', data);

        // Hide loading, show results
        this.hideLoading();
        this.showResults();

        // Update images
        document.getElementById('base-image').src = data.image_url;
        document.getElementById('overlay-image').src = data.overlay_url;

        // Update statistics
        document.getElementById('building-count').textContent = 
            data.stats.building_count.toLocaleString();
        document.getElementById('built-area').textContent = 
            `${data.stats.built_area_km2.toFixed(3)} km²`;
        document.getElementById('density').textContent = 
            `${data.stats.density_per_km2.toFixed(0)} per km²`;
        document.getElementById('avg-size').textContent = 
            data.stats.avg_building_size_m2 
                ? `${data.stats.avg_building_size_m2.toFixed(0)} m²` 
                : 'N/A';

        // Update change detection if available
        if (data.change) {
            this.displayChangeDetection(data.change);
        }

        // Update metadata
        document.getElementById('meta-area').textContent = data.area_id;
        document.getElementById('meta-date').textContent = data.date;
        document.getElementById('meta-resolution').textContent = 
            `${data.resolution_m} m/pixel`;
        document.getElementById('meta-time').textContent = 
            data.processing_time_ms 
                ? `${data.processing_time_ms} ms` 
                : 'N/A';

        // Place marker on map
        this.mapManager.placeMarker(data.lat, data.lon);
    }

    /**
     * Display change detection results
     */
    displayChangeDetection(changeData) {
        const changeSection = document.getElementById('change-section');
        changeSection.classList.remove('hidden');

        document.getElementById('compared-date').textContent = changeData.compared_to;
        document.getElementById('new-buildings').textContent = 
            changeData.new_buildings.toLocaleString();
        document.getElementById('removed-buildings').textContent = 
            changeData.removed_buildings.toLocaleString();
        document.getElementById('percent-change').textContent = 
            `${changeData.percent_change.toFixed(1)}%`;
        document.getElementById('activity-score').textContent = 
            changeData.activity_score 
                ? changeData.activity_score.toFixed(0) 
                : 'N/A';
    }

    /**
     * UI state management
     */
    showLoading() {
        document.getElementById('idle-state').classList.add('hidden');
        document.getElementById('results-content').classList.add('hidden');
        document.getElementById('loading-state').classList.remove('hidden');
    }

    hideLoading() {
        document.getElementById('loading-state').classList.add('hidden');
    }

    showResults() {
        document.getElementById('idle-state').classList.add('hidden');
        document.getElementById('results-content').classList.remove('hidden');
    }

    showError(message) {
        this.hideLoading();
        alert(message); // TODO: Implement better error display
    }
}

// Initialize application when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    const app = new ASIPApp();
    app.initialize();
    
    // Make app globally accessible for debugging
    window.asipApp = app;
});
