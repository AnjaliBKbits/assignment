# Data Preparation and EDA - Implementation Guide

## Overview

A comprehensive data preparation and exploratory data analysis (EDA) framework has been implemented to clean, preprocess, and analyze recommendation system datasets before transformation and modeling.

## Components

### 1. **DataCleaner** (`src/preparation/data_cleaner.py`)

Handles data cleaning operations:

#### Features
- **Missing Value Handling**: Multiple strategies (drop, mean, median, zero, forward-fill, mode)
- **Duplicate Detection & Removal**: Identifies and removes duplicate rows
- **Data Type Fixing**: Infers and optimizes data types
- **Cleaning Reports**: Detailed documentation of all operations

#### Usage Example

```python
from src.preparation.data_cleaner import DataCleaner
from pathlib import Path

cleaner = DataCleaner()

# Define cleaning strategy
missing_strategy = {
    "rating": "drop",      # Drop rows with missing rating
    "timestamp": "drop",   # Drop rows with missing timestamp
}

# Clean dataset
df_clean, report = cleaner.clean_csv(
    file_path=Path("dataset/ratings.csv"),
    dataset_name="ratings",
    missing_strategy=missing_strategy
)

# Get cleaning summary
summary = cleaner.get_summary()
```

### 2. **DataPreprocessor** (`src/preparation/data_preprocessor.py`)

Performs preprocessing operations:

#### Features
- **Categorical Encoding**: Label encoding for categorical variables
- **One-Hot Encoding**: Creates dummy variables (with multicollinearity handling)
- **Numerical Normalization**: MinMax and Standard scaling
- **Interaction Matrix Creation**: Pivot ratings into user-item matrices
- **Preprocessing Reports**: Detailed operation documentation

#### Usage Example

```python
from src.preparation.data_preprocessor import DataPreprocessor

preprocessor = DataPreprocessor()

# Preprocess with encoding and normalization
df_processed, report = preprocessor.preprocess_dataset(
    df=df_clean,
    dataset_name="ratings",
    categorical_columns=[],
    numerical_columns=["userId", "movieId", "rating", "timestamp"],
    normalize_method="minmax"  # or "standard"
)

# Create interaction matrix
interaction_matrix = preprocessor.create_interaction_matrix(
    df_ratings=df_clean,
    user_col="userId",
    item_col="movieId",
    rating_col="rating"
)
```

### 3. **ExploratoryAnalyzer** (`src/preparation/exploratory_analysis.py`)

Generates comprehensive exploratory analysis and visualizations:

#### Features
- **Distribution Analysis**: Statistical analysis of features
- **Correlation Analysis**: Identifies feature relationships
- **Visualization Generation**: 
  - Histograms and KDE plots
  - Correlation heatmaps
  - Categorical bar charts
  - Sparsity analysis plots
- **Sparsity Metrics**: Matrix sparsity, density, interaction patterns

#### Usage Example

```python
from src.preparation.exploratory_analysis import ExploratoryAnalyzer

analyzer = ExploratoryAnalyzer(output_dir=Path("data/plots"))

# Analyze dataset
analysis = analyzer.analyze_dataset(df_ratings_clean, "ratings")

# Generate visualizations
analyzer.plot_distributions(df_ratings_clean, "ratings", save=True)
analyzer.plot_heatmap(df_ratings_clean, "ratings", save=True)
analyzer.plot_categorical_distributions(df_movies_clean, "movies", save=True)
analyzer.plot_sparsity(interaction_matrix, "interactions", save=True)
```

## Jupyter Notebook Workflow

### File Location
`notebooks/01_Data_Preparation_EDA.ipynb`

### Sections Covered

1. **Import Libraries** - All necessary dependencies
2. **Load Data** - Load and inspect raw datasets
3. **Handle Missing Values** - Clean missing interactions
4. **Encode Categorical** - Process genres and tags
5. **Normalize Numerical** - Scale ratings and timestamps
6. **Interaction Distributions** - Analyze rating patterns
7. **Item Popularity** - Examine top items
8. **Sparsity Patterns** - Matrix density analysis
9. **Summary Visualizations** - Comprehensive plots
10. **Export Data** - Save prepared datasets

### Key Visualizations Generated

1. **Distribution Plots**
   - Rating distributions (histogram + box plot)
   - User interaction counts
   - Item popularity distribution
   - Top 20 most active users
   - Top 20 most popular items

2. **Heatmaps**
   - Correlation matrix heatmap
   - Feature relationship visualization

3. **Sparsity Analysis**
   - Matrix sparsity pie chart
   - User interaction distribution
   - Item popularity distribution
   - Interaction statistics

4. **Summary Visualization**
   - 8-panel comprehensive summary
   - All key metrics in one figure
   - Statistical summaries

## Data Preparation Results

### Dataset Statistics

| Metric | Value |
|--------|-------|
| Total Users | 610 |
| Total Items | 9,742 |
| Total Interactions | 100,836 |
| Matrix Sparsity | 98.30% |
| Matrix Density | 1.70% |

### Rating Distribution

| Statistic | Value |
|-----------|-------|
| Mean | 3.54 |
| Median | 3.50 |
| Std Dev | 1.04 |
| Min | 0.5 |
| Max | 5.0 |

### User Behavior

- **Average interactions/user**: 165.30
- **Median interactions/user**: 71.00
- **Most active user**: 2,391 ratings
- **Least active user**: 20 ratings

### Item Popularity

- **Average ratings/item**: 10.36
- **Median ratings/item**: 4.00
- **Most popular item**: 329 ratings
- **Least popular item**: 1 rating

