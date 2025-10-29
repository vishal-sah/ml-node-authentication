"""
Test with actual generated test files to verify differentiation
"""

import pandas as pd
import sys
import os

# Add path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.model_loader import ModelLoader
from utils.data_processor import DataProcessor

def test_file(filename, description):
    """Test a specific file"""
    print(f"\n{'='*70}")
    print(f"Testing: {filename}")
    print(f"Description: {description}")
    print('='*70)
    
    # Load data
    df = pd.read_csv(f'test/{filename}')
    print(f"Loaded {len(df)} samples")
    
    # Process
    processor = DataProcessor(ModelLoader('../models'))
    processed_df, issues = processor.validate_and_prepare(df)
    
    if issues:
        print(f"⚠️ Issues: {issues[0]}")
    
    # Predict
    results_df = processor.predict(processed_df)
    
    # Show statistics
    print(f"\n📊 Results Summary:")
    print(f"  Trust Score Range: {results_df['trust_score'].min():.2f} - {results_df['trust_score'].max():.2f}")
    print(f"  Trust Score Mean:  {results_df['trust_score'].mean():.2f}")
    print(f"  Confidence Range:  {results_df['confidence'].min():.4f} - {results_df['confidence'].max():.4f}")
    print(f"  Confidence Mean:   {results_df['confidence'].mean():.4f}")
    
    print(f"\n🎯 Action Distribution:")
    for action in ['ALLOW', 'MONITOR', 'BLOCK']:
        count = len(results_df[results_df['action'] == action])
        pct = count / len(results_df) * 100
        print(f"  {action}: {count} ({pct:.1f}%)")
    
    print(f"\n🔍 Prediction Distribution:")
    for pred in results_df['prediction'].unique():
        count = len(results_df[results_df['prediction'] == pred])
        pct = count / len(results_df) * 100
        print(f"  {pred}: {count} ({pct:.1f}%)")
    
    # Show sample results
    print(f"\n📋 Sample Results (first 5):")
    print(results_df[['prediction', 'trust_score', 'confidence', 'action']].head().to_string(index=False))
    
    return results_df

# Test different file types
print("="*70)
print("COMPREHENSIVE TEST WITH VARIED DATA")
print("="*70)

test_files = [
    ('test1.csv', 'Pure Normal Traffic'),
    ('test6.csv', 'Pure DoS Attacks'),
    ('test11.csv', 'Pure Probe/Scan Attacks'),
    ('test13.csv', 'Pure R2L Attacks'),
    ('test8.csv', 'Mixed 50/50'),
]

results = {}
for filename, description in test_files:
    try:
        results[filename] = test_file(filename, description)
    except Exception as e:
        print(f"\n❌ Error testing {filename}: {e}")
        import traceback
        traceback.print_exc()

print("\n" + "="*70)
print("COMPARISON SUMMARY")
print("="*70)

for filename, description in test_files:
    if filename in results:
        df = results[filename]
        print(f"\n{filename} ({description}):")
        print(f"  Avg Trust: {df['trust_score'].mean():.2f}, Avg Conf: {df['confidence'].mean():.4f}")
        actions = df['action'].value_counts().to_dict()
        print(f"  Actions: ALLOW={actions.get('ALLOW',0)}, MONITOR={actions.get('MONITOR',0)}, BLOCK={actions.get('BLOCK',0)}")

print("\n✅ Comprehensive test complete!")
