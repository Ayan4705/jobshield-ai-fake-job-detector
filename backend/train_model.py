import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Load dataset
df = pd.read_csv("data/fake_job_postings.csv")

df = df[['description', 'fraudulent']]
df.dropna(inplace=True)

X = df['description']
y = df['fraudulent']

# Vectorize
vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
X_vec = vectorizer.fit_transform(X)

# Train / Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X_vec, y,
    test_size=0.2,
    random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
print("\n===== Model Evaluation =====")
print(classification_report(y_test, y_pred))

# Top 20 important features
feature_names = vectorizer.get_feature_names_out()
importances = model.feature_importances_
top_indices = importances.argsort()[::-1][:20]

print("\n===== Top 20 Important Words =====")
for i in top_indices:
    print(f"  {feature_names[i]:<20} {importances[i]:.4f}")

# Save model
joblib.dump(model, "models/trained_model.pkl")
joblib.dump(vectorizer, "models/vectorizer.pkl")

print("\nModel Trained and Saved")