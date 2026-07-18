"""
Test suite for API validation and preparation modules
"""

import json
import tempfile
from pathlib import Path
import sys
import pandas as pd

# Setup paths
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.validation.api_validator import (
    APIValidator,
    APIDataProfiler,
    get_default_product_schema,
    get_default_product_constraints,
)
from src.preparation.api_preparation import (
    APIDataCleaner,
    APIDataPreprocessor,
    normalize_product_for_recommendation,
)
from src.preparation.data_fusion import (
    DataFusionEngine,
    HybridRecommendationPreparator,
)


def create_sample_api_data():
    """Create sample API response data for testing."""
    return {
        "products": [
            {
                "id": 1,
                "title": "Wireless Headphones",
                "description": "High-quality wireless headphones",
                "price": 99.99,
                "discountPercentage": 10,
                "rating": 4.5,
                "stock": 50,
                "brand": "AudioBrand",
                "category": "Electronics",
                "thumbnail": "https://example.com/thumb1.jpg",
                "images": ["https://example.com/img1.jpg"],
            },
            {
                "id": 2,
                "title": "USB-C Cable",
                "description": "Durable USB-C charging cable",
                "price": 9.99,
                "discountPercentage": 5,
                "rating": 4.2,
                "stock": 200,
                "brand": "CableCo",
                "category": "Accessories",
                "thumbnail": "https://example.com/thumb2.jpg",
                "images": ["https://example.com/img2.jpg"],
            },
            {
                "id": 3,
                "title": "Laptop Stand",
                "description": "Adjustable laptop stand",
                "price": 49.99,
                "discountPercentage": 15,
                "rating": 4.8,
                "stock": 30,
                "brand": "DeskGear",
                "category": "Office",
                "thumbnail": "https://example.com/thumb3.jpg",
                "images": ["https://example.com/img3.jpg"],
            },
        ]
    }


def test_api_validator():
    """Test API validation module."""
    print("\n" + "=" * 80)
    print("TEST 1: API VALIDATOR")
    print("=" * 80)

    validator = APIValidator()
    schema = get_default_product_schema()
    constraints = get_default_product_constraints()

    # Create temporary JSON file
    sample_data = create_sample_api_data()
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(sample_data, f)
        temp_file = Path(f.name)

    try:
        # Test 1.1: Validate JSON file
        print("\n[1.1] Testing JSON file validation...")
        records, report = validator.validate_json_file(
            temp_file,
            schema=schema,
            constraints=constraints
        )

        assert records is not None
        assert len(records) > 0
        assert report["total_records"] == 3
        assert report["valid_records"] == 3
        print(f"  ✓ Validation: {report['valid_records']}/{report['total_records']} records valid")

        # Test 1.2: Schema validation
        print("\n[1.2] Testing schema validation...")
        assert "id" in records[0]
        assert "title" in records[0]
        assert "price" in records[0]
        print(f"  ✓ All required fields present")

        # Test 1.3: Constraint validation
        print("\n[1.3] Testing constraint validation...")
        for product in records:
            assert 0 < product["price"] < 10000
            assert 0 <= product["rating"] <= 5
        print(f"  ✓ All values within constraints")

        print("\n✅ API VALIDATOR TESTS PASSED (3/3)")
        return True

    finally:
        temp_file.unlink()


def test_api_profiler():
    """Test API data profiler."""
    print("\n" + "=" * 80)
    print("TEST 2: API DATA PROFILER")
    print("=" * 80)

    profiler = APIDataProfiler()
    sample_data = create_sample_api_data()
    records = sample_data["products"]

    # Test 2.1: Profile API data
    print("\n[2.1] Testing API data profiling...")
    profile = profiler.profile_api_data(records, "test_products")

    assert profile is not None
    assert profile["basic_stats"]["total_records"] == 3
    assert len(profile["field_profiles"]) > 0
    print(f"  ✓ Profiled {profile['basic_stats']['total_records']} records")

    # Test 2.2: Data quality assessment
    print("\n[2.2] Testing data quality assessment...")
    quality = profile["data_quality"]
    assert quality["quality_score"] >= 0
    assert quality["completeness_percentage"] >= 0
    print(f"  ✓ Quality score: {quality['quality_score']:.1f}%")

    # Test 2.3: Field statistics
    print("\n[2.3] Testing field statistics...")
    field_profiles = profile["field_profiles"]
    assert "price" in field_profiles
    assert "rating" in field_profiles
    print(f"  ✓ Profiled {len(field_profiles)} fields")

    print("\n✅ API PROFILER TESTS PASSED (3/3)")
    return True


