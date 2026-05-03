"""Agri Predict Streamlit demo (copied project folder).
- Same compact preprocessing, feature engineering, and model code as the main app.
- Keep it simple: load CSV, train light RandomForest, and quickly visualize predictions.
"""

import streamlit as st  # streamlit for web app
import pandas as pd     # pandas for data manipulation
import numpy as np      # numpy for numerical operations
from sklearn.ensemble import RandomForestRegressor     #Random Forest model from sklearn 
from sklearn.model_selection import train_test_split    #train-test split function
from sklearn.preprocessing import LabelEncoder, StandardScaler    #Label encoding and feature scaling 
from sklearn.metrics import mean_absolute_error, r2_score   #evaluation metrics of the model
import plotly.graph_objects as go   #plotly for interactive visualizations

st.set_page_config(page_title=" V's AgriPredict", page_icon="🌽", layout="wide")   #page title , icon , layout   
st.title("🌽  V's AgriPredict")  # Title
st.markdown("Fast agricultural production predictions")  # Subtitle


# 1) FAST PREPROCESSING FOR FAO DATA

@st.cache_data # Cache the preprocessing function for efficiency
def preprocess(df):     # Preprocess the FAO dataset
    # identifier columns to keep during melt
    idv = ['Area Code','Area Code (M49)','Area','Item Code','Item Code (CPC)',
           'Item','Element Code','Element','Unit']                              # Identifier variables
    df_long = df.melt(id_vars=idv, var_name="Year", value_name="Value") # Reshape to long format
    df_long["Year"] = df_long["Year"].str.replace("Y", "").astype(int)  # Extract year as integer
    df_long = df_long.dropna(subset=["Value"])                       # Drop rows with missing values

    # pivot to make elements columns (production, yield, etc.)
    df_p = df_long.pivot_table(        
        index=["Area","Item","Year"],  # Pivot to wide format
        columns="Element",          # Columns are elements
        values="Value", #  Values are the measurements
        aggfunc="first" # First occurrence if duplicates
    ).reset_index()   # Reset index after pivot

    # tidy column names for easier downstream use
    df_p.columns = [c.replace(" ", "_").lower() for c in df_p.columns] # Clean column names
    return df_p # Return preprocessed DataFrame


# 2) SMART FEATURES

# Create lagged and rolling features which are useful for time-based predictions
def add_features(df):  # Add features to the DataFrame
    df = df.sort_values(["area","item","year"]) # Sort by area, item, year
    for col in ["production","yield","area_harvested"]:  # Lag features
        if col in df:  # Check if column exists
            df[f"{col}_lag1"] = df.groupby(["area","item"])[col].shift(1)  # 1-year lag
            df[f"{col}_lag2"] = df.groupby(["area","item"])[col].shift(2)   #

    if "production" in df: # Rolling average feature
        df["prod_roll3"] = df.groupby(["area","item"])["production"]\
                               .transform(lambda x: x.rolling(3,min_periods=1).mean()) # 3-year rolling mean

    df["year_norm"] = df["year"] - 1960  # Normalize year   # Year normalization
    df["area_code"] = df["area"].astype("category").cat.codes  # Area encoding
    df["item_code"] = df["item"].astype("category").cat.codes  # Item encoding
    df["weather"] = 0.8 + 0.4 * np.sin(df["year_norm"]*0.1 + df["area_code"]*0.5) # Simulated weather index
    df["crop_factor"] = 0.7 + 0.6 * ((df["item_code"] % 10)/10) # Simulated crop factor

    df = df.ffill().bfill().fillna(0)  # Fill missing values
    return df # Return DataFrame with new features


# 3) MODEL CLASS (LIGHT & FAST)

# Keep models small and fast: RandomForest per target
class Predictor:   # Predictor class for training and prediction
    def __init__(self):
        self.enc_area = LabelEncoder()  # Label encoder for area
        self.enc_item = LabelEncoder()  # Label encoder for item
        self.models = {}  # Dictionary to hold trained models
        self.scalers = {}  # Dictionary to hold feature scalers
        self.features = [  # Features used for prediction
            "year","area_enc","item_enc","year_norm",   # Normalized year # Encoded area # Encoded item # Year
            "production_lag1","yield_lag1","prod_roll3", # Lag features # Rolling average
            "weather","crop_factor","area_code" # Simulated weather index # Simulated crop factor
        ]

    # Fit the label encoders and add encoded columns
    def prepare(self, df):  # Prepare DataFrame for training
        df["area_enc"] = self.enc_area.fit_transform(df["area"]) # Encode area
        df["item_enc"] = self.enc_item.fit_transform(df["item"]) # Encode item
        return df # Return prepared DataFrame

    # Train a separate RandomForest for each target (lightweight and fast)
    def train(self, df): # Train models for each target variable
        targets = ["production","yield","area_harvested"]  # Target variables

        for t in targets:  # Train model for each target
            if t not in df:  # Skip if target not in DataFrame
                continue  
            df_c = df.dropna(subset=[t])  # Drop rows with missing target values

            X = df_c[self.features].fillna(0) # Features
            y = df_c[t].fillna(0)  # Target variable

            Xtr, Xts, ytr, yts = train_test_split(X,y,test_size=0.2,random_state=42) # Train-test split
            scaler = StandardScaler() # Feature scaling
            Xtr_s = scaler.fit_transform(Xtr) # Scale training features
            Xts_s = scaler.transform(Xts) # Scale testing features

            model = RandomForestRegressor(           # Random Forest model
                n_estimators=80, max_depth=12,   # Max depth of trees
                min_samples_split=5, min_samples_leaf=2,   # Min samples for split and leaf
                random_state=42, n_jobs=-1   # Use all CPU cores
            )
            model.fit(Xtr_s, ytr)   # Fit model

            self.models[t] = model   # Store trained model
            self.scalers[t] = scaler   # Store scaler

            y_pred = model.predict(Xts_s)       # Predict on test set
            st.sidebar.write(f"**{t}** — MAE: {mean_absolute_error(yts,y_pred):,.0f} | R²: {r2_score(yts,y_pred):.3f}")  # Display Evaluation metrics

    # Predict future values using latest history and trained models
    def predict(self, area, crop, year, history):  # Predict future values  
        area_e = self.enc_area.transform([area])[0] # Encode area
        crop_e = self.enc_item.transform([crop])[0] # Encode item

        latest = history.iloc[-1] # Get latest historical record

        feats = { # Feature dictionary for prediction
            "year": year,       #Year
            "area_enc": area_e, # Encoded area
            "item_enc": crop_e, # Encoded item
            "year_norm": year - 1960, # Normalized year
            "production_lag1": latest.get("production_lag1",0), # Lagged production
            "yield_lag1": latest.get("yield_lag1",0), # Lagged yield
            "prod_roll3": latest.get("prod_roll3",0), # Rolling average production
            "weather": 0.8 + 0.4*np.sin((year-1960)*0.1 + area_e*0.5), # Simulated weather index
            "crop_factor": 0.7 + 0.6*((crop_e % 10)/10), # Simulated crop factor
            "area_code": area_e # Encoded area code
        }

        feats = [feats[f] for f in self.features] # Feature list for prediction
        preds = {} # Predictions dictionary

        for t,m in self.models.items(): # Predict for each target
            val = m.predict(self.scalers[t].transform([feats]))[0] # Scale and predict
            val = max(0, val * np.random.uniform(0.97,1.04))   # tiny realism noise # Ensure non-negative prediction
            preds[t] = val # Store prediction

        return preds # Return predictions


