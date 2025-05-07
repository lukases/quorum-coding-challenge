# Quorum Coding Challenge (PoC with Pandas)

This is a proof of concept (PoC) built with Python and Pandas that processes CSV files containing data about legislators, bills, votes, and vote results, generating aggregated reports.

---

## Project Structure

├── main.py # Main processing script

├── tests.py # Unit tests using pytest

├── data/

│ ├── legislators.csv

│ ├── bills.csv

│ ├── votes.csv

│ └── vote_results.csv

├── output/

│ ├── legislators-support-oppose-count.csv

│ └── bills.csv

---

## Requirements

- Python 3.8+
- pandas
- pytest (for running tests)

---

## Setup Instructions

### 1. Create and activate a virtual environment

```bash
# Create virtualenv
python -m venv venv

# Activate on Unix/macOS
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate
```

### 2. Install dependencies using:

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install pandas pytest
```

## Running the Main Script

```py
python main.py
```

This will:

- Load data from the "data/" directory
- Process and analyze the data
- Write two output files to the "output/" directory:
1. legislators-support-oppose-count.csv
2. bills.csv

## Running Tests
Use pytest to run the unit tests:

```bash
pytest tests.py
```

## Notes

- Input .csv files must be located in the data/ directory.
- Output files will be saved in the output/ directory.
- Code is modular and easy to expand.
- Great for CSV-based data validation without needing a database.
