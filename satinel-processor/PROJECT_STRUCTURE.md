# ASIP Project Structure Summary
Generated: November 26, 2025

## 🎯 High-Level Architecture

```
ASIP - Automated Satellite Intelligence Processor
│
├── 🌐 Frontend Layer (Leaflet.js + Vanilla JS)
│   └── Interactive map → Click coordinates → Submit analysis request
│
├── 🚀 API Layer (FastAPI)
│   └── Task submission → Processing orchestration → Results delivery
│
├── 🧠 Analysis Layer (Python Modules)
│   ├── Imagery Management (load, snap, preprocess)
│   ├── Building Detection (CV models, masks, polygons)
│   ├── Statistics & Metrics (counts, areas, density)
│   └── Change Detection (temporal comparison, activity scoring)
│
└── 💾 Data Layer
    ├── Satellite imagery tiles (pre-downloaded)
    ├── Precomputed building masks
    └── Generated overlays & cache
```

---

## 📁 Complete File Structure

```
satinel-processor/
│
├── 📂 app/                          # FastAPI Backend
│   ├── __init__.py                  # Package init
│   ├── main.py                      # App entry point, CORS, static files
│   ├── schemas.py                   # Pydantic models (request/response)
│   └── routes/
│       ├── __init__.py
│       ├── health.py                # Health check & areas listing
│       └── task.py                  # Task submission & results
│
├── 📂 satintel/                     # Core Analysis Modules
│   ├── __init__.py
│   ├── imagery.py                   # ImageryManager class
│   │   ├── snap_to_tile()          # Coordinate → tile mapping
│   │   ├── load_image()            # Load satellite imagery
│   │   ├── get_available_dates()   # List dates for area
│   │   └── preprocess_image()      # Normalization, resizing
│   │
│   ├── models.py                    # Building Detection
│   │   ├── BuildingDetector        # ML-based detection
│   │   │   ├── load_model()       # Load PyTorch model
│   │   │   ├── detect_buildings()  # Run inference
│   │   │   ├── mask_to_polygons()  # Convert to vectors
│   │   │   └── compute_bounding_boxes()
│   │   └── PrecomputedMaskLoader   # Fast demo mode
│   │       ├── load_mask()
│   │       └── save_mask()
│   │
│   ├── analysis.py                  # Statistics & Metrics
│   │   └── BuildingAnalyzer
│   │       ├── count_buildings()
│   │       ├── calculate_built_area()
│   │       ├── calculate_density()
│   │       ├── summarize_buildings()
│   │       ├── create_overlay()    # Visual overlay generation
│   │       └── save_overlay()
│   │
│   └── change_detection.py          # Temporal Analysis
│       └── ChangeDetector
│           ├── compare_masks()      # Pixel-level comparison
│           ├── compare_polygons()   # IoU-based matching
│           ├── calculate_change_stats()
│           ├── create_change_overlay()  # Red/green visualization
│           └── compute_activity_score()
│
├── 📂 data/                         # Data Storage (not committed)
│   ├── imagery/                     # Satellite tiles
│   │   ├── new_york/               # NYC tiles by date
│   │   │   ├── 2021-01-01.png
│   │   │   ├── 2023-01-01.png
│   │   │   └── .gitkeep
│   │   └── tehran/                 # Tehran tiles by date
│   │       ├── 2021-01-01.png
│   │       ├── 2023-01-01.png
│   │       └── .gitkeep
│   │
│   ├── masks/                       # Precomputed building masks
│   │   ├── new_york/
│   │   │   ├── 2021-01-01_buildings.npy
│   │   │   ├── 2023-01-01_buildings.npy
│   │   │   └── .gitkeep
│   │   └── tehran/
│   │       └── .gitkeep
│   │
│   ├── cache/                       # Processing cache
│   │   └── .gitkeep
│   │
│   └── metadata/                    # Tile metadata (coordinates, etc.)
│       └── .gitkeep
│
├── 📂 static/                       # Frontend Assets
│   ├── css/
│   │   └── main.css                # Mission-style dark theme
│   │
│   ├── js/
│   │   ├── map.js                  # MapManager class
│   │   │   ├── initialize()       # Setup Leaflet map
│   │   │   ├── setupClickHandler() # Map click events
│   │   │   ├── placeMarker()
│   │   │   ├── snapToNearestArea()
│   │   │   └── parseCoordinates()
│   │   │
│   │   ├── api.js                  # APIClient class
│   │   │   ├── submitTask()       # POST /api/task
│   │   │   ├── getTaskResult()    # GET cached results
│   │   │   ├── getAvailableDates()
│   │   │   ├── getAreas()
│   │   │   └── healthCheck()
│   │   │
│   │   └── main.js                 # ASIPApp controller
│   │       ├── initialize()       # App startup
│   │       ├── setupEventHandlers()
│   │       ├── handleTaskSubmit()
│   │       ├── displayResults()   # Update UI with results
│   │       └── displayChangeDetection()
│   │
│   ├── imagery/                     # Served satellite images (symlink/copy)
│   └── overlays/                    # Generated overlay images
│
├── 📂 templates/
│   └── index.html                   # Main UI
│       ├── Header (title, coord input, task button)
│       ├── Map panel (left side)
│       └── Results panel (right side)
│           ├── Image comparison (base vs overlay)
│           ├── Statistics cards (buildings, area, density)
│           ├── Change detection section
│           └── Metadata display
│
├── 📂 config/
│   ├── settings.py                  # App configuration
│   │   └── Settings class (env vars, paths, model config)
│   │
│   └── areas.py                     # AOI definitions
│       ├── AREAS dict (NYC, Tehran metadata)
│       ├── get_area_by_id()
│       ├── get_all_areas()
│       └── find_nearest_area()
│
├── 📂 scripts/                      # Utility Scripts
│   └── download_sample_data.py      # Download Sentinel/USGS imagery
│       ├── download_sentinel_tile()
│       ├── download_usgs_tile()
│       └── preprocess_imagery()
│
├── 📂 tests/
│   ├── test_satintel.py            # Core module tests
│   └── test_api.py                 # API endpoint tests
│
├── 📄 requirements.txt              # Python dependencies
├── 📄 .env.example                  # Environment template
├── 📄 .gitignore                    # Git ignore rules
└── 📄 README.md                     # Project documentation
```

