import pytest
import csv
import json
import os
from unittest.mock import patch, MagicMock
import logging

import main
import message

# Define the expected CSV header
EXPECTED_CSV_HEADER = ["Email ID", "Percentage Probability of SPAM", "Tone"]

OUTPUT_FILENAME = "output.csv"
TEST_EMAIL_LIMIT = 2 # Define a limit for the test run

@pytest.fixture(autouse=True)
def manage_output_file() -> None: # type: ignore[misc]
    """Fixture to ensure the output file is removed before and after the test."""
    # Setup: Remove the output file if it exists before the test
    if os.path.exists(OUTPUT_FILENAME):
        os.remove(OUTPUT_FILENAME)

    yield # Run the test

    # Teardown: Remove the output file after the test
    if os.path.exists(OUTPUT_FILENAME):
        os.remove(OUTPUT_FILENAME)


def test_e2e_main_flow_real_clients(monkeypatch, caplog) -> None: # type: ignore[no-untyped-def]
    """Test the end-to-end flow using real inbox and AI clients."""
    caplog.set_level(logging.INFO) # Capture logs for debugging

    # Check if credentials.json exists, otherwise skip the test
    if not os.path.exists("credentials.json"):
        pytest.skip("credentials.json not found - skipping e2e test requiring real authentication")

    # Mock command line arguments to control the number of emails processed
    mock_args = MagicMock()
    mock_args.limit = TEST_EMAIL_LIMIT
    mock_args.prompt = None # Use default prompt logic
    mock_args.interactive = False # Don't use interactive mode for testing
    monkeypatch.setattr(main, "parse_args", lambda: mock_args)

    # Run the main function (will use real inbox and AI clients)
    main.main()

    # Assertions
    # 1. Check if the output file was created
    assert os.path.exists(OUTPUT_FILENAME), f"Output file '{OUTPUT_FILENAME}' was not created."
    logging.info(f"Output file '{OUTPUT_FILENAME}' was created successfully.")
    # 2. Check the content of the output file
    actual_output = []
    try:
        with open(OUTPUT_FILENAME, newline="") as f:
            reader = csv.reader(f)
            actual_output = list(reader)
    except FileNotFoundError:
        pytest.fail(f"Output file '{OUTPUT_FILENAME}' was not found after main() execution.")

    # Check header
    assert len(actual_output) >= 1, "CSV file is empty."
    assert actual_output[0] == EXPECTED_CSV_HEADER, "CSV header is incorrect."

    # Check number of data rows (should match the limit, unless fewer emails were available)
    num_data_rows = len(actual_output) - 1
    assert num_data_rows <= TEST_EMAIL_LIMIT, f"Expected at most {TEST_EMAIL_LIMIT} data rows, but found {num_data_rows}." #noqa: E501
    if num_data_rows == 0:
        logging.warning(f"No emails were processed (limit was {TEST_EMAIL_LIMIT}). Check if the inbox has emails.") #noqa: E501
        # If no emails were processed, we can't check row structure
        return

    # Check data rows for correct structure and types
    for i, row in enumerate(actual_output[1:]):
        assert len(row) == 3, f"Row {i+1} does not have 3 columns."
        email_id, pct_spam_str, tone = row
        assert isinstance(email_id, str), f"Email ID in row {i+1} is not a string."
        assert email_id != "", f"Email ID in row {i+1} should not be empty."
        try:
            pct_spam = int(pct_spam_str)
            assert isinstance(pct_spam, int), f"Percentage in row {i+1} is not an integer."
        except ValueError:
            pytest.fail(f"Percentage '{pct_spam_str}' in row {i+1} could not be converted to an integer.") #noqa: E501
        assert isinstance(tone, str), f"Tone in row {i+1} is not a string."
        assert tone != "", f"Tone in row {i+1} should not be empty."

    # --- No mock calls to assert ---

