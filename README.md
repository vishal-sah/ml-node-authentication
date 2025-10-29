# ML-Based Trust and Reputation System for Node Authentication

A machine learning system for network intrusion detection using Support Vector Machine (SVM) to classify network connections as normal or anomalous, with an adaptive trust scoring mechanism.

## Dataset

**NSL-KDD Network Intrusion Detection Dataset**
- 22,544 training samples
- 41 features including protocol type, service, flags, and network statistics
- Binary classification: Normal vs Anomaly

## Model Performance

| Metric | Score |
|--------|-------|
| Accuracy | 96.91% |
| Precision | 98.42% |
| Recall | 94.34% |
| F1-Score | 96.34% |
| ROC-AUC | 99.49% |

## ML Pipeline

1. **Data Preprocessing**
   - Label encoding for categorical features (protocol_type, service, flag)
   - StandardScaler normalization for numerical features
   - Train-test split (70-30) with stratification

2. **Model Training**
   - Algorithm: Support Vector Machine (SVM)
   - Kernel: RBF (Radial Basis Function)
   - Hyperparameters: C=10, gamma='scale'
   - Cross-validation: 5-fold stratified

3. **Trust Scoring**
   - MinMaxScaler to convert predictions to 0-100 trust score
   - Adaptive thresholds for action classification

## Trust Score System

| Range | Action | Description |
|-------|--------|-------------|
| 0-33 | BLOCK | High risk - Deny access |
| 33-66 | MONITOR | Medium risk - Additional verification required |
| 66-100 | ALLOW | Low risk - Grant access |

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Streamlit Web Application

Launch the interactive web interface:

```bash
cd streamlit_app
streamlit run app.py
```

The web application provides:
- CSV file upload for batch predictions
- Interactive visualizations (trust score distribution, confidence levels, action breakdown)
- Real-time prediction results with detailed metrics
- Downloadable results in CSV format

### Python API

```python
import pandas as pd
from streamlit_app.utils.model_loader import ModelLoader
from streamlit_app.utils.data_processor import DataProcessor

# Load models
loader = ModelLoader('../models')
models = loader.load_all_models()

# Initialize processor
processor = DataProcessor(
    model=models['model'],
    scaler=models['scaler'],
    trust_scaler=models['trust_scaler'],
    label_encoders=models['label_encoders'],
    feature_names=models['feature_names']
)

# Load and predict
df = pd.read_csv('test_data.csv')
results = processor.predict(df)

print(results[['prediction', 'confidence', 'trust_score', 'action']])
```

### Test Data Generation

Generate sample test datasets:

```bash
cd streamlit_app
python generate_test_data.py
```

Creates 20 varied CSV test files in the `test/` directory with different attack patterns.

## Project Structure

```
ml-node-authentication/
├── data.csv                      # Training dataset
├── project.ipynb                 # Complete ML pipeline and analysis
├── requirements.txt              # Python dependencies
├── rebuild_scaler.py             # Utility to rebuild feature scaler
├── models/                       # Trained models and encoders
│   ├── svm_optimized_model.pkl
│   ├── feature_scaler.pkl
│   ├── trust_scaler.pkl
│   ├── label_encoders.pkl
│   └── feature_names.pkl
└── streamlit_app/                # Web application
    ├── app.py                    # Main Streamlit application
    ├── requirements.txt          # Streamlit dependencies
    ├── utils/
    │   ├── model_loader.py       # Model loading utilities
    │   ├── data_processor.py     # Data preprocessing and prediction
    │   └── visualizer.py         # Visualization components
    └── test/                     # Test datasets
        └── test1.csv ... test20.csv
```

## Requirements

- Python 3.11+
- pandas
- numpy
- scikit-learn
- joblib
- streamlit
- plotly
- matplotlib
- seaborn

## License

This project uses the NSL-KDD dataset, which is publicly available for research purposes.
