import os
import csv
import pytest
import subprocess

def test_e2e(tmp_path: str) -> None:
    # Change to a temp directory to avoid overwriting real output.csv
    """End-to-end test for main.py."""
    orig_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        # Run main.py as a subprocess using pytest's built-in python
        exit_code = os.system(f'python {os.path.join(orig_cwd, "main.py")}')
        assert exit_code == 0, "main.py did not exit cleanly"
        # Check that output.csv was created
        assert os.path.exists("output.csv"), "output.csv was not created"
        # Check that the CSV has the correct header
        with open("output.csv", newline="") as f:
            reader = csv.reader(f)
            header = next(reader)
            assert header == ["Email ID", "Percentage Probability of SPAM"]
            # Optionally, check that at least one row exists
            rows = list(reader)
            assert len(rows) > 0, "No results written to output.csv"
    finally:
        os.chdir(orig_cwd)
