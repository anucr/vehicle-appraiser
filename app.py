# pyrefly: ignore [missing-import]
import streamlit as st
import requests
# pyrefly: ignore [missing-import]
from PIL import Image
import io
import hashlib

# Page Configuration
st.set_page_config(page_title="AI Vehicle Appraiser", page_icon="🚗", layout="centered")

# Custom CSS for Premium Design
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

    /* Global Fonts & Background */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
        font-family: 'Outfit', sans-serif;
        color: #f8fafc;
    }

    /* Titles and Headers */
    .app-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(90deg, #60a5fa 0%, #38bdf8 50%, #818cf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.2rem;
        letter-spacing: -0.03em;
    }
    
    .app-subtitle {
        font-size: 1.1rem;
        color: #94a3b8;
        text-align: center;
        margin-bottom: 2rem;
    }

    /* Container Card styling */
    .section-card {
        background: rgba(30, 41, 59, 0.45);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 24px;
        margin-top: 15px;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }

    /* Native Widget Styling overrides */
    div[data-baseweb="select"], div[data-baseweb="input"], div[data-baseweb="radio"] {
        border-radius: 10px !important;
    }
    
    /* Premium Styled Primary Button */
    div.stButton > button:first-child {
        width: 100%;
        background: linear-gradient(90deg, #3b82f6 0%, #6366f1 100%);
        border: none;
        color: white;
        padding: 14px 28px;
        border-radius: 12px;
        font-weight: 700;
        font-size: 17px;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4);
        transition: all 0.3s ease;
        margin-top: 10px;
    }

    div.stButton > button:first-child:hover {
        background: linear-gradient(90deg, #2563eb 0%, #4f46e5 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(99, 102, 241, 0.6);
    }

    div.stButton > button:first-child:active {
        transform: translateY(1px);
    }

    /* Styling Metric Cards */
    [data-testid="stMetric"] {
        background: rgba(15, 23, 42, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 14px;
        padding: 16px;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    [data-testid="stMetricValue"] {
        font-size: 30px !important;
        font-weight: 700 !important;
        background: linear-gradient(90deg, #60a5fa 0%, #a78bfa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    [data-testid="stMetricLabel"] {
        font-size: 13px !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #94a3b8 !important;
        font-weight: 600;
    }
    
    /* File Uploader Custom design */
    section[data-testid="stFileUploader"] {
        background: rgba(15, 23, 42, 0.25) !important;
        border: 2px dashed rgba(99, 102, 241, 0.3) !important;
        border-radius: 14px !important;
        padding: 16px !important;
    }

    section[data-testid="stFileUploader"]:hover {
        border-color: rgba(99, 102, 241, 0.7) !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="app-title">🚗 AI-Powered Vehicle Valuation Engine</div>', unsafe_allow_html=True)
st.markdown('<div class="app-subtitle">Upload a photo and enter vehicle details for an instant automated appraisal report.</div>', unsafe_allow_html=True)

# --- SIDEBAR DESIGN ---
st.sidebar.markdown("### ⚙️ Engine Settings")
api_key = st.sidebar.text_input("Roboflow API Key", value="rf_9fK6bX8zY3wM1vN5qP0r", type="password", help="Customize your Roboflow inference API key if needed.")
api_mode = st.sidebar.selectbox("Analysis Mode", ["Auto-Detect (API with Sim Fallback)", "Pure Simulation (No API calls)"])

st.sidebar.markdown("---")
st.sidebar.markdown("### 🛠️ Manual Adjustments")
manual_override = st.sidebar.checkbox("Enable Manual Adjustments", value=False, help="Manually override or supplement AI damage detection.")

manual_damages = []
paint_condition = 100
if manual_override:
    paint_condition = st.sidebar.slider("General Paint Quality (%)", min_value=30, max_value=100, value=90)
    manual_damages = st.sidebar.multiselect(
        "Select Vehicle Damages",
        ["Scratches", "Dents", "Bumper Crack", "Broken Light", "Cracked Windshield", "Rust Damage"],
        default=["Scratches"]
    )

# --- INPUTS PANEL ---
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("📋 Vehicle Specifications")
col1, col2 = st.columns(2)

with col1:
    brand = st.selectbox("Select Brand", ["Toyota", "Honda", "Nissan", "Suzuki"])
    year = st.slider("Manufacturing Year", min_value=2010, max_value=2026, value=2020)

with col2:
    mileage = st.number_input("Mileage (KM)", min_value=0, max_value=500000, value=50000, step=5000)
    fuel_type = st.radio("Fuel Type", ["Petrol", "Hybrid", "Diesel"], horizontal=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- IMAGE UPLOADER ---
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("📸 Automated Damage Assessment")
uploaded_file = st.file_uploader("Upload vehicle image to scan for body dents or scratches...", type=["jpg", "jpeg", "png"])

image = None
if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file)
        st.image(image, caption="Target Appraisal Vehicle", use_container_width=True)
    except Exception as e:
        st.error(f"❌ Failed to load image: {e}. Please ensure it is a valid image file.")
        image = None
st.markdown('</div>', unsafe_allow_html=True)

# --- APPRAISAL EXECUTION ENGINE ---
if st.button("🔥 Run AI Appraisal Analysis", type="primary"):
    
    # 1. Baseline Calculation Engine
    base_prices = {"Toyota": 35000, "Honda": 32000, "Nissan": 25000, "Suzuki": 18000}
    baseline = base_prices.get(brand, 20000)
    
    # Fuel Type Factor
    fuel_multipliers = {"Petrol": 1.0, "Hybrid": 1.10, "Diesel": 0.95}
    fuel_multiplier = fuel_multipliers.get(fuel_type, 1.0)
    
    # Depreciation Logic
    age_factor = max(0.2, 1 - ((2026 - year) * 0.06))
    mileage_factor = max(0.4, 1 - (mileage / 300000))
    baseline_market_value = round(baseline * age_factor * mileage_factor * fuel_multiplier, 2)
    
    # 2. Production Computer Vision REST API Integration & Fallback Simulation
    detected_damages = []
    damage_penalty = 0.0
    
    if uploaded_file is not None and image is not None:
        if api_mode == "Pure Simulation (No API calls)":
            st.info("ℹ️ Running in Pure Simulation Mode (No external API calls made).")
            # Deterministic simulation based on file content
            img_bytes = uploaded_file.getvalue()
            hasher = hashlib.md5(img_bytes)
            img_hash = int(hasher.hexdigest(), 16)
            
            # Possible damages: (Label, penalty)
            possible_damages = [
                ("Scratch", 0.04),
                ("Dent", 0.07),
                ("Paint Chip", 0.03),
                ("Cracked Windshield", 0.12),
                ("Bumper Dent", 0.06),
                ("Rust Patch", 0.10)
            ]
            num_damages = (img_hash % 3) + 1  # 1 to 3 damages
            for i in range(num_damages):
                damage_idx = (img_hash // (i + 1)) % len(possible_damages)
                name, penalty = possible_damages[damage_idx]
                confidence = 70.0 + ((img_hash // (i + 2)) % 25)
                detected_damages.append(f"{name} ({confidence:.1f}% confidence - Simulated)")
                damage_penalty += penalty
        else:
            with st.spinner("Analyzing vehicle exterior surfaces via Computer Vision API..."):
                try:
                    # Directly retrieve original bytes instead of re-saving via PIL
                    img_bytes = uploaded_file.getvalue()
                    
                    ROBOFLOW_API_URL = "https://detect.roboflow.com/car-damage-detection-ha5mm/1"
                    params = {"api_key": api_key} 
                    
                    response = requests.post(ROBOFLOW_API_URL, params=params, data=img_bytes, timeout=12)
                    
                    if response.status_code == 200:
                        predictions = response.json().get("predictions", [])
                        for pred in predictions:
                            label = pred.get("class", "damage")
                            confidence = pred.get("confidence", 0.0)
                            if confidence > 0.40: # Filter low-confidence detections
                                detected_damages.append(f"{label.title()} ({confidence*100:.1f}% confidence)")
                                damage_penalty += 0.05
                    elif response.status_code in [401, 403]:
                        st.warning("⚠️ Roboflow API key is unauthorized or invalid. Running simulated assessment fallback.")
                        # Fallback simulated damage detection
                        hasher = hashlib.md5(img_bytes)
                        img_hash = int(hasher.hexdigest(), 16)
                        possible_damages = [
                            ("Scratch", 0.04),
                            ("Dent", 0.07),
                            ("Bumper Dent", 0.06),
                            ("Cracked Windshield", 0.12)
                        ]
                        num_damages = (img_hash % 2) + 1  # 1 to 2 damages
                        for i in range(num_damages):
                            damage_idx = (img_hash // (i + 1)) % len(possible_damages)
                            name, penalty = possible_damages[damage_idx]
                            confidence = 72.0 + ((img_hash // (i + 2)) % 20)
                            detected_damages.append(f"{name} ({confidence:.1f}% confidence - Simulated)")
                            damage_penalty += penalty
                    else:
                        st.warning(f"⚠️ Vision API returned code {response.status_code}. Defaulting to basic simulation.")
                        # Default basic damage
                        detected_damages.append("Minor Scratches (Simulated Fallback)")
                        damage_penalty += 0.03
                except Exception as e:
                    st.warning(f"⚠️ Network timeout or API error ({e}). Defaulting to simulated fallback.")
                    # Default basic damage
                    detected_damages.append("Surface Imperfections (Simulated Fallback)")
                    damage_penalty += 0.03

    # Integrate manual adjustments if enabled
    if manual_override:
        # Subtract paint degradation (e.g. 100% paint is 0% deduction, 80% paint is 4% deduction)
        paint_penalty = (100 - paint_condition) * 0.002
        damage_penalty += paint_penalty
        
        # Add manual damages
        damage_map = {
            "Scratches": ("Scratch (Manual)", 0.04),
            "Dents": ("Dent (Manual)", 0.08),
            "Bumper Crack": ("Bumper Crack (Manual)", 0.06),
            "Broken Light": ("Broken Light (Manual)", 0.05),
            "Cracked Windshield": ("Cracked Windshield (Manual)", 0.15),
            "Rust Damage": ("Rust Damage (Manual)", 0.10)
        }
        for d in manual_damages:
            name, penalty = damage_map[d]
            detected_damages.append(name)
            damage_penalty += penalty

    # Apply penalty bounds capping structural deduction at 35%
    damage_penalty = min(0.35, damage_penalty)
    deduction_amount = baseline_market_value * damage_penalty
    final_value = max(0.0, baseline_market_value - deduction_amount)
    
    # --- OUTPUT METRICS DISPLAY PANEL ---
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.success("### 📊 Live Valuation Breakdown Report")
    res_col1, res_col2 = st.columns(2)
    
    with res_col1:
        st.metric(label="Baseline Market Value", value=f"${baseline_market_value:,.2f}")
        st.write(f"**Brand Baseline:** ${baseline:,}")
        st.write(f"**Fuel Adjustment:** {fuel_type} (x{fuel_multiplier})")
        st.write(f"**Condition Status:** {'Damaged' if detected_damages else 'Clean / Minor Wear'}")
    
    with res_col2:
        st.metric(label="Final Estimated Value", value=f"${final_value:,.2f}")
        if detected_damages:
            st.error(f"⚠️ **AI Deductions:** -${deduction_amount:,.2f} (-{int(damage_penalty*100)}%)")
            st.write("**Identified Faults & Adjustments:**")
            for defect in set(detected_damages):
                st.write(f"* {defect}")
        else:
            st.info("ℹ️ **AI Deductions:** $0.00 (No structural anomalies identified)")
    st.markdown('</div>', unsafe_allow_html=True)
