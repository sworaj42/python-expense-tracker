# Personal Expense Tracker (CLI)

A Python command-line application for tracking daily expenses with
monthly summaries, category-wise analysis, visualizations, and CSV export.

---

## Overview

This application allows users to record daily expenses, view spending by
day and month, and analyze expenses using simple charts. Data is stored
locally using JSON and can be exported to CSV.

---

## Features

- Add, update, and delete expenses
- View expenses for a specific day
- Monthly spending summary
- Category-wise spending analysis
- Daily spending trend visualization
- JSON-based data storage
- CSV export

---

## Technologies Used

- Python 3
- dataclasses
- JSON and CSV
- matplotlib

---

## How to Run

### Install Dependency

pip install matplotlib

---

### Load Sample Data (January 2025)

A file named `expenses.sample.json` is included in the repository.
It contains sample expense data for January 2025 (2025-01).

To use the sample data:
- Rename `expenses.sample.json` to `expenses.json`
- Run the program using:

python expense_tracker.py

The data will be loaded automatically when the program starts.

---

### Run Without Sample Data

If `expenses.json` does not exist, the program starts with no data and
creates the file automatically when an expense is added.

---

## File Structure

expense_tracker.py  
expenses.sample.json  
README.md  

---

## Author

Swaraj Sigdel
