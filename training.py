import pandas as pd
import joblib
import os
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import OneHotEncoder

# File paths
train_path = os.path.join("dataset", "Training.csv")
test_path = os.path.join("dataset", "Testing.csv")
model_output_path = os.path.join("dataset", "trained_model.pkl")
feature_output_path = os.path.join("dataset", "symptom_columns.pkl")

# Load datasets
train_df = pd.read_csv(train_path)
test_df = pd.read_csv(test_path)

# Drop unused column if exists
train_df.drop(columns=["Unnamed: 133"], inplace=True, errors="ignore")
test_df.drop(columns=["Unnamed: 133"], inplace=True, errors="ignore")

# Rename mapping (tidak termasuk fever)
rename_map = {
    "sore throat": "patches_in_throat",
    "difficulty swallowing": "patches_in_throat",
    "shortness of breath": "breathlessness",
    "nasal congestion": "congestion",
    "diarrhea": "diarrhoea"
}
train_df.rename(columns={k: v for k, v in rename_map.items() if k in train_df.columns}, inplace=True)
test_df.rename(columns={k: v for k, v in rename_map.items() if k in test_df.columns}, inplace=True)

# Simulate 'duration' feature based on total active symptoms
def simulate_duration(row):
    count = row.sum()
    if count <= 3:
        return "1-3 days"
    elif count <= 6:
        return "4-7 days"
    else:
        return "More than a week"

# Simulate 'severity' feature based on serious symptoms
def simulate_severity(row):
    severe_symptoms = [
        "high_fever", "vomiting", "breathlessness", "dehydration",
        "abdominal_pain", "loss_of_appetite", "diarrhoea", "malaise"
    ]
    score = sum([row.get(symptom, 0) for symptom in severe_symptoms if symptom in row])
    if score == 0:
        return "Mild"
    elif score <= 2:
        return "Moderate"
    else:
        return "Severe"

# Add duration & severity
for df in [train_df, test_df]:
    df["duration"] = df.drop(columns=["prognosis"]).apply(simulate_duration, axis=1)
    df["severity"] = df.drop(columns=["prognosis"]).apply(simulate_severity, axis=1)

# Convert "fever" → "mild_fever" or "high_fever" based on severity
for df in [train_df, test_df]:
    if "fever" in df.columns:
        df["mild_fever"] = df.apply(lambda row: 1 if row.get("fever", 0) == 1 and row["severity"] == "Mild" else 0, axis=1)
        df["high_fever"] = df.apply(lambda row: 1 if row.get("fever", 0) == 1 and row["severity"] in ["Moderate", "Severe"] else 0, axis=1)
        df.drop(columns=["fever"], inplace=True)

# Pisahkan fitur & label
X_train_full = train_df.drop(columns=["prognosis"])
y_train_full = train_df["prognosis"]
X_test = test_df.drop(columns=["prognosis"])
y_test = test_df["prognosis"]

# Encode categorical
try:
    encoder = OneHotEncoder(sparse=False, handle_unknown='ignore')
except TypeError:
    encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')

encoded_train = encoder.fit_transform(X_train_full[["duration", "severity"]])
encoded_test = encoder.transform(X_test[["duration", "severity"]])

X_train_symptoms = X_train_full.drop(columns=["duration", "severity"])
X_test_symptoms = X_test.drop(columns=["duration", "severity"])

X_train_encoded = pd.concat([
    X_train_symptoms.reset_index(drop=True),
    pd.DataFrame(encoded_train, columns=encoder.get_feature_names_out(["duration", "severity"]))
], axis=1)

X_test_encoded = pd.concat([
    X_test_symptoms.reset_index(drop=True),
    pd.DataFrame(encoded_test, columns=encoder.get_feature_names_out(["duration", "severity"]))
], axis=1)

# Simpan nama kolom akhir
final_feature_columns = X_train_encoded.columns.tolist()

# Grid search model terbaik
param_grid = {
    "n_estimators": [100, 200, 300],
    "max_depth": [None, 10, 20],
    "min_samples_split": [2, 5, 10]
}
grid_search = GridSearchCV(RandomForestClassifier(random_state=42), param_grid, cv=3, n_jobs=-1)
grid_search.fit(X_train_encoded, y_train_full)
best_model = grid_search.best_estimator_

# Validasi
cv_scores = cross_val_score(best_model, X_train_encoded, y_train_full, cv=5)
print(f"[Cross-Validation Accuracy] Mean: {cv_scores.mean()*100:.2f}%, Std: {cv_scores.std()*100:.2f}%")

X_train, X_val, y_train, y_val = train_test_split(X_train_encoded, y_train_full, test_size=0.2, random_state=42)
best_model.fit(X_train, y_train)

val_preds = best_model.predict(X_val)
test_preds = best_model.predict(X_test_encoded)

print(f"[Validation Accuracy] {accuracy_score(y_val, val_preds) * 100:.2f}%")
print(f"[Testing Accuracy] {accuracy_score(y_test, test_preds) * 100:.2f}%")

print("\nClassification Report (Validation):")
print(classification_report(y_val, val_preds))

print("\nClassification Report (Testing):")
print(classification_report(y_test, test_preds))

# Save model & fitur
joblib.dump(best_model, model_output_path)
joblib.dump(final_feature_columns, feature_output_path)

print("✅ Model and features with dynamic fever handling saved successfully.")
