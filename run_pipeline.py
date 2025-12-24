#!/usr/bin/env python3
"""
Standalone Pipeline Runner

This script runs the data pipeline without Jupyter, useful for:
- Automated/scheduled execution
- CI/CD pipelines
- Command-line workflows
- Testing and debugging

Usage:
    python run_pipeline.py [options]

Options:
    --data-file PATH    Path to input CSV file (default: data/sample.csv)
    --output-dir PATH   Output directory for results (default: output/)
    --verbose          Enable verbose logging
    --no-export        Skip CSV export step
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime


def setup_logging(verbose=False):
    """Configure logging based on verbosity level."""
    import logging

    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger(__name__)


def load_data_with_dlt(data_file, logger):
    """Load data using dlt pipeline."""
    import dlt
    import pandas as pd

    logger.info(f"Loading data from {data_file}...")

    @dlt.resource(name="sales_data", write_disposition="replace")
    def load_sales_data():
        """Load sales data from CSV file."""
        if not Path(data_file).exists():
            raise FileNotFoundError(f"Data file not found: {data_file}")

        df = pd.read_csv(data_file)
        logger.info(f"Loaded {len(df)} records")
        return df.to_dict('records')

    # Configure pipeline
    pipeline = dlt.pipeline(
        pipeline_name="local_data_pipeline",
        destination="duckdb",
        dataset_name="sales_analytics"
    )

    # Execute pipeline
    logger.info("Running dlt pipeline...")
    info = pipeline.run(load_sales_data())
    logger.info("✓ Data loaded successfully into DuckDB")

    return pipeline


def run_quality_checks(pipeline, logger):
    """Execute data quality checks."""
    logger.info("\nRunning data quality checks...")

    with pipeline.sql_client() as client:
        # Null value check
        null_check = """
            SELECT
                COUNT(*) as total_records,
                SUM(CASE WHEN date IS NULL THEN 1 ELSE 0 END) as null_dates,
                SUM(CASE WHEN product_category IS NULL THEN 1 ELSE 0 END) as null_categories,
                SUM(CASE WHEN quantity IS NULL THEN 1 ELSE 0 END) as null_quantities,
                SUM(CASE WHEN price IS NULL THEN 1 ELSE 0 END) as null_prices
            FROM sales_analytics.sales_data
        """

        with client.execute_query(null_check) as cursor:
            result = cursor.fetchone()
            if any(result[1:]):
                logger.warning("NULL values detected in data")
            else:
                logger.info("✓ No NULL values found")

        # Business rule validation
        business_check = """
            SELECT
                SUM(CASE WHEN quantity <= 0 THEN 1 ELSE 0 END) as invalid_quantity,
                SUM(CASE WHEN price <= 0 THEN 1 ELSE 0 END) as invalid_price
            FROM sales_analytics.sales_data
        """

        with client.execute_query(business_check) as cursor:
            result = cursor.fetchone()
            if result[0] > 0 or result[1] > 0:
                logger.warning(f"Business rule violations: {result}")
            else:
                logger.info("✓ All business rules satisfied")


def run_analytics(pipeline, logger):
    """Execute analytical queries and return results."""
    logger.info("\nRunning analytics queries...")

    results = {}

    with pipeline.sql_client() as client:
        # Summary statistics
        summary_query = """
            SELECT
                COUNT(*) as total_transactions,
                SUM(quantity * price) as total_revenue,
                ROUND(AVG(price), 2) as avg_price,
                ROUND(AVG(quantity), 2) as avg_quantity
            FROM sales_analytics.sales_data
        """
        results['summary'] = client.execute_query(summary_query).df()
        logger.info("✓ Summary statistics calculated")

        # Category analysis
        category_query = """
            SELECT
                product_category,
                COUNT(*) as transactions,
                SUM(quantity) as total_units_sold,
                SUM(quantity * price) as total_revenue,
                ROUND(AVG(price), 2) as avg_price
            FROM sales_analytics.sales_data
            GROUP BY product_category
            ORDER BY total_revenue DESC
        """
        results['category'] = client.execute_query(category_query).df()
        logger.info("✓ Category analysis completed")

        # Regional analysis
        regional_query = """
            SELECT
                region,
                COUNT(*) as transactions,
                SUM(quantity) as total_units_sold,
                SUM(quantity * price) as total_revenue
            FROM sales_analytics.sales_data
            GROUP BY region
            ORDER BY total_revenue DESC
        """
        results['regional'] = client.execute_query(regional_query).df()
        logger.info("✓ Regional analysis completed")

    return results


def export_results(results, output_dir, logger):
    """Export analysis results to CSV files."""
    logger.info(f"\nExporting results to {output_dir}...")

    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    exports = [
        ('summary', f'summary_stats_{timestamp}.csv'),
        ('category', f'category_analysis_{timestamp}.csv'),
        ('regional', f'regional_analysis_{timestamp}.csv')
    ]

    for key, filename in exports:
        filepath = output_path / filename
        results[key].to_csv(filepath, index=False)
        logger.info(f"✓ Exported: {filepath}")


def main():
    """Main pipeline execution function."""
    parser = argparse.ArgumentParser(
        description='Run the local data engineering pipeline'
    )
    parser.add_argument(
        '--data-file',
        default='data/sample.csv',
        help='Path to input CSV file'
    )
    parser.add_argument(
        '--output-dir',
        default='output',
        help='Output directory for results'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    parser.add_argument(
        '--no-export',
        action='store_true',
        help='Skip CSV export step'
    )

    args = parser.parse_args()

    # Setup logging
    logger = setup_logging(args.verbose)

    try:
        logger.info("=" * 60)
        logger.info("LOCAL DATA ENGINEERING PIPELINE")
        logger.info("=" * 60)

        # Load data
        pipeline = load_data_with_dlt(args.data_file, logger)

        # Quality checks
        run_quality_checks(pipeline, logger)

        # Analytics
        results = run_analytics(pipeline, logger)

        # Export (unless skipped)
        if not args.no_export:
            export_results(results, args.output_dir, logger)
        else:
            logger.info("\nSkipping export (--no-export flag set)")

        logger.info("\n" + "=" * 60)
        logger.info("✓ PIPELINE COMPLETED SUCCESSFULLY")
        logger.info("=" * 60)

        return 0

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        return 1
    except Exception as e:
        logger.error(f"Pipeline failed: {e}", exc_info=args.verbose)
        return 1


if __name__ == "__main__":
    sys.exit(main())
