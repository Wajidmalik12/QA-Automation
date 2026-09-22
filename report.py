import csv
from datetime import datetime


def generate_csv_report(tests, results, filename=None):

    if filename is None:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"qa_report_{timestamp}.csv"

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(filename, "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        # =========================
        # LLM GENERATED TEST PLAN
        # =========================

        writer.writerow(["LLM GENERATED TEST PLAN"])
        writer.writerow([
            "Test Name",
            "Type",
            "Target",
            "Expected"
        ])

        for test in tests:

            writer.writerow([
                test["name"],
                test["type"],
                test["target"],
                test["expected"]
            ])

        # Empty space between sections
        writer.writerow([])
        writer.writerow([])

        # =========================
        # EXECUTION RESULTS
        # =========================

        writer.writerow(["PLAYWRIGHT EXECUTION RESULTS"])
        writer.writerow([
            "Test Name",
            "Type",
            "Status",
            "Actual Result",
            "Timestamp"
        ])

        for test, result in zip(tests, results):

            writer.writerow([
                test["name"],
                test["type"],
                result["status"],
                result["message"],
                timestamp
            ])

    print(f"\nCSV report generated: {filename}")