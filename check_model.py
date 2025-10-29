import joblib

model = joblib.load('models/svm_optimized_model.pkl')
print('Model expects', model.n_features_in_, 'features')
print('Has feature names:', hasattr(model, 'feature_names_in_'))
if hasattr(model, 'feature_names_in_'):
    print('\nFeature names used during fit:')
    for i, name in enumerate(model.feature_names_in_, 1):
        print(f'{i}. {name}')
