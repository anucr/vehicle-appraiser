import pandas as pd
import re
import numpy as np

def load_and_clean_dataset():
    file_name = "riyasewana-com-2026-05-29-2_partial.xlsx"
    
    # Read raw spreadsheet input metrics
    df = pd.read_excel(file_name)
    
    # 1. Clean and convert prices (e.g., "Rs. 8,750,000" -> 8750000)
    df['clean_price'] = df['price'].astype(str).apply(lambda x: int(re.sub(r'[^\d]', '', x)) if re.sub(r'[^\d]', '', x) else np.nan)
    
    # 2. Extract numeric mileage cleanly out of 'data3' column (e.g., "Malabe·165,000 km" -> 165000)
    def extract_km(val):
        if pd.isna(val): return np.nan
        match = re.search(r'([\d,]+)\s*km', str(val), re.IGNORECASE)
        if match:
            return int(re.sub(r'[^\d]', '', match.group(1)))
        return np.nan

    df['clean_km'] = df['data3'].apply(extract_km)
    
    # Rename key structural column mappings for clear coding architecture
    df = df.rename(columns={'data': 'model_name', 'data2': 'manufacture_year'})
    df['model_name'] = df['model_name'].astype(str).str.lower()
    
    # Drop rows that are missing critical price coordinates
    return df.dropna(subset=['clean_price'])

def estimate_vehicle_worth_range(model_query, user_year, user_km):
    df = load_and_clean_dataset()
    query = model_query.lower().strip()
    
    if not query:
        return None, "Please enter a vehicle model."
        
    # Remove spaces for robust exact letter matching (e.g. 'wagon r' matching 'wagonr')
    query_clean = query.replace(' ', '')
    df['search_name'] = df['model_name'].astype(str).str.lower().str.replace(' ', '')
    
    matched_df = df[df['search_name'].str.contains(query_clean, na=False)]
        
    if matched_df.empty:
        return None, f"No matching model '{model_query}' found in dataset."
        
    # Filter strictly by the selected year
    age_bracket_df = matched_df[matched_df['manufacture_year'] == user_year]
    
    if age_bracket_df.empty:
        return None, f"Found '{model_query}' models but none manufactured in {user_year}."
        
    analysis_pool = age_bracket_df
    
    if len(analysis_pool) == 0:
        return None, "Not enough data to form a price range."
        
    prices = analysis_pool['clean_price'].values
    
    # Step 3: Run algorithm to establish market bounding price thresholds
    avg_base = np.mean(prices)
    min_range = np.percentile(prices, 20)  # Low-end market valuation point
    max_range = np.percentile(prices, 80)  # Premium/mint market valuation point
    
    # Step 4: Apply Mileage adjustments relative to sample data cluster averages
    sample_avg_km = analysis_pool['clean_km'].mean()
    if not pd.isna(sample_avg_km) and user_km > 0:
        km_variance_ratio = (user_km - sample_avg_km) / max(1, sample_avg_km)
        # Apply up to a 10% penalty for unusually high mileage or a 5% bonus for low usage
        adjustment_factor = max(-0.10, min(0.05, -km_variance_ratio * 0.05))
        
        avg_base *= (1 + adjustment_factor)
        min_range *= (1 + adjustment_factor)
        max_range *= (1 + adjustment_factor)
        
    return {
        "average": round(avg_base, 2),
        "min_range": round(min_range, 2),
        "max_range": round(max_range, 2),
        "samples_found": len(analysis_pool)
    }, None