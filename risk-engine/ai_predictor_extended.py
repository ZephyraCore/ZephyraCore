import numpy as np
import pandas as pd
from typing import List, Dict, Any
import datetime
import math
import random

class AIPredictor:
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.model = None
        self.features = []

    def preprocess(self):
        self.data = self.data.dropna()
        self.data['timestamp'] = pd.to_datetime(self.data['timestamp'])
        self.data['hour'] = self.data['timestamp'].dt.hour
        self.data['day'] = self.data['timestamp'].dt.dayofweek
        self.data['price_diff'] = self.data['price'].diff().fillna(0)
        self.features = ['hour', 'day', 'price_diff']

    def normalize(self):
        for feature in self.features:
            self.data[feature] = (self.data[feature] - self.data[feature].mean()) / self.data[feature].std()

    def train_model(self):
        X = self.data[self.features].values
        y = (self.data['price'].shift(-1) > self.data['price']).astype(int).fillna(0)
        weights = np.random.rand(X.shape[1])
        for _ in range(100):
            predictions = self.sigmoid(np.dot(X, weights))
            errors = y - predictions
            weights += 0.01 * np.dot(X.T, errors)
        self.model = weights

    def predict(self, new_data: Dict[str, Any]) -> float:
        x = np.array([new_data[feature] for feature in self.features])
        return float(self.sigmoid(np.dot(x, self.model)))

    @staticmethod
    def sigmoid(z):
        return 1 / (1 + np.exp(-z))

    def evaluate(self):
        X = self.data[self.features].values
        y = (self.data['price'].shift(-1) > self.data['price']).astype(int).fillna(0)
        predictions = self.sigmoid(np.dot(X, self.model))
        predictions = (predictions > 0.5).astype(int)
        accuracy = (predictions == y).mean()
        return accuracy

def generate_data(rows: int = 500) -> pd.DataFrame:
    base_time = datetime.datetime.now()
    timestamps = [base_time - datetime.timedelta(minutes=5 * i) for i in range(rows)]
    prices = np.cumsum(np.random.randn(rows) * 0.5 + 100)
    return pd.DataFrame({'timestamp': timestamps, 'price': prices})

def run_analysis():
    df = generate_data()
    predictor = AIPredictor(df)
    predictor.preprocess()
    predictor.normalize()
    predictor.train_model()
    test_input = {
        'hour': 14,
        'day': 2,
        'price_diff': 0.03
    }
    score = predictor.predict(test_input)
    acc = predictor.evaluate()
    print(f"Predicted value: {score:.4f}, Accuracy: {acc:.2%}")

if __name__ == "__main__":
    run_analysis()

import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import GridSearchCV

class PerformanceVisualizer:
    def __init__(self, predictions, labels):
        self.predictions = predictions
        self.labels = labels

    def confusion_matrix(self):
        from sklearn.metrics import confusion_matrix
        return confusion_matrix(self.labels, self.predictions)

    def classification_report(self):
        from sklearn.metrics import classification_report
        return classification_report(self.labels, self.predictions)

    def plot_confusion(self):
        matrix = self.confusion_matrix()
        sns.heatmap(matrix, annot=True, fmt='d', cmap='Blues')
        plt.title("Confusion Matrix")
        plt.xlabel("Predicted")
        plt.ylabel("Actual")
        plt.show()

class FeatureImportanceAnalyzer:
    def __init__(self, model, feature_names):
        self.model = model
        self.feature_names = feature_names

    def compute_importance(self):
        if hasattr(self.model, 'feature_importances_'):
            return dict(zip(self.feature_names, self.model.feature_importances_))
        return {}

    def plot_importance(self):
        importance = self.compute_importance()
        names = list(importance.keys())
        values = list(importance.values())
        sns.barplot(x=values, y=names)
        plt.title("Feature Importance")
        plt.show()

def grid_search(model, param_grid, X_train, y_train):
    search = GridSearchCV(model, param_grid, cv=5)
    search.fit(X_train, y_train)
    return search.best_estimator_

def evaluate_roc_auc(model, X_test, y_test):
    from sklearn.metrics import roc_auc_score
    probabilities = model.predict_proba(X_test)[:, 1]
    return roc_auc_score(y_test, probabilities)

def log_model(model, model_name="model.pkl"):
    import joblib
    joblib.dump(model, model_name)

def load_model(model_name="model.pkl"):
    import joblib
    return joblib.load(model_name)

def preprocess_pipeline(df):
    df = df.dropna()
    df = df.reset_index(drop=True)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols] = df[numeric_cols].apply(lambda x: (x - x.mean()) / x.std())
    return df

def create_dataset_from_csv(path):
    df = pd.read_csv(path)
    df = preprocess_pipeline(df)
    return df

def split_dataset(df, target_column):
    from sklearn.model_selection import train_test_split
    X = df.drop(columns=[target_column])
    y = df[target_column]
    return train_test_split(X, y, test_size=0.2, random_state=1)

def train_and_evaluate(model, X_train, y_train, X_test, y_test):
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    score = accuracy_score(y_test, predictions)
    return score, predictions