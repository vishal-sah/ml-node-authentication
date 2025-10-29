# 📁 Test Data Files - Description

This folder contains **20 test CSV files** with varied network connection data for testing the Node Authentication Trust System.

## 📊 File Overview

### Files 1-5: Normal Traffic Variations
| File | Samples | Description |
|------|---------|-------------|
| `test1.csv` | 10 | Pure normal traffic |
| `test2.csv` | 15 | Pure normal traffic (larger set) |
| `test3.csv` | 12 | Pure normal traffic |
| `test4.csv` | 13 | **90% normal, 10% attacks** |
| `test5.csv` | 14 | **80% normal, 20% attacks** |

**Expected Results:** High trust scores (66-100), mostly ALLOW actions

---

### Files 6-10: DoS Attacks & Mixed Scenarios
| File | Samples | Description |
|------|---------|-------------|
| `test6.csv` | 10 | Pure DoS (Denial of Service) attacks |
| `test7.csv` | 15 | Pure DoS attacks (larger set) |
| `test8.csv` | 12 | **Balanced: 50% normal, 50% attacks** |
| `test9.csv` | 11 | **Attack-heavy: 30% normal, 70% attacks** |
| `test10.csv` | 13 | **Mostly attacks: 10% normal, 90% attacks** |

**Expected Results:** Low trust scores (0-33), mostly BLOCK actions for DoS

---

### Files 11-15: Specific Attack Types
| File | Samples | Description |
|------|---------|-------------|
| `test11.csv` | 10 | Pure **Probe/Scan** attacks (port scanning, reconnaissance) |
| `test12.csv` | 14 | Pure **Probe/Scan** attacks (larger) |
| `test13.csv` | 12 | Pure **R2L** (Remote to Local) attacks (unauthorized access) |
| `test14.csv` | 15 | Pure **R2L** attacks (larger) |
| `test15.csv` | 11 | Pure **U2R** (User to Root) attacks (privilege escalation) |

**Expected Results:** Low trust scores, BLOCK or MONITOR actions

---

### Files 16-20: Varied Mixed Traffic
| File | Samples | Description |
|------|---------|-------------|
| `test16.csv` | 13 | **70% normal, 30% attacks** |
| `test17.csv` | 14 | **40% normal, 60% attacks** |
| `test18.csv` | 10 | **60% normal, 40% attacks** |
| `test19.csv` | 15 | **85% normal, 15% attacks** |
| `test20.csv` | 12 | **20% normal, 80% attacks** |

**Expected Results:** Mixed trust scores, variety of actions

---

## 🎯 Attack Type Characteristics

### 1. **DoS (Denial of Service)** - Files 6-7, 10
- **Characteristics:**
  - Very high connection counts (50-500)
  - High error rates (serror_rate > 0.8)
  - Same service rate near 1.0
  - Duration typically 0
  - Dst_host_count = 255 (max)

### 2. **Probe/Scan** - Files 11-12
- **Characteristics:**
  - Low duration (0)
  - High error rates
  - High diff_srv_rate (0.7-1.0)
  - Low same_srv_rate (0-0.3)
  - Scanning multiple hosts/services

### 3. **R2L (Remote to Local)** - Files 13-14
- **Characteristics:**
  - Failed login attempts
  - Hot indicators
  - Guest login attempts
  - Compromised indicators
  - Targeting authentication services (ftp, telnet, ssh)

### 4. **U2R (User to Root)** - File 15
- **Characteristics:**
  - Root shell access
  - High num_compromised
  - Su_attempted indicators
  - Num_root indicators
  - File creation/shell activities

### 5. **Normal Traffic** - Files 1-5, 19
- **Characteristics:**
  - Logged_in = 1
  - Low/zero error rates
  - Reasonable connection counts
  - Standard protocols (tcp/udp)
  - Common services (http, ftp, smtp)

---

## 🧪 Testing Workflow

### Quick Test (Single File):
```powershell
# In Streamlit app
1. Upload test1.csv (normal traffic)
2. View predictions - should be mostly "Normal" with high trust scores
3. Upload test6.csv (DoS attacks)
4. View predictions - should be mostly "Anomaly" with low trust scores
```

### Comprehensive Test (All Files):
```powershell
# Test each file and compare results
for i in {1..20}:
    - Upload test{i}.csv
    - Check prediction accuracy
    - Verify trust score distribution
    - Download results
```

### Batch Analysis:
- Upload multiple files to compare
- Analyze trust score trends
- Identify detection patterns
- Validate model performance across attack types

---

## 📈 Expected Performance

| Traffic Type | Expected Accuracy | Trust Score Range | Primary Action |
|--------------|-------------------|-------------------|----------------|
| Pure Normal | >95% | 66-100 (High) | ALLOW |
| Pure DoS | >90% | 0-33 (Low) | BLOCK |
| Pure Probe | >85% | 0-33 (Low) | BLOCK |
| Pure R2L | >80% | 0-66 (Low-Med) | BLOCK/MONITOR |
| Pure U2R | >75% | 0-66 (Low-Med) | BLOCK/MONITOR |
| Mixed 80/20 | >90% | Varied | Mixed |
| Mixed 50/50 | >85% | Varied | Mixed |

---

## 📝 Data Format

All files contain **41 features**:

### Categorical (3):
- `protocol_type`: tcp, udp, icmp
- `service`: http, ftp, smtp, telnet, ssh, pop3, domain, finger, private, eco_i
- `flag`: SF, S0, REJ, RSTR, RSTO, SH, S1, S2, RSTOS0, S3, OTH

### Numeric (38):
- Connection features (duration, src_bytes, dst_bytes)
- Content features (hot, logged_in, num_failed_logins, etc.)
- Traffic features (count, srv_count, error rates)
- Host-based features (dst_host_count, dst_host_srv_count, etc.)

---

## 🚀 Usage in Streamlit App

1. **Start Streamlit:**
   ```powershell
   streamlit run app.py
   ```

2. **Navigate to "Upload & Predict"**

3. **Select test file:**
   - Browse to `test/` folder
   - Choose any test1.csv through test20.csv

4. **Generate predictions and analyze:**
   - View results table
   - Explore visualizations
   - Check detailed analysis
   - Download results

---

## 🔍 Validation Tips

- **Test1-5:** Should show high trust (ALLOW)
- **Test6-7:** Should detect DoS (BLOCK)
- **Test11-15:** Should catch specific attacks
- **Test8,16-18:** Should show mixed results based on ratios
- **Test10,20:** Should be attack-dominant (mostly BLOCK)

---

## ✅ Quality Assurance

All test files:
- ✓ Contain 10-15 samples each
- ✓ Have all 41 required features
- ✓ Use realistic value ranges
- ✓ Follow NSL-KDD dataset patterns
- ✓ Include varied attack scenarios
- ✓ Are ready for immediate testing

---

**Generated:** October 29, 2025  
**Total Files:** 20  
**Total Samples:** 245 (across all files)  
**Purpose:** Comprehensive testing of ML-based Node Authentication System
