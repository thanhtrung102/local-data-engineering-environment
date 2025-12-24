# Quick Start Guide

Get up and running in 5 minutes!

## Prerequisites

- Python 3.9 or higher
- Terminal/Command Prompt access

## Setup (1 minute)

### Windows
```cmd
setup.bat
env\Scripts\activate.bat
```

### Linux/Mac
```bash
chmod +x setup.sh
./setup.sh
source env/bin/activate
```

## Verify (30 seconds)

```bash
python test_setup.py
```

Expected output: `✓ ALL CHECKS PASSED!`

## Run Pipeline

### Option 1: Jupyter Notebook (Interactive)

```bash
jupyter notebook
```

Then open `notebooks/data_workflow.ipynb` and click "Run All"

### Option 2: Command Line (Automated)

```bash
python run_pipeline.py
```

## What You'll See

1. Data loads from `data/sample.csv` into DuckDB
2. Quality checks run automatically
3. Analytics queries execute:
   - Summary statistics
   - Category analysis (by product)
   - Regional analysis (by geography)
4. Results export to `output/` directory

## Check Results

```bash
ls output/
```

You should see three CSV files with timestamps:
- `summary_stats_*.csv`
- `category_analysis_*.csv`
- `regional_analysis_*.csv`

## Next Steps

1. Explore the Jupyter notebook to see how it works
2. Modify the SQL queries to try different analytics
3. Add your own CSV data to `data/` directory
4. Read `README.md` for detailed documentation

## Common Issues

**Python not found?**
- Install from https://www.python.org/

**Virtual environment won't activate?**
- Windows: Try `env\Scripts\Activate.ps1` in PowerShell
- Linux/Mac: Use `source env/bin/activate`

**Packages won't install?**
- Upgrade pip: `pip install --upgrade pip`
- Retry: `pip install -r requirements.txt`

## Learn More

- `README.md` - Full documentation
- `CLAUDE.md` - Technical details
- `CONTRIBUTING.md` - How to extend the project

---

**Need help?** Check the Troubleshooting section in README.md