# SESSION STATE

if "data" not in st.session_state: st.session_state.data = None # Data storage
if "pred" not in st.session_state: st.session_state.pred = Predictor() # Predictor instance
if "trained" not in st.session_state: st.session_state.trained = False # Training status


# 4) DATA LOADING
st.sidebar.header("Upload Dataset ") # Sidebar header
file = st.sidebar.file_uploader("Upload CSV", type=["csv"])  # File uploader

if file: # If file is uploaded
    with st.spinner("Processing data..."):  # Show spinner during processing
        raw = pd.read_csv(file)  # Read CSV file
        df = preprocess(raw)  # Preprocess data
        df = add_features(df) # Add features
        df = st.session_state.pred.prepare(df) # Prepare data for prediction
        st.session_state.data = df # Store data in session state
        st.sidebar.success(f"Loaded {len(df):,} records")  # Success message


# 5) Train models

if st.session_state.data is not None and not st.session_state.trained: # If data is loaded and not trained
    if st.sidebar.button("Train Models", type="primary"): # Train button
        with st.spinner("Training..."):  # Show spinner during training
            st.session_state.pred.train(st.session_state.data)   # Train models
        st.session_state.trained = True   # Update training status
        st.sidebar.success("Training complete!")   # Success message

# 6) UI OF THE PREDCITON

if st.session_state.trained:   # If models are trained
    st.header("Predict Future Values")  # Prediction Heading

    df = st.session_state.data  # Get data from session state
    col1,col2,col3 = st.columns(3) # Three columns for inputs

    with col1: # Country selection
        country = st.selectbox("Country", sorted(df["area"].unique()))  # Select country
    with col2: # Crop selection
        crop = st.selectbox("Crop", sorted(df["item"].unique())) # Select crop
    with col3: # Year selection
        next_year = df["year"].max() + 1# Next prediction year
        year = st.slider("Prediction Year", next_year, next_year+5, next_year) # Year slider
 
    if st.button("Predict", type="primary"):  # Predict button
        history = df[(df["area"]==country)&(df["item"]==crop)].sort_values("year") # Historical data for selected country and crop
        preds = st.session_state.pred.predict(country,crop,year,history) # Make predictions

        st.subheader("Results")  # Results subheader
        c = st.columns(3) # Three columns for metrics display

        def latest(col):  # Get latest historical value
            return history[col].iloc[-1] if col in history else 0 # Return latest value or 0

        metrics = [("production","tons"),("yield","kg/ha"),("area_harvested","ha")] # Metrics to display
        for i,(k,u) in enumerate(metrics): # Display metrics
            if k in preds:  # If prediction exists
                base = latest(k)    # Get latest historical value
                change = ((preds[k]-base)/base*100) if base else 0  #   Calculate percentage change
                c[i].metric(k.capitalize(), f"{preds[k]:,.0f} {u}", f"{change:+.1f}%") # Display metric with change

        # Plot
        if "production" in history:     # If production data exists
            fig = go.Figure()   # Create plotly figure
            fig.add_trace(go.Scatter(x=history["year"], y=history["production"],   # Historical production
                                     name="Historical", line=dict(width=3)))        # Add historical trace
            fig.add_trace(go.Scatter(x=[year], y=[preds["production"]],          # Predicted production
                                     name="Prediction",
                                     mode="markers", marker=dict(size=12)))         # Add prediction trace
            fig.update_layout(title=f"Production Trend — {crop} in {country}", height=420)      # Update layout
            st.plotly_chart(fig, use_container_width=True)      # Display plot

            st.write("Recent Data")     # Recent data subheader
            st.dataframe(history[["year","production","yield","area_harvested"]].tail(5))       # Display recent data
