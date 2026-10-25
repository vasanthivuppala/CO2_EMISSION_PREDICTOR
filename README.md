# 🚗 ExploreDrive – Four-Wheeler CO₂ Emission Prediction

ExploreDrive is a machine learning application that predicts **CO₂ emissions from four-wheeler vehicles** based on vehicle specifications. It uses Random Forest Regression and SHAP-based Explainable AI to predict emissions and explain the factors influencing each prediction.

## ✨ Key Features
- 🚘 **CO₂ Prediction:** Estimates emissions (g/km) for four-wheeler vehicles.
- 🔍 **SHAP Explainability:** Identifies the key factors influencing predictions.
- 🌱 **Eco Score:** Provides an eco score out of 100.
- 💡 **Smart Recommendations:** Suggests ways to reduce emissions.
- 📊 **Prediction History:** Stores previous predictions using SQLite.
- 🔐 **User Authentication:** Login and signup functionality.

## 🛠️ Tech Stack
- **Language:** Python
- **ML Model:** Random Forest Regression
- **Explainable AI:** SHAP
- **Libraries:** Pandas, NumPy, Scikit-learn
- **Frontend:** Streamlit
- **Database:** SQLite

## ⚙️ Installation & Setup

1. Clone the repository:
   ```bash
   git clone <your-repository-url>
   cd ExploreDrive
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run app.py
   ```

## 📈 Model Performance
- **R² Score:** 0.9992
- **Mean Cross-Validation R²:** 0.9973

## 🎯 Objective
To help users understand the environmental impact of four-wheeler vehicles by predicting CO₂ emissions, explaining prediction results, and providing insights for more environmentally conscious vehicle choices.
