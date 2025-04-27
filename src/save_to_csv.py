import csv

def save_results_to_csv(results, output_path):
    """Save a list of dictionaries (mail_id and Pct_spam) to a CSV file."""
    with open(output_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["mail_id", "Pct_spam"])
        writer.writeheader()
        writer.writerows(results)