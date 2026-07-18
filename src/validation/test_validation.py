"""
Test Data Validation Pipeline

Runs the complete data validation and profiling workflow,
generates quality reports, and demonstrates the validation framework.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

from src.config.config import CSV_FILES
from src.validation.validation_pipeline import DataValidationPipeline
from src.utils.logger import logger


def main():
    """Run validation pipeline and generate reports."""

    logger.info("Starting Data Validation Pipeline Test")

    # Initialize pipeline
    pipeline = DataValidationPipeline()

    # Run validation and profiling
    results = pipeline.run_validation(datasets=CSV_FILES)

    # Print summary
    pipeline.print_summary(results)

    # Return results for programmatic access
    return results


if __name__ == "__main__":
    results = main()