def test_api_cleaner():
    """Test API data cleaner."""
    print("\n" + "=" * 80)
    print("TEST 3: API DATA CLEANER")
    print("=" * 80)

    cleaner = APIDataCleaner()
    sample_data = create_sample_api_data()
    records = sample_data["products"]

    # Test 3.1: Clean API data
    print("\n[3.1] Testing API data cleaning...")
    df_clean, report = cleaner.clean_api_data(
        records=records,
        dataset_name="products",
        flatten_nested=True,
        missing_strategy="drop"
    )

    assert df_clean is not None
    assert len(df_clean) > 0
    print(f"  ✓ Cleaned: {report['initial_rows']} → {report['final_rows']} rows")

    # Test 3.2: Check data types
    print("\n[3.2] Testing data type fixes...")
    numeric_cols = df_clean.select_dtypes(include=['int64', 'float64']).columns
    assert len(numeric_cols) > 0
    print(f"  ✓ Numeric columns: {list(numeric_cols)}")

    # Test 3.3: Text normalization
    print("\n[3.3] Testing text normalization...")
    if "title" in df_clean.columns:
        for title in df_clean["title"]:
            assert isinstance(title, str)
            assert title == title.strip()
    print(f"  ✓ Text normalized")

    print("\n✅ API CLEANER TESTS PASSED (3/3)")
    return True


def test_api_preprocessor():
    """Test API data preprocessor."""
    print("\n" + "=" * 80)
    print("TEST 4: API DATA PREPROCESSOR")
    print("=" * 80)

    cleaner = APIDataCleaner()
    preprocessor = APIDataPreprocessor()
    sample_data = create_sample_api_data()
    records = sample_data["products"]

    # Clean first
    df_clean, _ = cleaner.clean_api_data(records, "products")

    # Test 4.1: Preprocess data
    print("\n[4.1] Testing API data preprocessing...")
    df_processed, report = preprocessor.preprocess_api_data(
        df=df_clean,
        dataset_name="products",
        normalize_method="minmax"
    )

    assert df_processed is not None
    assert len(df_processed) > 0
    print(f"  ✓ Preprocessed: {len(report['operations'])} operations")

    # Test 4.2: Feature extraction
    print("\n[4.2] Testing feature extraction...")
    df_features, feature_report = preprocessor.extract_features(df_processed, "products")

    assert len(feature_report["new_features"]) > 0
    print(f"  ✓ Extracted {len(feature_report['new_features'])} features")

    # Test 4.3: Data normalization
    print("\n[4.3] Testing data normalization...")
    if "price" in df_processed.columns:
        assert df_processed["price"].min() >= 0
        assert df_processed["price"].max() <= 1
    print(f"  ✓ Values normalized to [0, 1]")

    print("\n✅ API PREPROCESSOR TESTS PASSED (3/3)")
    return True


