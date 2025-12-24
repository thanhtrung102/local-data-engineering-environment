# Local Data Engineering Environment

A hands-on, production-ready local data engineering environment for learning and experimenting with modern data engineering tools and practices.

## Overview

This project provides a complete, working data pipeline that demonstrates core data engineering concepts using industry-standard tools. It's designed to run entirely on your local machine without requiring cloud services or complex infrastructure.

## Learning Objectives

By working with this environment, you'll gain practical experience with:

- **Data Ingestion**: Loading data from various sources using dlt (data load tool)
- **Schema Management**: Automatic schema inference and evolution
- **Data Quality**: Implementing validation checks and data quality monitoring
- **Analytics**: Running SQL queries for business insights using DuckDB
- **Pipeline Orchestration**: Building reproducible data workflows
- **Best Practices**: Following industry standards for code organization and documentation

## Core Technologies

- **[dlt](https://dlthub.com/)**: Modern data loading framework with automatic schema management
- **[DuckDB](https://duckdb.org/)**: High-performance analytical database (embedded, no server required)
- **[Pandas](https://pandas.pydata.org/)**: Data manipulation and analysis
- **[Jupyter](https://jupyter.org/)**: Interactive notebook environment for development and documentation

## Requirements

### Technical Requirements

- **Python**: 3.9 or higher
- **Operating System**: Windows, macOS, or Linux
- **Disk Space**: ~500MB (for Python environment and dependencies)
- **RAM**: 2GB minimum (4GB recommended)

### Skills Prerequisites

- Basic Python knowledge
- Familiarity with SQL (helpful but not required)
- Command line/terminal basics

## Project Structure

```
local-data-engineering-environment/
│
├── notebooks/                  # Jupyter notebooks
│   └── data_workflow.ipynb    # Main data pipeline notebook
│
├── data/                       # Sample datasets
│   └── sample.csv             # Sample sales data
│
├── output/                     # Generated analysis results (auto-created)
│   ├── summary_stats_*.csv
│   ├── category_analysis_*.csv
│   └── regional_analysis_*.csv
│
├── env/                        # Virtual environment (auto-created)
│
├── setup.sh                    # Setup script for Linux/Mac
├── setup.bat                   # Setup script for Windows
├── test_setup.py              # Validation script
├── requirements.txt           # Python dependencies
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

## Quick Start

### Step 1: Clone or Download

If you have git:
```bash
git clone <repository-url>
cd local-data-engineering-environment
```

Or download and extract the ZIP file, then navigate to the directory.

### Step 2: Run Setup Script

#### Linux/Mac

```bash
chmod +x setup.sh
./setup.sh
```

#### Windows

Double-click `setup.bat` or run from Command Prompt:
```cmd
setup.bat
```

The setup script will:
- Check your Python version
- Create a virtual environment
- Install all dependencies
- Set up Jupyter kernel

### Step 3: Verify Installation

Activate the virtual environment:

#### Linux/Mac
```bash
source env/bin/activate
```

#### Windows
```cmd
env\Scripts\activate.bat
```

Run the validation tests:
```bash
python test_setup.py
```

You should see "ALL CHECKS PASSED" if everything is configured correctly.

### Step 4: Start Jupyter Notebook

```bash
jupyter notebook
```

This will open Jupyter in your web browser.

### Step 5: Run the Pipeline

1. In Jupyter, navigate to `notebooks/data_workflow.ipynb`
2. Click "Cell" → "Run All" to execute the entire pipeline
3. Watch as the notebook:
   - Loads data from CSV
   - Performs quality checks
   - Runs analytical queries
   - Exports results to CSV files

## Detailed Usage Workflow

### 1. Data Loading

The pipeline uses dlt to load data from CSV files into DuckDB:

```python
@dlt.resource(name="sales_data", write_disposition="replace")
def load_sales_data():
    csv_path = Path("../data/sample.csv")
    df = pd.read_csv(csv_path)
    return df.to_dict('records')

pipeline = dlt.pipeline(
    pipeline_name="local_data_pipeline",
    destination="duckdb",
    dataset_name="sales_analytics"
)

info = pipeline.run(load_sales_data())
```

**Key Concepts**:
- `@dlt.resource`: Marks the function as a data source
- `write_disposition="replace"`: Controls how data is loaded (replace/append/merge)
- DuckDB automatically creates tables based on inferred schema

### 2. Data Quality Checks

The notebook implements several quality checks:

- **Null Value Detection**: Identifies missing data
- **Business Rule Validation**: Ensures data meets business requirements (e.g., quantity > 0)
- **Duplicate Detection**: Finds duplicate records
- **Data Statistics**: Provides overview of data characteristics

### 3. Analytics Queries

Run SQL queries directly on DuckDB:

```python
summary_query = """
    SELECT
        COUNT(*) as total_transactions,
        SUM(quantity * price) as total_revenue,
        AVG(price) as avg_price
    FROM sales_analytics.sales_data
"""

with pipeline.sql_client() as client:
    summary_df = client.execute_query(summary_query).df()
```

### 4. Results Export

Analysis results are automatically exported to timestamped CSV files:

```
output/
├── summary_stats_20240124_143022.csv
├── category_analysis_20240124_143022.csv
└── regional_analysis_20240124_143022.csv
```

## Working with Your Own Data

### Adding New Data Sources

1. Place your CSV file in the `data/` directory
2. Modify the `load_sales_data()` function to read your file
3. Update column references in quality checks and queries

### Connecting to APIs

```python
@dlt.resource
def load_api_data():
    import requests
    response = requests.get("https://api.example.com/data")
    return response.json()
```

### Loading from Databases

```python
@dlt.resource
def load_from_postgres():
    import psycopg2
    conn = psycopg2.connect("postgresql://user:pass@localhost/db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM table")
    return cursor.fetchall()
```

## Troubleshooting

### Python Version Issues

**Problem**: "Python 3.9+ required" error

**Solution**:
- Check your Python version: `python --version`
- Install Python 3.9 or higher from [python.org](https://www.python.org/)
- On some systems, use `python3` instead of `python`

### Virtual Environment Activation

**Problem**: Virtual environment won't activate

**Solution**:
- Linux/Mac: Ensure you use `source env/bin/activate`
- Windows: Try `env\Scripts\activate.bat` or `env\Scripts\Activate.ps1` (PowerShell)
- Check file permissions: `chmod +x env/bin/activate` (Linux/Mac)

### Package Installation Failures

**Problem**: Errors during `pip install`

**Solution**:
- Upgrade pip: `pip install --upgrade pip`
- Install packages individually to identify the problematic one
- Check internet connection
- On Linux, you may need development headers: `sudo apt-get install python3-dev`

### Jupyter Kernel Not Found

**Problem**: "Local DE Environment" kernel not available in Jupyter

**Solution**:
- Re-run: `python -m ipykernel install --user --name=local-de-env`
- Restart Jupyter Notebook
- Check installed kernels: `jupyter kernelspec list`

### DuckDB Connection Issues

**Problem**: Cannot connect to DuckDB or table not found

**Solution**:
- Delete the DuckDB file and re-run the notebook
- Ensure the pipeline ran successfully (check for error messages)
- Verify dataset and table names match in queries

### File Path Issues

**Problem**: "File not found" errors

**Solution**:
- Ensure you're running Jupyter from the project root directory
- Check that `data/sample.csv` exists
- Use absolute paths if relative paths don't work

## Success Criteria

Your environment is working correctly if:

- ✓ `test_setup.py` passes all checks
- ✓ Jupyter notebook runs without errors
- ✓ Data loads successfully into DuckDB
- ✓ Quality checks execute and report results
- ✓ Analytics queries return data
- ✓ CSV files are created in the `output/` directory
- ✓ You can modify queries and see different results

## Future Enhancements

### Easy Extensions

- Add more sample datasets
- Create additional analytical queries
- Implement data visualizations with matplotlib or plotly
- Add more data quality checks

### Intermediate Extensions

- Implement incremental loading (append mode)
- Add data transformation logic
- Create a simple data catalog
- Implement logging and monitoring

### Advanced Extensions

- Schedule pipeline execution with cron/Task Scheduler
- Add multiple data sources (APIs, databases)
- Implement a simple web dashboard
- Create data lineage tracking
- Add unit tests for data transformations
- Implement schema versioning

## Additional Resources

### Documentation

- [dlt Documentation](https://dlthub.com/docs)
- [DuckDB Documentation](https://duckdb.org/docs/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Jupyter Documentation](https://jupyter.org/documentation)

### Learning Resources

- [dlt Getting Started Guide](https://dlthub.com/docs/getting-started)
- [DuckDB Tutorials](https://duckdb.org/docs/guides/index)
- [Data Engineering Best Practices](https://www.startdataengineering.com/)

### Community

- [dlt Discord](https://discord.com/invite/nMM74A7CkD)
- [DuckDB Discord](https://discord.duckdb.org/)
- [r/dataengineering](https://www.reddit.com/r/dataengineering/)

## Contributing

If you'd like to improve this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is released under the MIT License. Feel free to use it for learning, teaching, or as a foundation for your own projects.

## Acknowledgments

Built with:
- [dlt](https://dlthub.com/) - Modern data loading framework
- [DuckDB](https://duckdb.org/) - High-performance analytical database
- [Pandas](https://pandas.pydata.org/) - Data manipulation library
- [Jupyter](https://jupyter.org/) - Interactive computing environment

---

**Questions or Issues?**

If you encounter problems or have questions:
1. Check the Troubleshooting section above
2. Review the documentation links
3. Open an issue on GitHub
4. Reach out to the community forums

Happy Data Engineering! 🚀
