/**
 * API Client Module
 * Handles communication with FastAPI backend
 */

class APIClient {
    constructor(baseURL = '') {
        this.baseURL = baseURL;
    }

    /**
     * Submit satellite analysis task
     */
    async submitTask(lat, lon, date = null, areaId = null) {
        const payload = {
            lat,
            lon,
            date,
            area_id: areaId
        };

        try {
            const response = await fetch(`${this.baseURL}/api/task`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            return { success: true, data };
        } catch (error) {
            console.error('Task submission failed:', error);
            return { success: false, error: error.message };
        }
    }

    /**
     * Get cached task result
     */
    async getTaskResult(areaId, date) {
        try {
            const response = await fetch(
                `${this.baseURL}/api/task/${areaId}/${date}`
            );

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            return { success: true, data };
        } catch (error) {
            console.error('Failed to fetch cached result:', error);
            return { success: false, error: error.message };
        }
    }

    /**
     * Get available dates for area
     */
    async getAvailableDates(areaId) {
        try {
            const response = await fetch(
                `${this.baseURL}/api/dates/${areaId}`
            );

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const dates = await response.json();
            return { success: true, dates };
        } catch (error) {
            console.error('Failed to fetch dates:', error);
            return { success: false, error: error.message };
        }
    }

    /**
     * Get list of available areas
     */
    async getAreas() {
        try {
            const response = await fetch(`${this.baseURL}/api/areas`);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const areas = await response.json();
            return { success: true, areas };
        } catch (error) {
            console.error('Failed to fetch areas:', error);
            return { success: false, error: error.message };
        }
    }

    /**
     * Health check
     */
    async healthCheck() {
        try {
            const response = await fetch(`${this.baseURL}/api/health`);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const health = await response.json();
            return { success: true, health };
        } catch (error) {
            console.error('Health check failed:', error);
            return { success: false, error: error.message };
        }
    }
}

// Export for use in other modules
window.APIClient = APIClient;
