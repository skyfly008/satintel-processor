# ASIP - Automated Satellite Intelligence Processor

🛰️ **Real-time satellite imagery analysis with AI-powered building detection**

---

## 🎯 Project Overview

ASIP is a web-based geospatial intelligence platform that demonstrates automated satellite imagery analysis capabilities similar to those used by defense and intelligence agencies. It provides:

- **Interactive map interface** for selecting areas of interest
- **Automated building detection** using computer vision
- **Current-state analysis** with instant results
- **Statistical analysis** and metrics
- **Mission-style dashboard** for analysts

Perfect for portfolios targeting: **Space Force, NGA, NRO, defense contractors, geospatial AI roles**

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend (Leaflet.js)                   │
│  - Interactive map with click-to-analyze                     │
│  - Results visualization and statistics dashboard            │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ↓ REST API
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                           │
│  - Task submission and processing                            │
│  - Results caching and retrieval                             │
│  - Static file serving                                       │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────────────────────────┐
│                  Satintel Core Modules                       │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐        │
│  │   Imagery    │ │    Models    │ │   Analysis   │        │
│  │  Management  │ │   Building   │ │  Statistics  │        │
│  │              │ │  Detection   │ │  & Metrics   │        │
│  └──────────────┘ └──────────────┘ └──────────────┘        │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────────────────────────┐
│                      Data Storage                            │
│  - Current satellite tiles (NYC, Tehran)                     │
│  - Precomputed building masks                                │
│  - Generated overlays and cache                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
satinel-processor/
├── app/                      # FastAPI backend
│   ├── main.py              # Application entry point
│   ├── schemas.py           # Pydantic models
│   └── routes/              # API endpoints
│       ├── health.py        # Health & status
│       └── task.py          # Task submission & results
│
├── satintel/                # Core analysis modules
│   ├── imagery.py           # Image loading & tile management
│   ├── models.py            # Building detection models
│   └── analysis.py          # Statistics & metrics
│
├── data/                    # Data storage
│   ├── imagery/             # Satellite tiles
│   │   ├── new_york/
│   │   └── tehran/
│   ├── masks/               # Precomputed building masks
│   ├── cache/               # Processing cache
│   └── metadata/            # Tile metadata
│
├── static/                  # Frontend assets
│   ├── css/
│   ├── js/
│   ├── imagery/             # Served images
│   └── overlays/            # Served overlays
│
├── templates/               # HTML templates
│   └── index.html          # Main UI
│
├── config/                  # Configuration
│   ├── settings.py         # App settings
│   └── areas.py            # AOI definitions
│
├── scripts/                 # Utility scripts
│   └── (download scripts, preprocessing, etc.)
│
├── tests/                   # Unit tests
│
├── requirements.txt         # Python dependencies
├── .env.example            # Environment template
└── README.md               # This file
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Sentinel Hub account (for live data - optional)
- USGS Earth Explorer account (for live data - optional)

### Installation

1. **Clone the repository**
   ```bash
   cd c:\Users\ML05\Projects\ASIP\satinel-processor
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   copy .env.example .env
   # Edit .env with your API keys
   ```

5. **Download sample imagery** (TODO: Create download script)
   ```bash
   python scripts/download_sample_data.py
   ```

### Running the Application

```bash
# Development mode
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

Access the application at: `http://localhost:8000`

---

## 🔧 Development Roadmap

### Phase 1: Core Infrastructure ✅ (Current)
- [x] Project structure and placeholders
- [x] FastAPI backend skeleton
- [x] Frontend map interface
- [x] Data directory structure

### Phase 2: Data Acquisition (Next)
- [ ] Download script for Sentinel-2 imagery (NYC)
- [ ] Download script for Sentinel-2 imagery (Tehran)
- [ ] Image preprocessing pipeline
- [ ] Tile organization and metadata generation

### Phase 3: Building Detection
- [ ] Select/train building segmentation model
- [ ] Implement detection pipeline
- [ ] Generate precomputed masks for demo
- [ ] Polygon extraction and vectorization

### Phase 4: Analysis & Statistics
- [ ] Building counting and metrics
- [ ] Area calculations
- [ ] Density analysis
- [ ] Overlay generation

### Phase 5: Change Detection
- [ ] Temporal comparison logic
- [ ] New/removed building detection
- [ ] Change visualization
- [ ] Activity scoring

### Phase 6: Integration & Testing
- [ ] API endpoint implementation
- [ ] Frontend-backend integration
- [ ] End-to-end testing
- [ ] Performance optimization

### Phase 7: Deployment
- [ ] Dockerization
- [ ] Render.com deployment
- [ ] Production configuration
- [ ] Documentation finalization

---

## 🎨 Demo Features

### For Recruiters/Interviewers:

1. **Interactive Map**
   - Click anywhere in NYC or Tehran
   - Instant satellite imagery retrieval

2. **Real-time Analysis**
   - Building detection overlay
   - Statistical summaries
   - Change detection (when available)

3. **Professional UI**
   - Mission-style dark theme
   - Clean data visualization
   - Analyst-focused dashboard

4. **Technical Depth**
   - Computer vision (building segmentation)
   - Geospatial processing
   - FastAPI backend
   - Modern frontend (Leaflet.js)

---

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PyTorch** - Deep learning for building detection
- **OpenCV / Pillow** - Image processing
- **NumPy / scikit-image** - Numerical processing

### Frontend
- **Leaflet.js** - Interactive mapping
- **Vanilla JavaScript** - Clean, dependency-free
- **CSS3** - Mission-style dark theme

### Data
- **Sentinel-2** - 10m resolution satellite imagery
- **USGS Earth Explorer** - Alternative imagery source

### Deployment
- **Render.com** - Free-tier web hosting
- **Docker** - Containerization

---

## 📊 Technical Highlights

### Computer Vision
- Building segmentation using deep learning
- Instance detection and counting
- Change detection algorithms
- Overlay visualization

### Geospatial
- Coordinate snapping to available tiles
- Area/distance calculations
- Multi-temporal analysis

### Software Engineering
- Clean architecture (separation of concerns)
- RESTful API design
- Async processing
- Caching strategies
- Comprehensive error handling

---

## 🎯 Career Positioning

This project demonstrates capabilities in:

✅ **Geospatial Intelligence** - Core ISR analyst workflow  
✅ **Computer Vision** - Applied AI for defense use cases  
✅ **Full-Stack Development** - End-to-end system design  
✅ **Data Pipelines** - Imagery → Analysis → Insights  
✅ **UI/UX for Analysts** - Mission-focused design  

Perfect for roles at:
- Space Force / NGA / NRO
- Palantir, Anduril, BlackSky
- Defense contractors (RII, Booz Allen, etc.)
- Geospatial AI companies

---

## 📝 License

MIT License - See LICENSE file for details

---

## 👤 Author

**ML05** - Defense Intelligence & Geospatial AI Portfolio Project

---

## 🔗 Links

- Live Demo: (TODO: Add Render.com URL)
- Portfolio: (TODO: Add portfolio link)
- GitHub: https://github.com/skyfly008/satintel-processor

---

## 📧 Contact

For questions or collaboration: (TODO: Add contact info)

---

**Note**: This is a demonstration project using synthetic/pre-downloaded imagery. No classified or sensitive satellite data is used.