def test_data_fusion():
    """Test data fusion engine."""
    print("\n" + "=" * 80)
    print("TEST 5: DATA FUSION ENGINE")
    print("=" * 80)

    fusion = DataFusionEngine()

    # Create sample data
    df_ratings = pd.DataFrame({
        "userId": [1, 1, 2, 2, 3],
        "movieId": [1, 2, 1, 3, 2],
        "rating": [4.5, 3.0, 5.0, 4.0, 3.5],
        "timestamp": ["2026-07-01", "2026-07-02", "2026-07-03", "2026-07-04", "2026-07-05"],
    })

    sample_data = create_sample_api_data()
    df_products = pd.DataFrame(sample_data["products"])

    # Test 5.1: Fuse ratings with products
    print("\n[5.1] Testing ratings-products fusion...")
    df_fused, report = fusion.fuse_ratings_with_products(
        df_ratings=df_ratings,
        df_products=df_products,
        user_col="userId",
        item_col="movieId",
        product_id_col="id"
    )

    assert df_fused is not None
    print(f"  ✓ Fused: {len(df_fused)} rows")

    # Test 5.2: Create hybrid features
    print("\n[5.2] Testing hybrid feature creation...")
    df_hybrid, feature_report = fusion.create_hybrid_features(df_fused)

    assert len(feature_report["new_features"]) > 0
    print(f"  ✓ Created {len(feature_report['new_features'])} hybrid features")

    # Test 5.3: Dataset comparison
    print("\n[5.3] Testing dataset comparison...")
    comparison = fusion.merge_dataset_comparison(
        df_csv=df_ratings,
        df_api=df_products,
        csv_id_col="movieId",
        api_id_col="id"
    )

    assert comparison["overlap_count"] >= 0
    print(f"  ✓ Overlap: {comparison['overlap_count']}/{comparison['csv_total_items']} items")

    print("\n✅ DATA FUSION TESTS PASSED (3/3)")
    return True


def test_hybrid_recommendation():
    """Test hybrid recommendation preparator."""
    print("\n" + "=" * 80)
    print("TEST 6: HYBRID RECOMMENDATION PREPARATOR")
    print("=" * 80)

    preparator = HybridRecommendationPreparator()

    # Create sample data
    df_ratings = pd.DataFrame({
        "userId": [1, 1, 2, 2, 3, 3],
        "movieId": [1, 2, 1, 3, 2, 3],
        "rating": [4.5, 3.0, 5.0, 4.0, 3.5, 2.5],
        "timestamp": ["2026-07-01", "2026-07-02", "2026-07-03", "2026-07-04", "2026-07-05", "2026-07-06"],
    })

    sample_data = create_sample_api_data()
    df_products = pd.DataFrame(sample_data["products"])

    # Test 6.1: Prepare for hybrid model
    print("\n[6.1] Testing hybrid model preparation...")
    prepared, report = preparator.prepare_for_hybrid_model(
        df_ratings=df_ratings,
        df_products=df_products,
        user_col="userId",
        item_col="movieId",
        rating_col="rating"
    )

    assert len(prepared) > 0
    assert "interaction_matrix" in prepared
    assert "user_features" in prepared
    assert "item_features" in prepared
    print(f"  ✓ Prepared {len(prepared)} components")

    # Test 6.2: Interaction matrix
    print("\n[6.2] Testing interaction matrix generation...")
    interaction_matrix = prepared["interaction_matrix"]
    assert interaction_matrix is not None
    print(f"  ✓ Interaction matrix shape: {interaction_matrix.shape}")

    # Test 6.3: User features
    print("\n[6.3] Testing user features generation...")
    user_features = prepared["user_features"]
    assert len(user_features) > 0
    assert "rating_count" in user_features.columns
    print(f"  ✓ User features: {len(user_features)} users")

    print("\n✅ HYBRID RECOMMENDATION TESTS PASSED (3/3)")
    return True


def main():
    """Run all API tests."""
    print("\n" + "=" * 80)
    print("API VALIDATION & PREPARATION TEST SUITE")
    print("=" * 80)

    try:
        results = []

        # Run tests
        results.append(("API Validator", test_api_validator()))
        results.append(("API Profiler", test_api_profiler()))
        results.append(("API Cleaner", test_api_cleaner()))
        results.append(("API Preprocessor", test_api_preprocessor()))
        results.append(("Data Fusion", test_data_fusion()))
        results.append(("Hybrid Recommendation", test_hybrid_recommendation()))

        # Print summary
        print("\n" + "=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)

        passed = sum(1 for _, result in results if result)
        total = len(results)

        for test_name, result in results:
            status = "PASSED" if result else "FAILED"
            print(f"{test_name}: {status}")

        print(f"\nTotal: {passed}/{total} test groups passed")

        if passed == total:
            print("\n✅ ALL API TESTS PASSED - API Module is Ready!")
            print("=" * 80 + "\n")
            return 0
        else:
            print("\n❌ SOME TESTS FAILED")
            print("=" * 80 + "\n")
            return 1

    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
