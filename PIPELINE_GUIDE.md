# Interactive Prediction Pipeline

## 🎯 Complete User Input → Model → Output Pipeline

Yes! I've created **3 complete pipelines** for you:

---

## 📁 Pipeline Files

### 1. **`prediction_api.py`** - Core API Class
- The base class with prediction logic
- Can be imported into other scripts
- Use this for integration into larger applications

### 2. **`interactive_pipeline.py`** - Full Interactive System ⭐ 
**This is what you asked for!**
- Complete user input → model → output pipeline
- Interactive command-line interface
- Multiple input options (manual, CSV, sample data)
- Beautiful formatted output with trust meter
- Logging support

### 3. **`quick_test.py`** - Quick Testing
- Fast way to test if everything works
- Uses sample data
- No user input required

---

## 🚀 How to Use

### Option 1: Full Interactive Pipeline (Recommended)

```bash
cd deployment
python interactive_pipeline.py
```

**Features:**
- ✅ User inputs data (manual or CSV)
- ✅ Model processes input
- ✅ Prediction displayed with visual trust meter
- ✅ Color-coded decision (🔴 BLOCK / 🟡 MONITOR / 🟢 ALLOW)
- ✅ Save results to log file
- ✅ Test multiple connections in one session

**Example Session:**
```
🔐 NODE AUTHENTICATION SYSTEM - INITIALIZING
✅ All models loaded successfully!

📥 INPUT OPTIONS
1. Enter data manually (simplified - for testing)
2. Load from CSV file
3. Use sample test data

Select option (1/2/3): 3

🔄 PROCESSING INPUT DATA
✅ Data validated and formatted
✅ Features normalized
✅ Prediction complete!

🎯 AUTHENTICATION RESULT
🟢 DECISION: 🟢 ALLOW

📊 Prediction Details:
   • Classification: Normal
   • Trust Score: 78.45/100
   • Trust Level: High Trust
   • Confidence: 95.30%

💡 Recommendation:
   Low risk - GRANT ACCESS

📊 Trust Score Meter:
   0        33        66        100
   |---------|---------|---------|
   LOW      MED      HIGH      MAX
   🟢 [███████████████████████░░░] 78.5
```

---

### Option 2: Quick Test

```bash
cd deployment
python quick_test.py
```

Perfect for verifying the system works!

---

### Option 3: Use in Your Own Code

```python
from prediction_api import NodeAuthenticator

# Initialize
auth = NodeAuthenticator(model_dir='../models')

# Your input data (41 features)
user_input = {
    'duration': 0,
    'protocol_type': 1,
    'service': 20,
    # ... all 41 features
}

# Get prediction
result = auth.predict(user_input)

# Use result
print(f"Decision: {result['action']}")
print(f"Trust Score: {result['trust_score']}/100")
```

---

## 📋 Input Options

### Manual Input
User enters key features manually. Others are set to defaults.

### CSV File Input
Load network connection data from CSV file with all 41 features.

### Sample Data
Two pre-configured samples:
1. Normal network connection (should ALLOW)
2. Suspicious connection (should BLOCK)

---

## 🎨 Pipeline Flow

```
┌─────────────┐
│  User Input │
│  (Data)     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Validate   │
│  & Format   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Scale      │
│  Features   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  SVM Model  │
│  Predict    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Calculate  │
│  Trust Score│
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Determine  │
│  Action     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Display    │
│  Result     │
└─────────────┘
```

---

## 📊 Output Format

The pipeline returns:

- **Action**: 🔴 BLOCK / 🟡 MONITOR / 🟢 ALLOW
- **Classification**: Anomaly or Normal
- **Trust Score**: 0-100 scale
- **Trust Level**: Low / Medium / High
- **Confidence**: Model confidence percentage
- **Recommendation**: What to do with this node
- **Visual Trust Meter**: Easy-to-read bar chart

---

## 💾 Logging

Results can be saved to `prediction_log.json`:

```json
[
  {
    "timestamp": "2025-10-29 14:30:00",
    "input": { ... },
    "result": {
      "action": "ALLOW",
      "trust_score": 78.45,
      ...
    }
  }
]
```

---

## 🔧 Requirements

Make sure you're in the deployment folder with access to:
- `../models/` directory with trained models
- Python packages: `joblib`, `numpy`, `pandas`, `scikit-learn`

---

## 💡 Tips

1. **For Testing**: Use `quick_test.py` first to verify everything works
2. **For Demo**: Use `interactive_pipeline.py` with sample data
3. **For Production**: Import `NodeAuthenticator` class into your application
4. **For Batch Processing**: Load CSV with multiple connections

---

## 🎉 Summary

**YES, I created a complete pipeline!**

✅ User inputs data (manual, CSV, or sample)  
✅ Data goes through validation & preprocessing  
✅ Model makes prediction  
✅ Trust score calculated  
✅ Beautiful output displayed to user  
✅ Results can be logged  

**Try it now:**
```bash
cd deployment
python interactive_pipeline.py
```
