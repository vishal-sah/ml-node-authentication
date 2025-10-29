"""
Rebuild the correct feature scaler from training data
This will create a new feature_scaler.pkl with all 41 features
"""

import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler, LabelEncoder
import os

print("="*80)
print("REBUILDING FEATURE SCALER FROM TRAINING DATA")
print("="*80)

# Load the training data
print("\n1. Loading training data...")
df = pd.read_csv('data.csv')

# Clean column names
df.columns = df.columns.str.strip().str.replace("'", "")

print(f"✓ Loaded {len(df)} samples")
print(f"✓ Columns: {len(df.columns)}")

# Separate features and labels
print("\n2. Preparing features...")
X = df.drop('class', axis=1) if 'class' in df.columns else df
y = df['class'] if 'class' in df.columns else None

# Drop 'id' column if it exists (it's not a feature for prediction)
if 'id' in X.columns:
    X = X.drop('id', axis=1)
    print(f"✓ Dropped 'id' column (not used for prediction)")

print(f"✓ Features shape: {X.shape}")

# Load the saved label encoders
print("\n3. Loading label encoders...")
label_encoders = joblib.load('models/label_encoders.pkl')
print(f"✓ Loaded encoders for: {list(label_encoders.keys())}")

# Encode categorical features
print("\n4. Encoding categorical features...")
X_encoded = X.copy()
for col, encoder in label_encoders.items():
    if col in X_encoded.columns:
        # Handle any values not seen during training
        X_encoded[col] = X_encoded[col].apply(
            lambda x: x if x in encoder.classes_ else encoder.classes_[0]
        )
        X_encoded[col] = encoder.transform(X_encoded[col])
        print(f"  ✓ Encoded {col}")

# Create and fit StandardScaler on ALL 41 features
print("\n5. Creating StandardScaler for all 41 features...")
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_encoded)

print(f"✓ Scaler fitted on {scaler.n_features_in_} features")
print(f"✓ Feature names: {list(X_encoded.columns[:5])} ... (showing first 5)")

# Save the new scaler
print("\n6. Saving new scaler...")
os.makedirs('models', exist_ok=True)

# Backup old scaler
old_scaler_path = 'models/feature_scaler.pkl'
if os.path.exists(old_scaler_path):
    backup_path = 'models/feature_scaler_old_backup.pkl'
    # Remove existing backup if present
    if os.path.exists(backup_path):
        os.remove(backup_path)
    os.rename(old_scaler_path, backup_path)
    print(f"✓ Backed up old scaler to: {backup_path}")

# Save new scaler
joblib.dump(scaler, old_scaler_path)
print(f"✓ Saved new scaler to: {old_scaler_path}")

# Verify the new scaler
print("\n7. Verifying new scaler...")
loaded_scaler = joblib.load(old_scaler_path)
print(f"✓ Loaded scaler expects {loaded_scaler.n_features_in_} features")
print(f"✓ Mean values (first 5): {loaded_scaler.mean_[:5]}")
print(f"✓ Std values (first 5): {loaded_scaler.scale_[:5]}")

# Test transformation
print("\n8. Testing transformation...")
test_sample = X_encoded.iloc[:3]
test_scaled = loaded_scaler.transform(test_sample)
print(f"✓ Successfully transformed {len(test_sample)} samples")
print(f"  Original range: [{test_sample.values.min():.2f}, {test_sample.values.max():.2f}]")
print(f"  Scaled range: [{test_scaled.min():.2f}, {test_scaled.max():.2f}]")

print("\n" + "="*80)
print("✅ FEATURE SCALER SUCCESSFULLY REBUILT!")
print("="*80)
print(f"\n📁 New scaler saved at: {os.path.abspath(old_scaler_path)}")
print(f"   Features: {scaler.n_features_in_}")
print(f"   Fitted on: {len(df)} training samples")
print("\n🚀 You can now use the Streamlit app with proper scaling!")
