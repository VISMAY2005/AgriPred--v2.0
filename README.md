# V AgriPredict – AI Crop Forecasting & Simulation System

V AgriPredict is an AI-based crop prediction and simulation system built using Streamlit. It predicts crop yield and production using FAOSTAT data and a stacked ensemble machine learning model.

The system models real agricultural conditions such as temperature, rainfall, irrigation, fertilizer usage, soil quality, and pest pressure. These inputs are transformed into a 22-feature agronomic vector derived from FAO datasets.

A stacked ensemble model is used:
• XGBoost (400 trees)
• Random Forest (300 trees)
• Ridge Regression (meta-learner)

The model is trained on 5000 realistic synthetic scenarios based on FAO distributions. It generates predictions along with confidence scores using model variance.

--------------------------------------------------

## Features

• Crop yield prediction (t/ha)  
• Production estimation  
• FAO-based simulation system  
• Top crop recommendation (Top 5)  
• Confidence scoring  
• Interactive dashboard  

--------------------------------------------------

## Tech Stack

• Python  
• Streamlit  
• NumPy, Pandas  
• Scikit-learn  
• XGBoost  
• Requests  

--------------------------------------------------

## Project Structure

AgriPredict/
│
├── app.py
├── requirements.txt
├── README.md

--------------------------------------------------

## How to Run

1. Create environment:
python -m venv venv
venv\Scripts\activate

2. Install dependencies:
pip install -r requirements.txt

3. Run:
streamlit run app.py

--------------------------------------------------

## Data Source

FAOSTAT  
https://www.fao.org/faostat/

--------------------------------------------------

## Notes

• Requires internet for FAO API  
• Falls back to simulation if API fails  
• Uses 22 engineered agronomic features  

--------------------------------------------------

## Output

• Yield prediction  
• Production estimation  
• Confidence score  
• Crop recommendations  

--------------------------------------------------

## Author

Vismay Rao B. N.
