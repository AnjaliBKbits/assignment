"""
Quick Reference: Data Validation & Profiling

Simple examples and common use cases for the validation framework.
"""

# ============================================================
# EXAMPLE 1: Basic Validation
# ============================================================

from src.validation.data_validator import DataValidator
from pathlib import Path

validator = DataValidator()

# Define expected schema
schema = {
    "movieId": "int",
    "title": "str",
    "genres": "str",
}

# Run validation
result = validator.validate_csv(
    file_path=Path("dataset/movies.csv"),
    dataset_name="movies",
    schema=schema,
)

# Check results
print(f"Status: {result['status']}")  # PASS or FAIL
print(f"Issues: {result['issues']}")  # List of problems


# ============================================================
# EXAMPLE 2: Validation with Constraints
# ============================================================

validator = DataValidator()

schema = {
    "userId": "int",
    "movieId": "int",
    "rating": "float",
    "timestamp": "int",
}

# Define business logic constraints
constraints = {
    "rating": {
        "type": "range",
        "min": 0.5,
        "max": 5.0,
    },
    "userId": {
        "type": "range",
        "min": 1,
    },
    "movieId": {
        "type": "range",
        "min": 1,
    },
}

result = validator.validate_csv(
    file_path=Path("dataset/ratings.csv"),
    dataset_name="ratings",
    schema=schema,
    constraints=constraints,
)

# Check for constraint violations
for check_name, check_result in result["checks"].items():
    if check_result["status"] == "FAIL":
        print(f"⚠ {check_name}: {check_result['message']}")


# ============================================================
# EXAMPLE 3: Data Profiling
# ============================================================

from src.validation.data_profiler import DataProfiler

profiler = DataProfiler()

profile = profiler.profile_dataset(
    file_path=Path("dataset/ratings.csv"),
    dataset_name="ratings"
)

# Access basic info
basic = profile["basic_info"]
print(f"Total rows: {basic['total_rows']}")
print(f"Total columns: {basic['total_columns']}")
print(f"Memory usage: {basic['memory_usage_mb']} MB")

# Access column statistics
for col_name, col_profile in profile["column_profiles"].items():
    print(f"\n{col_name}:")
    print(f"  Type: {col_profile['data_type']}")
    print(f"  Null %: {col_profile['null_percentage']}%")
    print(f"  Unique: {col_profile['unique_values']}")
    
    # For numeric columns
    if "min" in col_profile:
        print(f"  Min: {col_profile['min']}")
        print(f"  Max: {col_profile['max']}")
        print(f"  Mean: {col_profile['mean']:.2f}")

# Access quality metrics
metrics = profile["data_quality_metrics"]
print(f"\nQuality Score: {metrics['overall_quality_score']:.2f}%")
print(f"Completeness: {metrics['completeness_percentage']:.2f}%")


# ============================================================
# EXAMPLE 4: Full Pipeline with Report
# ============================================================

from src.validation.validation_pipeline import DataValidationPipeline
from src.config.config import CSV_FILES

pipeline = DataValidationPipeline()

# Run full validation pipeline
results = pipeline.run_validation(
    datasets=CSV_FILES,
    custom_constraints={
        "ratings": {
            "rating": {"type": "range", "min": 0.5, "max": 5.0},
        }
    }
)

# Print summary to console
pipeline.print_summary(results)

# Access detailed results
validation_results = results["validation"]
profiling_results = results["profiling"]
report_path = results["report_path"]

print(f"\nReport saved to: {report_path}")

# Check individual dataset
for dataset_name, validation in validation_results.items():
    if validation["status"] == "FAIL":
        print(f"\n⚠ {dataset_name} has issues:")
        for issue in validation["issues"]:
            print(f"  - {issue['type']}: {issue['message']}")


# ============================================================
# EXAMPLE 5: Iterating Through Validation Results
# ============================================================

# Get summary of all validations
summary = pipeline.validator.get_summary()

print(f"Total datasets: {summary['total_datasets']}")
print(f"Passed: {summary['passed_datasets']}")
print(f"Failed: {summary['failed_datasets']}")

# Categorize issues
issues_by_type = summary["issue_summary"]
for issue_type, count in issues_by_type.items():
    print(f"{issue_type}: {count} issues")


# ============================================================
# EXAMPLE 6: Accessing Detailed Check Results
# ============================================================

validation_result = results["validation"]["movies"]

# Schema check
schema_check = validation_result["checks"]["schema"]
print(f"Schema Status: {schema_check['status']}")
print(f"Columns found: {schema_check['columns_found']}")

# Missing values check
missing_check = validation_result["checks"]["missing_values"]
print(f"Missing values: {missing_check['details']}")

# Duplicates check
dup_check = validation_result["checks"]["duplicates"]
print(f"Duplicate count: {dup_check['details']['duplicate_count']}")


# ============================================================
# EXAMPLE 7: Custom Validation Schemas
# ============================================================

# Create different schemas for different datasets
schemas = {
    "movies": {
        "movieId": "int",
        "title": "str",
        "genres": "str",
    },
    "ratings": {
        "userId": "int",
        "movieId": "int",
        "rating": "float",
        "timestamp": "int",
    },
    "tags": {
        "userId": "int",
        "movieId": "int",
        "tag": "str",
        "timestamp": "int",
    },
}

# Validate each with appropriate schema
validator = DataValidator()
for dataset_name, file_path in CSV_FILES.items():
    schema = schemas[dataset_name]
    result = validator.validate_csv(file_path, dataset_name, schema)
    print(f"{dataset_name}: {result['status']}")


# ============================================================
# EXAMPLE 8: Filtering Issues by Severity
# ============================================================

validation_results = results["validation"]

# Find all HIGH severity issues
critical_issues = []
for dataset_name, validation in validation_results.items():
    for issue in validation["issues"]:
        if issue.get("severity") == "HIGH":
            critical_issues.append({
                "dataset": dataset_name,
                "issue": issue
            })

print(f"Critical issues found: {len(critical_issues)}")
for item in critical_issues:
    print(f"  {item['dataset']}: {item['issue']['message']}")


# ============================================================
# EXAMPLE 9: Data Quality Comparison
# ============================================================

profiling = results["profiling"]

# Compare quality scores
print("Data Quality Comparison:")
quality_by_dataset = {}
for dataset_name, profile in profiling["profiles"].items():
    quality_score = profile["data_quality_metrics"]["overall_quality_score"]
    completeness = profile["data_quality_metrics"]["completeness_percentage"]
    quality_by_dataset[dataset_name] = {
        "quality": quality_score,
        "completeness": completeness
    }

# Sort by quality score
for dataset_name, metrics in sorted(
    quality_by_dataset.items(),
    key=lambda x: x[1]["quality"],
    reverse=True
):
    print(f"  {dataset_name}: {metrics['quality']:.2f}% quality, "
          f"{metrics['completeness']:.2f}% complete")


# ============================================================
# EXAMPLE 10: Saving Results for Later Analysis
# ============================================================

import json

# Save validation results
results_file = Path("data/reports/validation_results.json")
with open(results_file, "w") as f:
    json.dump(results, f, indent=2, default=str)

# Load and analyze later
with open(results_file, "r") as f:
    loaded_results = json.load(f)

# Continue analysis...
print(f"Loaded results from {results_file}")
print(f"Validation status: {loaded_results['status']}")
