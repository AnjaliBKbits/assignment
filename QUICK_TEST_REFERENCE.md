# Quick Testing Reference

## Test the Data Preparation Modules

### Option 1: Run Simplified Test Suite (Recommended)
```bash
cd f:\DM4MLPROJECT\DM4ML-Group12\RecoMart-Recommendation-Pipeline
python src/preparation/simple_test.py
```

**What it tests:**
- ✅ Data Cleaner (cleaning CSV files)
- ✅ Data Preprocessor (normalization, encoding, interaction matrix)
- ✅ Exploratory Analyzer (plots and visualizations)
- ✅ End-to-End Pipeline (complete workflow)

**Expected output:** 4/4 test groups passed

---

## Test Individual Components

### Test Data Cleaner Only
```bash
python -c "
from pathlib import Path
import sys
sys.path.insert(0, '.')
from src.preparation.data_cleaner import DataCleaner

cleaner = DataCleaner()
df_clean, _ = cleaner.clean_csv('dataset/ratings.csv', 'ratings', {'rating': 'drop'})
print(f'✓ Cleaned ratings: {len(df_clean)} rows')
"
```

### Test Data Preprocessor Only
```bash
python -c "
from pathlib import Path
import sys, pandas as pd
sys.path.insert(0, '.')
from src.preparation.data_preprocessor import DataPreprocessor

preprocessor = DataPreprocessor()
df = pd.read_csv('dataset/ratings.csv')
matrix = preprocessor.create_interaction_matrix(df, 'userId', 'movieId', 'rating')
print(f'✓ Interaction matrix: {matrix.shape}')
"
```

### Test Exploratory Analyzer Only
```bash
python -c "
from pathlib import Path
import sys, pandas as pd
sys.path.insert(0, '.')
from src.preparation.exploratory_analysis import ExploratoryAnalyzer

analyzer = ExploratoryAnalyzer()
df = pd.read_csv('dataset/ratings.csv').head(2000)
plot = analyzer.plot_distributions(df, 'test')
print(f'✓ Plot generated: {Path(plot).name}')
"
```

---

## Run Jupyter Notebook (Interactive Testing)

```bash
jupyter notebook notebooks/01_Data_Preparation_EDA.ipynb
```

This runs all 10 sections:
1. Import libraries
2. Load and inspect data
3. Handle missing values
4. Encode categorical
5. Normalize numerical
6. Interaction distribution analysis
7. Item popularity analysis
8. Sparsity patterns
9. Summary visualizations
10. Export prepared data

---

## Verify Output Files

### Check all processed data
```powershell
Get-ChildItem data/processed/ -File | Select-Object Name, @{Name="Size(KB)";Expression={"{0:N2}" -f ($_.Length/1KB)}}
```

### Check all plots
```powershell
Get-ChildItem data/plots/ -Filter "*.png" | Select-Object Name, @{Name="Size(KB)";Expression={"{0:N2}" -f ($_.Length/1KB)}}
```

### Check test plots
```powershell
Get-ChildItem data/test_plots/ -Filter "*.png" | Measure-Object -Property Length -Sum | Select-Object Count, @{Name="Total Size(MB)";Expression={"{0:N2}" -f ($_.Sum/1MB)}}
```

---

## Test Results Summary

```
✅ Data Cleaner Tests (4/4 PASSED)
  - ratings.csv: 100,836 rows, no nulls
  - movies.csv: 9,742 rows
  - tags.csv: 3,683 rows
  - links.csv: 9,734 rows (8 removed)

✅ Data Preprocessor Tests (4/4 PASSED)
  - MinMax Normalization: values in [0, 1]
  - Standard Normalization: mean ≈ 0, std ≈ 1
  - Label Encoding: categorical → numeric
  - Interaction Matrix: 610 users × 9,724 items, 98.30% sparse

✅ Exploratory Analyzer Tests (4/4 PASSED)
  - Distribution plots generated
  - Heatmaps generated
  - Categorical plots generated
  - Sparsity plots generated

✅ End-to-End Pipeline Test (PASSED)
  - Full workflow: Clean → Preprocess → Analyze
  - Data integrity maintained throughout
  - All outputs generated successfully
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Module not found" | Ensure working directory is project root |
| Plot not displaying | Add `plt.show()` or use `%matplotlib inline` in Jupyter |
| Kernel timeout | Reduce data size or restart kernel |
| Memory error | Use sampling: `df.sample(n=10000)` |
| Unicode error in console | Add encoding: `PYTHONIOENCODING=utf-8` |

---

## Key Metrics

### Data Quality
- **Missing Values**: Handled (drop strategy)
- **Duplicates**: Removed (8 from links)
- **Data Types**: Fixed and normalized
- **Completeness**: 100% (post-cleaning)

### Dataset Statistics
| Metric | Value |
|--------|-------|
| Users | 610 |
| Items | 9,742 |
| Interactions | 100,836 |
| Sparsity | 98.30% |
| Avg Rating | 3.54 |

### Pipeline Performance
- **Execution Time**: < 2 minutes
- **Memory Usage**: ~500 MB
- **Output Files**: 11+ CSVs + 5+ plots
- **Report Size**: ~25 KB

---

**Last Updated:** 2026-07-18  
**Status:** ✅ All Tests Passing  
**Ready for:** Feature Engineering & Modeling
