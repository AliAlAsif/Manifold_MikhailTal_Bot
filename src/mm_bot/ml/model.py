import joblib
import os

MODEL_PATH = "src/mm_bot/ml/model.pkl"

def load_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    else:
        from sklearn.ensemble import RandomForestRegressor
        return RandomForestRegressor()