---

## 🔄 Data Flow

### Task Submission Flow
```
1. User clicks map → (lat, lon) captured
   ↓
2. Frontend: ASIPApp.handleTaskSubmit()
   ↓
3. API: POST /api/task { lat, lon, date? }
   ↓
4. Backend: ImageryManager.snap_to_tile()
   → Find nearest available tile
   ↓
5. Backend: ImageryManager.load_image(area_id, date)
   → Load satellite imagery
   ↓
6. Backend: BuildingDetector.detect_buildings(image)
   → Run model OR load precomputed mask
   ↓
7. Backend: BuildingAnalyzer.summarize_buildings(mask)
   → Calculate stats
   ↓
8. Backend: BuildingAnalyzer.create_overlay(image, mask)
   → Generate visualization
   ↓
9. Backend: [Optional] ChangeDetector.compare_masks(prev, curr)
   → Run change detection
   ↓
10. Backend: Return TaskResponse JSON
    {
      area_id, date, lat, lon,
      image_url, overlay_url,
      stats: { count, area, density },
      change: { new, removed, percent_change }
    }
    ↓
11. Frontend: ASIPApp.displayResults(data)
    → Update UI with images + statistics
```

---

## 🎨 UI Components

### Header Bar
- **Title**: 🛰️ ASIP - Automated Satellite Intelligence Processor
- **Coord Input**: Text field for lat/lon entry
- **Task Button**: Submit analysis request

### Map Panel (Left)
- **Leaflet map** centered on demo areas
- **Area markers** for NYC and Tehran
- **Click-to-analyze** interaction
- **Red marker** on selection

### Results Panel (Right)

#### Idle State
- Welcome message
- Feature list
- Instructions

#### Loading State
- Spinner animation
- "Analyzing imagery..." message

#### Results State

**Image Section**
- Base satellite image
- Overlay with building highlights

**Statistics Cards** (2x2 grid)
- Buildings Detected
- Built Area (km²)
- Density (per km²)
- Avg Building Size (m²)

**Change Detection Section** (if available)
- Compared date
- New buildings (green)
- Removed buildings (red)
- Percent change
- Activity score

**Metadata**
- Area ID
- Date
- Resolution (m/pixel)
- Processing time (ms)

---

## 🛠️ Technology Decisions

### Why FastAPI?
- Modern async Python framework
- Automatic OpenAPI docs
- Pydantic validation
- Fast performance

