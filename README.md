# V AgriPredict – AI Crop Forecasting & Simulation System

V AgriPredict is a Streamlit-based AI system for crop yield prediction, production estimation, and agricultural simulation.

It combines FAOSTAT real-world data with a custom-built machine learning engine to simulate farming conditions and recommend optimal crops.

--------------------------------------------------

## Core Capabilities

• Crop yield prediction (t/ha)  
• Production estimation (million tonnes)  
• FAO-based simulation engine  
• Top crop recommendation system  
• Confidence scoring using model uncertainty  
• Interactive scenario testing  

--------------------------------------------------

## Two System Modes

### 1. FAO Data Mode (Real Data)
- Uses FAOSTAT API
- Pulls real agricultural data
- Suitable for analysis and validation

### 2. Simulation Mode (AI Engine)
- Uses FAO-derived agronomic models
- Generates synthetic scenarios
- Runs custom Random Forest (NumPy-based)

--------------------------------------------------

## Key Technical Design

### Feature Engineering
18-dimensional FAO ecosystem feature vector:
- temperature stress
- water stress
- fertilizer efficiency
- soil quality
- irrigation benefit
- agro suitability score
- country yield index
- and more

### Model
Custom implementation:
- Decision Tree (from scratch)
- Random Forest ensemble (50 trees)
- Prediction intervals using variance

### Training
- 3500 FAO-based synthetic scenarios
- Realistic distributions based on:
  - FAO AQUASTAT
  - CLIMWAT
  - GAEZ v4
  - FAOSTAT

--------------------------------------------------

## Tech Stack

• Python  
• Streamlit  
• NumPy  
• Pandas  
• Requests  

(No sklearn or external ML libraries used)

--------------------------------------------------

## Project Structure


AgriPredict/
│
├── app.py # Main Streamlit app (your current file)
├── synthetic_version.py # Optional offline version (if you keep it)
├── requirements.txt
├── README.md


--------------------------------------------------

## How to Run

### 1. Create virtual environment

python -m venv venv
venv\Scripts\activate


### 2. Install dependencies

pip install -r requirements.txt


### 3. Run app

streamlit run app.py


--------------------------------------------------

## Data Source

FAOSTAT  
https://www.fao.org/faostat/

--------------------------------------------------

## Notes

• FAO API can be slow due to large dataset  
• Bulk download is used for efficiency  
• Simulation works offline if API fails  
• Model confidence is derived from tree variance  

--------------------------------------------------

## Output

• Yield prediction (t/ha)  
• Production estimate (Mt)  
• Confidence score (%)  
• Top crop recommendations  
• Scenario comparison  

--------------------------------------------------

## Author

Vismay Rao B. N.
