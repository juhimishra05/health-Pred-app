import joblib
from sklearn.tree import DecisionTreeClassifier

# Sample training data
X = [
    [90, 13, 180],
    [95, 14, 170],
    [110, 13, 220],
    [150, 12, 210],
    [180, 11, 260],
    [200, 10, 280],
    [130, 11, 240],
    [85, 15, 160]
]

# Labels
y = [
    "Healthy",
    "Healthy",
    "Prediabetes Risk",
    "High Diabetes Risk",
    "Very High Risk",
    "Very High Risk",
    "High Cholesterol Risk",
    "Healthy"
]

model = DecisionTreeClassifier()
model.fit(X, y)

joblib.dump(model, "model.pkl")

print("Model saved successfully!")