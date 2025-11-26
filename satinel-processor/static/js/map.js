/**
 * Map Management Module
 * Handles Leaflet map initialization, user interactions, and marker placement
 */

class MapManager {
    constructor() {
        this.map = null;
        this.currentMarker = null;
        this.clickHandler = null;
        
        // AOI center points for demo areas
        this.areas = {
            new_york: { lat: 40.7128, lon: -74.0060, name: "New York City" },
            tehran: { lat: 35.6892, lon: 51.3890, name: "Tehran" }
        };
    }

    /**
     * Initialize Leaflet map
     */
    initialize(containerId = 'map') {
        // Create map centered on NYC by default
        this.map = L.map(containerId).setView([40.7128, -74.0060], 12);

        // Add OpenStreetMap tile layer
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors',
            maxZoom: 19
        }).addTo(this.map);

        // Add area markers
        this.addAreaMarkers();

        // Setup click handler
        this.setupClickHandler();

        console.log('Map initialized');
    }

    /**
     * Add markers for available AOIs
     */
    addAreaMarkers() {
        for (const [areaId, data] of Object.entries(this.areas)) {
            const marker = L.marker([data.lat, data.lon], {
                title: data.name
            }).addTo(this.map);

            marker.bindPopup(`
                <b>${data.name}</b><br>
                <small>Area ID: ${areaId}</small><br>
                <small>Click map to analyze</small>
            `);
        }
    }

    /**
     * Setup map click handler
     */
    setupClickHandler() {
        this.map.on('click', (e) => {
            const { lat, lng } = e.latlng;
            console.log(`Map clicked: ${lat.toFixed(4)}, ${lng.toFixed(4)}`);
            
            // Place marker
            this.placeMarker(lat, lng);

            // Update coord input
            const coordInput = document.getElementById('coord-input');
            if (coordInput) {
                coordInput.value = `${lat.toFixed(4)}, ${lng.toFixed(4)}`;
            }

            // Trigger callback if set
            if (this.clickHandler) {
                this.clickHandler(lat, lng);
            }
        });
    }

    /**
     * Place or update marker on map
     */
    placeMarker(lat, lon) {
        // Remove existing marker
        if (this.currentMarker) {
            this.map.removeLayer(this.currentMarker);
        }

        // Add new marker
        this.currentMarker = L.marker([lat, lon], {
            icon: L.icon({
                iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
                shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
                iconSize: [25, 41],
                iconAnchor: [12, 41],
                popupAnchor: [1, -34],
                shadowSize: [41, 41]
            })
        }).addTo(this.map);

        this.currentMarker.bindPopup(`
            <b>Analysis Point</b><br>
            <small>Lat: ${lat.toFixed(4)}</small><br>
            <small>Lon: ${lon.toFixed(4)}</small>
        `).openPopup();
    }

    /**
     * Set callback for map clicks
     */
    onMapClick(callback) {
        this.clickHandler = callback;
    }

    /**
     * Snap coordinates to nearest AOI
     */
    snapToNearestArea(lat, lon) {
        let nearest = null;
        let minDist = Infinity;

        for (const [areaId, data] of Object.entries(this.areas)) {
            const dist = Math.sqrt(
                Math.pow(lat - data.lat, 2) + 
                Math.pow(lon - data.lon, 2)
            );

            if (dist < minDist) {
                minDist = dist;
                nearest = { areaId, ...data };
            }
        }

        return nearest;
    }

    /**
     * Pan map to coordinates
     */
    panTo(lat, lon, zoom = null) {
        if (zoom) {
            this.map.setView([lat, lon], zoom);
        } else {
            this.map.panTo([lat, lon]);
        }
    }

    /**
     * Parse coordinate string (various formats)
     */
    parseCoordinates(coordString) {
        // Remove whitespace
        coordString = coordString.trim();

        // Try comma-separated
        const commaSplit = coordString.split(',');
        if (commaSplit.length === 2) {
            const lat = parseFloat(commaSplit[0]);
            const lon = parseFloat(commaSplit[1]);
            if (!isNaN(lat) && !isNaN(lon)) {
                return { lat, lon };
            }
        }

        // Try space-separated
        const spaceSplit = coordString.split(/\s+/);
        if (spaceSplit.length === 2) {
            const lat = parseFloat(spaceSplit[0]);
            const lon = parseFloat(spaceSplit[1]);
            if (!isNaN(lat) && !isNaN(lon)) {
                return { lat, lon };
            }
        }

        return null;
    }
}

// Export for use in other modules
window.MapManager = MapManager;
