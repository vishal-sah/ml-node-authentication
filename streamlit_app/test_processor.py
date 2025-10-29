"""
Quick test script to verify data processing fixes
"""

import pandas as pd
import sys
import os

# Add path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.model_loader import ModelLoader
from utils.data_processor import DataProcessor

def test_sample_data():
    """Test with sample data"""
    print("=" * 60)
    print("Testing Data Processor with Sample Data")
    print("=" * 60)
    
    # Load models
    print("\n1. Loading models...")
    model_loader = ModelLoader('../models')
    print("✓ Models loaded successfully")
    
    # Get feature names
    feature_names = model_loader.get_feature_names()
    print(f"✓ Expected {len(feature_names)} features")
    
    # Create sample data
    print("\n2. Creating sample data...")
    sample_data = {
        'duration': [0, 0, 0],
        'protocol_type': ['tcp', 'tcp', 'udp'],
        'service': ['http', 'ftp', 'smtp'],
        'flag': ['SF', 'S0', 'SF'],
        'src_bytes': [181, 239, 235],
        'dst_bytes': [5450, 486, 1337],
        'land': [0, 0, 0],
        'wrong_fragment': [0, 0, 0],
        'urgent': [0, 0, 0],
        'hot': [0, 0, 0],
        'num_failed_logins': [0, 0, 0],
        'logged_in': [1, 1, 1],
        'num_compromised': [0, 0, 0],
        'root_shell': [0, 0, 0],
        'su_attempted': [0, 0, 0],
        'num_root': [0, 0, 0],
        'num_file_creations': [0, 0, 0],
        'num_shells': [0, 0, 0],
        'num_access_files': [0, 0, 0],
        'num_outbound_cmds': [0, 0, 0],
        'is_host_login': [0, 0, 0],
        'is_guest_login': [0, 0, 0],
        'count': [8, 8, 8],
        'srv_count': [8, 8, 8],
        'serror_rate': [0.0, 0.0, 0.0],
        'srv_serror_rate': [0.0, 0.0, 0.0],
        'rerror_rate': [0.0, 0.0, 0.0],
        'srv_rerror_rate': [0.0, 0.0, 0.0],
        'same_srv_rate': [1.0, 1.0, 1.0],
        'diff_srv_rate': [0.0, 0.0, 0.0],
        'srv_diff_host_rate': [0.0, 0.0, 0.0],
        'dst_host_count': [9, 19, 29],
        'dst_host_srv_count': [9, 19, 29],
        'dst_host_same_srv_rate': [1.0, 1.0, 1.0],
        'dst_host_diff_srv_rate': [0.0, 0.0, 0.0],
        'dst_host_same_src_port_rate': [0.11, 0.05, 0.03],
        'dst_host_srv_diff_host_rate': [0.0, 0.0, 0.0],
        'dst_host_serror_rate': [0.0, 0.0, 0.0],
        'dst_host_srv_serror_rate': [0.0, 0.0, 0.0],
        'dst_host_rerror_rate': [0.0, 0.0, 0.0],
        'dst_host_srv_rerror_rate': [0.0, 0.0, 0.0]
    }
    
    df = pd.DataFrame(sample_data)
    print(f"✓ Created sample DataFrame with {len(df)} rows and {len(df.columns)} columns")
    
    # Process data
    print("\n3. Validating and preparing data...")
    processor = DataProcessor(model_loader)
    processed_df, issues = processor.validate_and_prepare(df)
    
    if issues:
        print(f"⚠ Found {len(issues)} issues:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("✓ No validation issues")
    
    print(f"✓ Processed DataFrame shape: {processed_df.shape}")
    
    # Make predictions
    print("\n4. Making predictions...")
    try:
        results_df = processor.predict(processed_df)
        print("✓ Predictions successful!")
        
        print("\n5. Results:")
        print("-" * 60)
        print(results_df[['prediction', 'trust_score', 'trust_level', 'action', 'confidence']])
        print("-" * 60)
        
        print("\n✅ All tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Prediction failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_sample_data()
    sys.exit(0 if success else 1)
