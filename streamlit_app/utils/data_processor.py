"""
Data Processor Module
Handles CSV validation, preprocessing, and prediction
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any


class DataProcessor:
    """Process data for predictions"""
    
    def __init__(self, model_loader):
        """
        Initialize DataProcessor
        
        Args:
            model_loader: ModelLoader instance with loaded models
        """
        self.model_loader = model_loader
        self.model = model_loader.get_model()
        self.scaler = model_loader.get_scaler()
        self.trust_scaler = model_loader.get_trust_scaler()
        self.label_encoders = model_loader.get_label_encoders()
        self.feature_names = model_loader.get_feature_names()
    
    def validate_and_prepare(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
        """
        Validate and prepare data for prediction
        
        Args:
            df: Input DataFrame
            
        Returns:
            Tuple of (processed_df, list_of_issues)
        """
        issues = []
        processed_df = df.copy()
        
        # Clean column names
        processed_df.columns = processed_df.columns.str.strip().str.replace("'", "")
        
        # Check if 'class' column exists (ground truth)
        has_labels = 'class' in processed_df.columns
        if has_labels:
            # Store labels separately
            true_labels = processed_df['class'].copy()
            processed_df = processed_df.drop('class', axis=1)
        
        # Validate feature count
        if len(processed_df.columns) < len(self.feature_names):
            issues.append(f"Expected {len(self.feature_names)} features, got {len(processed_df.columns)}")
        
        # Check for missing values
        missing = processed_df.isnull().sum()
        if missing.sum() > 0:
            issues.append(f"Found {missing.sum()} missing values")
            # Fill missing values
            for col in processed_df.columns:
                if processed_df[col].dtype in ['int64', 'float64']:
                    processed_df[col].fillna(processed_df[col].median(), inplace=True)
                else:
                    processed_df[col].fillna(processed_df[col].mode()[0] if len(processed_df[col].mode()) > 0 else 'unknown', inplace=True)
        
        # Ensure correct feature order and add missing features
        missing_features = set(self.feature_names) - set(processed_df.columns)
        if missing_features:
            issues.append(f"Missing features: {missing_features}. Will fill with default values.")
            for feat in missing_features:
                # Add missing features with appropriate default values
                if feat in ['protocol_type', 'service', 'flag']:
                    # Categorical features - use first class from encoder
                    if feat in self.label_encoders:
                        processed_df[feat] = self.label_encoders[feat].classes_[0]
                else:
                    # Numeric features - use 0
                    processed_df[feat] = 0
        
        # Remove extra columns not in training features
        extra_features = set(processed_df.columns) - set(self.feature_names)
        if has_labels and 'true_class' in extra_features:
            extra_features.remove('true_class')
        
        if extra_features:
            issues.append(f"Extra features will be ignored: {extra_features}")
        
        # Reorder columns to match training feature order exactly
        available_features = [f for f in self.feature_names if f in processed_df.columns]
        processed_df = processed_df[available_features + (['true_class'] if has_labels else [])]
        
        # Final check: ensure all features present
        if len(available_features) != len(self.feature_names):
            issues.append(f"Expected {len(self.feature_names)} features, have {len(available_features)}")
        
        # Ensure we have all features in correct order
        processed_df = processed_df[self.feature_names + (['true_class'] if has_labels else [])]
        
        if has_labels:
            # Add labels back
            processed_df['true_class'] = true_labels.values
        
        return processed_df, issues
    
    def encode_categorical_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Encode categorical features using label encoders
        
        Args:
            df: DataFrame with categorical features
            
        Returns:
            DataFrame with encoded features
        """
        df_encoded = df.copy()
        
        for col, encoder in self.label_encoders.items():
            if col in df_encoded.columns:
                # Handle unseen categories
                try:
                    df_encoded[col] = encoder.transform(df_encoded[col])
                except ValueError:
                    # If unseen category, use most frequent category
                    df_encoded[col] = df_encoded[col].apply(
                        lambda x: encoder.transform([x])[0] if x in encoder.classes_ else encoder.transform([encoder.classes_[0]])[0]
                    )
        
        return df_encoded
    
    def predict(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Make predictions on the DataFrame
        
        Args:
            df: Preprocessed DataFrame
            
        Returns:
            DataFrame with predictions and trust scores
        """
        # Store true labels if they exist
        has_true_labels = 'true_class' in df.columns
        if has_true_labels:
            true_labels = df['true_class'].copy()
            df_features = df.drop('true_class', axis=1)
        else:
            df_features = df.copy()
        
        # Encode categorical features
        df_encoded = self.encode_categorical_features(df_features)
        
        # Ensure it's a DataFrame with correct feature names and dtypes
        df_encoded = pd.DataFrame(df_encoded, columns=self.feature_names)
        
        # Convert to numeric (in case encoding left some strings)
        for col in df_encoded.columns:
            df_encoded[col] = pd.to_numeric(df_encoded[col], errors='coerce').fillna(0)
        
        # Get numeric array
        X_numeric = df_encoded[self.feature_names].values
        
        # Check if scaler matches our features
        if self.scaler.n_features_in_ != len(self.feature_names):
            # Scaler mismatch - need to create a new one fitted on this data
            # This is a workaround: we'll use StandardScaler's typical scaling
            print(f"⚠️ Scaler mismatch detected ({self.scaler.n_features_in_} vs {len(self.feature_names)} features)")
            print("Creating temporary scaler based on current data statistics...")
            
            from sklearn.preprocessing import StandardScaler
            temp_scaler = StandardScaler()
            # Fit and transform on the current data
            # This assumes the data distribution is similar to training
            X_scaled = temp_scaler.fit_transform(X_numeric)
        else:
            # Use the saved scaler
            X_scaled = self.scaler.transform(X_numeric)
        
        # Make predictions
        predictions = self.model.predict(X_scaled)
        probabilities = self.model.predict_proba(X_scaled)
        decision_values = self.model.decision_function(X_scaled)
        
        # Calculate trust scores (0-100)
        trust_scores_raw = decision_values.reshape(-1, 1)
        trust_scores = self.trust_scaler.transform(trust_scores_raw).flatten()
        trust_scores = np.clip(trust_scores, 0, 100)
        
        # Determine actions and trust levels
        actions = []
        trust_levels = []
        recommendations = []
        
        for score in trust_scores:
            if score >= 66:
                actions.append('ALLOW')
                trust_levels.append('High')
                recommendations.append('Grant access - Low risk node')
            elif score >= 33:
                actions.append('MONITOR')
                trust_levels.append('Medium')
                recommendations.append('Additional verification required')
            else:
                actions.append('BLOCK')
                trust_levels.append('Low')
                recommendations.append('Deny access - High risk node')
        
        # Create results DataFrame
        results_df = pd.DataFrame({
            'prediction': ['Anomaly' if p == 1 else 'Normal' for p in predictions],
            'trust_score': trust_scores.round(2),
            'trust_level': trust_levels,
            'action': actions,
            'confidence': probabilities.max(axis=1).round(4),
            'recommendation': recommendations
        })
        
        # Add true labels if available
        if has_true_labels:
            results_df['true_class'] = true_labels.values
            results_df['correct'] = (results_df['prediction'] == results_df['true_class'])
        
        return results_df
    
    def get_feature_importance(self) -> pd.DataFrame:
        """
        Get feature importance (if available)
        
        Returns:
            DataFrame with feature names and importance scores
        """
        # For SVM, we can use coefficient magnitudes (if linear kernel)
        # For RBF kernel, feature importance is not directly available
        # Return placeholder
        return pd.DataFrame({
            'feature': self.feature_names,
            'importance': ['N/A (RBF kernel)'] * len(self.feature_names)
        })
    
    def validate_single_row(self, row_dict: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate a single row of data
        
        Args:
            row_dict: Dictionary with feature values
            
        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        issues = []
        
        # Check for required features
        missing_features = set(self.feature_names) - set(row_dict.keys())
        if missing_features:
            issues.append(f"Missing features: {missing_features}")
        
        # Check data types
        for feat in self.feature_names:
            if feat in row_dict:
                value = row_dict[feat]
                if pd.isna(value):
                    issues.append(f"Null value in feature: {feat}")
        
        is_valid = len(issues) == 0
        return is_valid, issues
