# 🔐 Node Authentication Trust System - Streamlit Web UI

A web-based interface for testing the ML-based node authentication system with CSV file uploads.

## 🚀 Features

- **CSV File Upload**: Upload network connection data for batch predictions
- **Real-time Predictions**: Fast SVM-based classification
- **Trust Scoring**: 0-100 scale with security recommendations
- **Interactive Visualizations**: Charts, graphs, and distribution plots
- **Downloadable Results**: Export predictions as CSV
- **Batch Analysis**: Process multiple nodes simultaneously

## 📋 Requirements

- Python 3.11+
- Trained model files in `../models/` directory
- Dependencies listed in `requirements.txt`

## 🛠️ Installation

1. **Navigate to the streamlit_app directory:**
```powershell
cd streamlit_app
```

2. **Install dependencies:**
```powershell
pip install -r requirements.txt
```

3. **Verify model files exist:**
```
../models/
  ├── svm_optimized_model.pkl
  ├── feature_scaler.pkl
  ├── trust_scaler.pkl
  ├── label_encoders.pkl
  └── feature_names.pkl
```

## 🏃 Running the Application

**Start the Streamlit server:**
```powershell
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## 📊 Using the Application

### 1. Home Page
- Overview of system features
- Model performance metrics
- Quick start guide

### 2. Upload & Predict
- Click "Upload & Predict" in sidebar
- Upload a CSV file with 41 network connection features
- View data preview and validation results
- Click "Generate Predictions" button
- Explore results in multiple tabs:
  - **Results Table**: Full prediction details
  - **Visualizations**: Charts and graphs
  - **Detailed Analysis**: High-risk detections
- Download results as CSV

### 3. Batch Analysis
- Compare multiple datasets
- Trend analysis (coming soon)

### 4. About
- System information
- Model specifications
- Feature requirements

## 📁 CSV File Format

Your CSV should contain **41 features** in the following order:

### Numeric Features (38):
- `duration`, `src_bytes`, `dst_bytes`
- `land`, `wrong_fragment`, `urgent`
- `hot`, `num_failed_logins`, `logged_in`
- `num_compromised`, `root_shell`, `su_attempted`
- `num_root`, `num_file_creations`, `num_shells`
- `num_access_files`, `num_outbound_cmds`
- `is_host_login`, `is_guest_login`
- `count`, `srv_count`
- `serror_rate`, `srv_serror_rate`
- `rerror_rate`, `srv_rerror_rate`
- `same_srv_rate`, `diff_srv_rate`
- `srv_diff_host_rate`
- `dst_host_count`, `dst_host_srv_count`
- `dst_host_same_srv_rate`, `dst_host_diff_srv_rate`
- `dst_host_same_src_port_rate`, `dst_host_srv_diff_host_rate`
- `dst_host_serror_rate`, `dst_host_srv_serror_rate`
- `dst_host_rerror_rate`, `dst_host_srv_rerror_rate`

### Categorical Features (3):
- `protocol_type` (tcp, udp, icmp)
- `service` (http, ftp, smtp, etc.)
- `flag` (SF, S0, REJ, etc.)

### Optional:
- `class` (Normal/Anomaly) - for validation if ground truth available

## 🔒 Trust Score Levels

- **High Trust (66-100)**: ✅ **ALLOW** - Grant access, low risk
- **Medium Trust (33-66)**: ⚠️ **MONITOR** - Additional verification required
- **Low Trust (0-33)**: 🛑 **BLOCK** - Deny access, high risk

## 📊 Model Performance

- **Algorithm**: Support Vector Machine (RBF Kernel)
- **Accuracy**: 96.91%
- **Precision**: 98.42%
- **Recall**: 94.34%
- **F1-Score**: 96.34%
- **ROC-AUC**: 99.49%

## 🏗️ Project Structure

```
streamlit_app/
├── app.py                    # Main Streamlit application
├── utils/                    # Utility modules
│   ├── __init__.py
│   ├── model_loader.py       # Model loading
│   ├── data_processor.py     # Data preprocessing & prediction
│   └── visualizer.py         # Visualization components
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## 🔧 Troubleshooting

### Models not loading
- Ensure model files are in `../models/` directory
- Check file permissions
- Verify all 5 .pkl files exist

### CSV upload errors
- Check CSV format matches required features
- Ensure no missing values in critical columns
- Verify categorical values are valid

### Port already in use
```powershell
streamlit run app.py --server.port 8502
```

### Dependencies issues
```powershell
pip install --upgrade -r requirements.txt
```

## 📞 Support

For issues or questions:
1. Check this README
2. Review error messages in the app
3. Verify model files are present
4. Check terminal output for debugging info

## 🎯 Next Steps

- Test with your own CSV data
- Explore different visualizations
- Download and analyze results
- Compare predictions across multiple datasets

---

**Version**: 1.0.0  
**Framework**: Streamlit  
**ML Model**: SVM (scikit-learn)
