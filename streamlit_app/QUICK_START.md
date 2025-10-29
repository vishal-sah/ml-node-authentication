# 🚀 Quick Start Guide for Streamlit UI

## Installation & Setup

1. **Navigate to streamlit app directory:**
```powershell
cd c:\Users\vs681\Downloads\NSL_KDD\streamlit_app
```

2. **Install Streamlit and dependencies:**
```powershell
pip install -r requirements.txt
```

3. **Run the application:**
```powershell
streamlit run app.py
```

4. **Access the web interface:**
- Automatically opens in browser at: `http://localhost:8501`
- Or manually navigate to that URL

## 📁 Prepare Your CSV File

### Option 1: Use Sample Template
Use the provided `sample_data_template.csv` as a reference

### Option 2: Use Your Own Data
Ensure your CSV has these **41 features**:

**Numeric (38 features):**
- duration, src_bytes, dst_bytes, land, wrong_fragment, urgent
- hot, num_failed_logins, logged_in, num_compromised, root_shell
- su_attempted, num_root, num_file_creations, num_shells
- num_access_files, num_outbound_cmds, is_host_login, is_guest_login
- count, srv_count, serror_rate, srv_serror_rate, rerror_rate
- srv_rerror_rate, same_srv_rate, diff_srv_rate, srv_diff_host_rate
- dst_host_count, dst_host_srv_count, dst_host_same_srv_rate
- dst_host_diff_srv_rate, dst_host_same_src_port_rate
- dst_host_srv_diff_host_rate, dst_host_serror_rate
- dst_host_srv_serror_rate, dst_host_rerror_rate, dst_host_srv_rerror_rate

**Categorical (3 features):**
- protocol_type: tcp, udp, icmp
- service: http, ftp, smtp, telnet, etc.
- flag: SF, S0, REJ, RSTO, etc.

## 🎯 Using the Web Interface

### Step-by-Step:

1. **Home Page**
   - Read system overview
   - Check model performance metrics

2. **Upload & Predict**
   - Click "📤 Upload & Predict" in sidebar
   - Click "Browse files" or drag-and-drop CSV
   - Review data preview (first 10 rows)
   - Check for any validation warnings
   - Click "🎯 Generate Predictions" button
   - Wait for processing (progress indicator shown)

3. **View Results**
   - **Results Table Tab**: See all predictions with trust scores
   - **Visualizations Tab**: Interactive charts
     * Action distribution (pie chart)
     * Trust score distribution (histogram)
     * Trust scores by prediction type (box plot)
   - **Detailed Analysis Tab**: High-risk detections

4. **Download Results**
   - Click "📥 Download Results CSV" button
   - File saved with timestamp: `predictions_YYYYMMDD_HHMMSS.csv`

## 📊 Understanding Results

### Columns in Results:
- **prediction**: Normal or Anomaly
- **trust_score**: 0-100 score
- **trust_level**: Low, Medium, or High
- **action**: ALLOW, MONITOR, or BLOCK
- **confidence**: Model confidence (0-1)
- **recommendation**: Security action suggestion

### Security Actions:
- 🛑 **BLOCK** (0-33): High risk - Deny access
- ⚠️ **MONITOR** (33-66): Medium risk - Additional verification
- ✅ **ALLOW** (66-100): Low risk - Grant access

## 🔧 Troubleshooting

### "Error loading models"
```powershell
# Verify model files exist
ls ..\models\*.pkl
```
Should show 5 files:
- svm_optimized_model.pkl
- feature_scaler.pkl
- trust_scaler.pkl
- label_encoders.pkl
- feature_names.pkl

### "Expected 41 features, got X"
- Check your CSV has all 41 columns
- Verify column names match exactly
- Use `sample_data_template.csv` as reference

### "Port already in use"
```powershell
streamlit run app.py --server.port 8502
```

### Missing dependencies
```powershell
pip install streamlit plotly pandas numpy scikit-learn joblib
```

## 💡 Tips

1. **Large Files**: App handles multiple rows efficiently
2. **Validation**: System automatically handles missing values
3. **Sorting**: Click column headers in results table to sort
4. **Filtering**: Use browser's Find (Ctrl+F) in results
5. **Mobile**: Responsive design works on tablets/phones

## 🎨 Features

✅ **Completed:**
- CSV file upload
- Batch predictions
- Trust score calculation
- Interactive visualizations
- Downloadable results
- Data validation
- Error handling

🚧 **Coming Soon:**
- Multiple file comparison
- Historical trend analysis
- Custom threshold settings
- PDF report generation

## 📞 Need Help?

1. Check `README.md` for detailed documentation
2. Review terminal output for error messages
3. Verify all model files are present
4. Ensure CSV format matches requirements

---

**Ready to test?**
```powershell
streamlit run app.py
```

Enjoy testing your ML model! 🚀