### Why Leaflet.js?
- Lightweight (40KB)
- Easy integration
- No API keys required (OSM tiles)
- Perfect for demo

### Why Vanilla JavaScript?
- No build step
- Fast loading
- Easy to understand
- Professional code quality

### Why Precomputed Masks?
- **Demo speed**: Instant results
- **Deployment**: Works without GPU
- **Development**: Focus on architecture first
- **Future**: Can swap in real model later

---

## 🚀 Next Steps (Development Phases)

### Phase 2: Data Acquisition
1. **Download NYC imagery** (3-4 dates)
   - Use Sentinel Hub API OR manual download
   - Dates: 2021, 2022, 2023, 2024
   - Coverage: Manhattan + surrounding areas

2. **Download Tehran imagery** (3-4 dates)
   - Same date range
   - Coverage: Central Tehran

3. **Preprocessing**
   - Resize to 1024x1024
   - Save as PNG (for demo) or GeoTIFF (for production)
   - Generate metadata JSON

### Phase 3: Building Detection
1. **Option A: Pretrained model**
   - Download SpaceNet-trained UNet
   - Or use Mask R-CNN from torchvision
   - Run inference on all tiles
   - Save masks as .npy

2. **Option B: Manual annotation** (fast demo)
   - Use QGIS or labelme
   - Annotate 2-3 tiles manually
   - Generate synthetic masks
   - Perfect for proof of concept

### Phase 4: Implementation
1. **Complete TODO items** in all modules
2. **Integrate** components end-to-end
3. **Test** with real data
4. **Optimize** performance
5. **Add error handling**

### Phase 5: Deployment
1. **Docker** containerization
2. **Render.com** deployment
3. **Environment** configuration
4. **Domain** setup (optional)

---

## 💡 Key Design Decisions

### Modularity
Each module has a **single responsibility**:
- `imagery.py` → Data loading only
- `models.py` → Detection only
- `analysis.py` → Statistics only
- `change_detection.py` → Temporal comparison only

### Extensibility
Easy to swap components:
- Precomputed masks → Real ML model
- OSM tiles → Satellite base map
- Static data → Live API integration

### Simplicity
- No complex dependencies
- No database (files only)
- No authentication (demo mode)
- No WebSockets (HTTP only)

### Career Focus
Designed to showcase:
- ✅ Geospatial processing
- ✅ Computer vision
- ✅ Full-stack development
- ✅ Clean architecture
- ✅ Production-ready code

---

## 📊 Metrics for Success

### Technical
- [x] Clean project structure
- [x] Comprehensive documentation
- [x] Modular architecture
- [ ] Working end-to-end demo
- [ ] <1 second response time
- [ ] Deployed to Render.com

### Career
- [x] GitHub-ready codebase
- [x] Professional README
- [ ] Live demo URL
- [ ] Portfolio integration
- [ ] LinkedIn post-worthy

---

## 🎯 Portfolio Positioning

**Elevator Pitch:**
> "I built ASIP - an automated satellite intelligence processor that demonstrates 
> the full pipeline used by NGA and defense contractors: imagery acquisition → 
> AI-powered building detection → change analysis → analyst dashboard. 
> It's deployed at [URL] and showcases my geospatial AI and full-stack skills."

**Technical Keywords:**
- Geospatial Intelligence (GEOINT)
- Satellite Imagery Analysis
- Computer Vision (Building Segmentation)
- Change Detection
- FastAPI Backend
- Interactive Mapping (Leaflet.js)
- Full-Stack Python

**Target Roles:**
- Space Force / NGA / NRO
- Palantir, Anduril, BlackSky
- Defense contractors (RII, Booz Allen, Northrop)
- Geospatial AI startups

---

## 📝 Notes

### API Keys Needed (Phase 2)
- **Sentinel Hub**: Sign up at https://www.sentinel-hub.com/
- **USGS**: Register at https://earthexplorer.usgs.gov/

### Alternative Data Sources
- **Maxar Open Data**: https://www.maxar.com/open-data
- **Planet Labs**: Free trial available
- **Google Earth Engine**: Academic access

### Model Options
- **SpaceNet**: Pretrained on satellite building detection
- **Mask R-CNN**: General instance segmentation
- **DeepLabV3+**: Semantic segmentation
- **UNet**: Lightweight, fast

---

**Status**: ✅ Project structure complete, ready for Phase 2 (data acquisition)

**Next Action**: Download sample Sentinel-2 imagery for NYC and Tehran
