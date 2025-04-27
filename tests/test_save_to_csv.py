import os
import csv
from src.save_to_csv import save_results_to_csv

def test_save_results_to_csv(tmp_path):
    output_path = tmp_path / "output.csv"
    sample_data = [
        {"mail_id": "email_001", "Pct_spam": 95.5},
        {"mail_id": "email_002", "Pct_spam": 10.2}
    ]
    save_results_to_csv(sample_data, output_path)

    assert output_path.exists()

    with open(output_path, newline='') as f:
        reader = list(csv.DictReader(f))
        assert len(reader) == 2
        assert reader[0]["mail_id"] == "email_001"
        assert "Pct_spam" in reader[0]