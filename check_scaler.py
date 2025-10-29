import joblib

scaler = joblib.load('models/feature_scaler.pkl')
print('Scaler expects', scaler.n_features_in_, 'features')
print('Has feature names:', hasattr(scaler, 'feature_names_in_'))
if hasattr(scaler, 'feature_names_in_'):
    print('\nFeature names used during fit:')
    for i, name in enumerate(scaler.feature_names_in_, 1):
        print(f'{i}. {name}')
