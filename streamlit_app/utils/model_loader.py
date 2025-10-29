"""
Model Loader Module
Handles loading of all trained models and preprocessing components
"""

import joblib
import os
from typing import Dict, Any


class ModelLoader:
    """Load and manage ML models and preprocessing components"""
    
    def __init__(self, model_dir: str = '../models'):
        """
        Initialize ModelLoader
        
        Args:
            model_dir: Directory containing saved model files
        """
        self.model_dir = model_dir
        self.model = None
        self.scaler = None
        self.trust_scaler = None
        self.label_encoders = None
        self.feature_names = None
        
        self._load_all_models()
    
    def _load_all_models(self):
        """Load all model components"""
        try:
            # Load SVM model
            model_path = os.path.join(self.model_dir, 'svm_optimized_model.pkl')
            self.model = joblib.load(model_path)
            print(f"✓ Loaded model from {model_path}")
            
            # Load feature scaler
            scaler_path = os.path.join(self.model_dir, 'feature_scaler.pkl')
            self.scaler = joblib.load(scaler_path)
            print(f"✓ Loaded scaler from {scaler_path}")
            
            # Load trust scaler
            trust_scaler_path = os.path.join(self.model_dir, 'trust_scaler.pkl')
            self.trust_scaler = joblib.load(trust_scaler_path)
            print(f"✓ Loaded trust scaler from {trust_scaler_path}")
            
            # Load label encoders
            encoders_path = os.path.join(self.model_dir, 'label_encoders.pkl')
            self.label_encoders = joblib.load(encoders_path)
            print(f"✓ Loaded label encoders from {encoders_path}")
            
            # Load feature names
            features_path = os.path.join(self.model_dir, 'feature_names.pkl')
            self.feature_names = joblib.load(features_path)
            print(f"✓ Loaded {len(self.feature_names)} feature names")
            
        except Exception as e:
            raise Exception(f"Error loading models: {e}")
    
    def get_model(self):
        """Get the trained SVM model"""
        return self.model
    
    def get_scaler(self):
        """Get the feature scaler"""
        return self.scaler
    
    def get_trust_scaler(self):
        """Get the trust score scaler"""
        return self.trust_scaler
    
    def get_label_encoders(self):
        """Get the label encoders dictionary"""
        return self.label_encoders
    
    def get_feature_names(self):
        """Get the list of feature names in correct order"""
        return self.feature_names
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information"""
        return {
            'model_type': type(self.model).__name__,
            'num_features': len(self.feature_names),
            'feature_names': self.feature_names,
            'categorical_features': list(self.label_encoders.keys()) if self.label_encoders else [],
            'scaler_type': type(self.scaler).__name__,
            'trust_scaler_type': type(self.trust_scaler).__name__
        }
    
    def validate_models(self) -> bool:
        """Validate that all models are loaded correctly"""
        return all([
            self.model is not None,
            self.scaler is not None,
            self.trust_scaler is not None,
            self.label_encoders is not None,
            self.feature_names is not None
        ])
