import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

def train():
    df = pd.read_csv("src/mm_bot/data/dataset.csv")

    X = df[["liquidity","trades","creator_score","market_prob"]]
    y = df["resolved_prob"]

    model = RandomForestRegressor(n_estimators=300, max_depth=12)
    model.fit(X,y)

    joblib.dump(model,"src/mm_bot/ml/model.pkl")
    print("✅ Model trained and saved.")
