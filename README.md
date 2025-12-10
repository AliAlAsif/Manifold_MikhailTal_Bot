
---

# **MikhailBot — Manifold Market Prediction Bot**


**Predicting Manifold Markets using Machine Learning**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Model Accuracy](https://img.shields.io/badge/Accuracy-0.76-orange.svg)]()
[![CI Pipeline](https://img.shields.io/badge/CI-GitHub_Actions-black.svg)]()

</div>

---

## 📌 **Overview**

**MikhailBot** is a lightweight machine-learning system designed to **predict outcomes of Manifold Markets** using resolved market data.
The bot:

* Scrapes Manifold markets
* Builds a structured dataset
* Trains a RandomForest classifier
* Produces probability-based predictions for YES/NO markets

This project is suitable for:

* 🤖 ML experimentation
* 🧪 Research on prediction markets
* 📊 Probabilistic forecasting
* 📦 Deployment to PyPI or HuggingFace

---

## 🚀 Features

* **Automated Dataset Collection**
  Fetches up to **1000 Manifold markets** and filters for resolved samples.

* **Clean ML Pipeline**
  RandomForest baseline classifier with ~**0.76 accuracy**.

* **Fast Inference CLI**
  Predict new markets with:

  ```bash
  python -m src.mm_bot.main --limit 5
  ```

* **Modular Project Structure**
  Easy to swap datasets, models, and vectorizers.

---

## 📁 Project Structure

```
MikhailBot/
│
├── src/mm_bot/
│   ├── data/
│   │   ├── collector.py
│   │   └── dataset.csv
│   ├── ml/
│   │   ├── trainer.py
│   │   └── model.joblib
│   └── main.py
│
├── README.md
└── pyproject.toml
```

---

## 📥 Dataset

After running:

```bash
python -m src.mm_bot.data.collector
```

You will see:

```
[INFO] Fetched 1000 markets (raw)
[INFO] Saved 101 resolved rows to dataset.csv
```

Your dataset includes:

* market name
* description
* resolution outcome
* timestamp fields
* textual metadata

---

## 🔧 Training

Run the trainer:

```bash
python -m src.mm_bot.ml.trainer
```

Example output:

```
[INFO] Samples: 101; label distribution: {0: 31, 1: 70}
[INFO] Training complete — accuracy: 0.7619
[INFO] Model saved to model.joblib
```

Model: **RandomForestClassifier**

Accuracy is calculated on a holdout validation split.

---

## 🔮 Running Predictions

Fetch and predict on new markets:

```bash
python -m src.mm_bot.main --limit 5
```

Example output:

```
Name: EU dissolves before ...?
Predicted YES probability: 0.725
Predicted label: 1
```

---

## 📦 Installation (PyPI-style)

```
pip install mikhailbot
```

> *(Replace with actual PyPI name when published)*

---

## 🤗 HuggingFace Model Card (optional snippet)

If you upload the model:

```
---
license: mit
tags:
- manifold
- prediction-markets
- randomforest
- classification
model_name: MikhailBot RandomForest v1
accuracy: 0.76
---

# MikhailBot — Manifold Market Predictor

This model predicts YES/NO outcomes of Manifold markets using textual features.
```

---



---

## 📝 License

Distributed under the **MIT License**.

---

## 🛠 Roadmap

* [ ] Switch to GradientBoosting / BERT embeddings
* [ ] Larger dataset (>10k markets)
* [ ] Deploy online prediction API
* [ ] Integrate reinforcement learning for live trading

---