### Sparsity Insights

1. **Matrix Characteristics**
   - 98.30% sparse (mostly 0s)
   - Long-tail distribution (few items with many ratings)
   - Concentrated user-item interactions

2. **Cold-Start Problem**
   - 50% of items have ≤ 4 ratings
   - New items will have limited interaction data
   - Requires content-based features

3. **User Diversity**
   - High variability in user engagement
   - Need for personalization strategies

## Generated Outputs

### Cleaned Datasets
- `data/processed/ratings_cleaned.csv` (100,836 rows)
- `data/processed/tags_cleaned.csv` (3,683 rows)
- `data/processed/movies_cleaned.csv` (9,742 rows)
- `data/processed/links_cleaned.csv` (9,742 rows)

### Processed Datasets
- `data/processed/ratings_processed.csv` (normalized)
- `data/processed/tags_processed.csv` (encoded)
- `data/processed/movies_processed.csv` (encoded)
- `data/processed/links_processed.csv` (normalized)

### Interaction Matrix
- `data/processed/user_item_interaction_matrix.csv` (610 × 9,742)
- Sparse matrix format (only non-zero ratings)

### Visualizations
- `data/plots/ratings_clean_distributions.png`
- `data/plots/ratings_heatmap.png`
- `data/plots/movies_categorical.png`
- `data/plots/user_item_interactions_sparsity.png`
- `data/plots/comprehensive_summary.png`

### Reports
- `data/processed/sparsity_report.json` - Detailed sparsity metrics
- `data/processed/data_preparation_summary.json` - Summary statistics

## Running the Notebook

### Prerequisites
```bash
pip install pandas numpy matplotlib seaborn scikit-learn
```

### Execute Notebook
```bash
jupyter notebook notebooks/01_Data_Preparation_EDA.ipynb
```

Or run directly:
```bash
cd RecoMart-Recommendation-Pipeline
jupyter notebook notebooks/01_Data_Preparation_EDA.ipynb
```

## Key Findings & Recommendations

### 1. Data Quality
- ✅ No missing values in ratings
- ✅ No duplicate ratings
- ⚠️ Some missing tmdbId in links (already addressed in validation)

### 2. Rating Distribution
- Normal-like distribution centered around 3.5 stars
- Long tail suggests mix of positive and critical ratings
- Good variety for recommendation learning

### 3. Sparsity Challenge
- 98.30% sparse matrix typical for collaborative filtering
- Cold-start problem for new items/users
- Need hybrid approach combining content + collaborative filtering

### 4. Recommendations

**For Model Selection:**
- Implicit feedback models for sparse data
- Matrix factorization techniques (SVD, NMF)
- Deep learning approaches (autoencoders, neural networks)
- Hybrid methods combining content and collaborative filtering

**For Handling Sparsity:**
- Use content features (genres, tags) for new items
- User segmentation for better personalization
- Temporal dynamics for popularity changes
- Social or demographic features for new users

**For Dataset Augmentation:**
- Consider adding timestamp-based features
- Extract features from movie titles and descriptions
- Leverage tag information for content-based features

## Next Steps

1. ✅ Data Preparation Complete
2. **Feature Engineering** - Create additional features from processed data
3. **Model Training** - Train recommendation models
4. **Evaluation** - Test on validation set
5. **Deployment** - Integrate into pipeline

## Integration with Pipeline

```python
# In main transformation pipeline
from src.preparation.data_cleaner import DataCleaner
from src.preparation.data_preprocessor import DataPreprocessor
from src.preparation.exploratory_analysis import ExploratoryAnalyzer

# Clean data
cleaner = DataCleaner()
df_clean, _ = cleaner.clean_csv(ratings_file, "ratings")

# Preprocess
preprocessor = DataPreprocessor()
df_processed, _ = preprocessor.preprocess_dataset(df_clean, "ratings")

# Analyze (optional, for monitoring)
analyzer = ExploratoryAnalyzer()
analysis = analyzer.analyze_dataset(df_processed, "ratings")

# Save prepared data
cleaner.save_cleaned_data()
preprocessor.save_processed_data()
```

## Troubleshooting

### Issue: Notebook kernel issues
**Solution**: Restart kernel and re-run from top

### Issue: Memory errors with large matrices
**Solution**: Use sparse matrix format or sample data

### Issue: Plot not displaying
**Solution**: Add `plt.show()` or `%matplotlib inline` in Jupyter

### Issue: Module import errors
**Solution**: Ensure project root is in sys.path and __init__.py files exist

## Dependencies

- **pandas**: Data manipulation
- **numpy**: Numerical computations
- **scikit-learn**: Preprocessing and encoding
- **matplotlib**: Static visualizations
- **seaborn**: Enhanced statistical plots

## File Structure

```
src/preparation/
├── __init__.py
├── data_cleaner.py (400+ lines)
├── data_preprocessor.py (350+ lines)
├── exploratory_analysis.py (500+ lines)

notebooks/
├── 01_Data_Preparation_EDA.ipynb (comprehensive walkthrough)

data/
├── processed/
│   ├── *_cleaned.csv (cleaned datasets)
│   ├── *_processed.csv (preprocessed datasets)
│   ├── user_item_interaction_matrix.csv
│   ├── sparsity_report.json
│   └── data_preparation_summary.json
└── plots/
    ├── *_distributions.png
    ├── *_heatmap.png
    ├── *_sparsity.png
    └── comprehensive_summary.png
```

---

**Status**: ✅ Complete and Tested  
**Last Updated**: 2026-07-18  
**Ready for**: Feature Engineering and Modeling
