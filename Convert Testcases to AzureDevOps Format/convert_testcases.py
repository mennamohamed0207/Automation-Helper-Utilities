import csv
import re

input_path = "./input.csv"
output_path = "output.csv"

# The header of the target CSV (reference format)
OUTPUT_HEADER = [
    "ID",
    "Work Item Type",
    "Title",
    "Test Step",
    "Step Action",
    "Step Expected",
    "Area Path",
    "Assigned To",
    "State",
]


def flush_case(case):
    """
    Convert one collected test case into the reference CSV format.
    """
    rows = []
    # Test Case header
    rows.append(
        [case["id"], "Test Case", case["title"], "", "", "", "main", "", "Design"]
    )

    # Collect all steps (preconditions + actions)
    allSteps = case["preconditions"] + [s["action"] for s in case["steps"]]
    lengthOfSteps = len(allSteps)

    step_num = 1

    # Preconditions first
    for pre in case["preconditions"]:
        if pre != "":
            rows.append(["", "", "", str(step_num), pre, "", "", "", ""])
            step_num += 1

    # Then actual steps
    for i, s in enumerate(case["steps"], start=1):
        # print(s.get("action", ""))
        if s != "":
            if step_num < lengthOfSteps:
                rows.append(["", "", "", str(step_num), s["action"], "", "", "", ""])
            elif s != "":  # last step includes expected result
                rows.append(
                    [
                        "",
                        "",
                        "",
                        str(step_num),
                        s["action"],
                        s.get("expected", ""),
                        "",
                        "",
                        "",
                    ]
                )
            step_num += 1

    return rows


def safe_open_csv(input_file):
    try:
        return open(input_file, newline="", encoding="utf-8")
    except UnicodeDecodeError:
        return open(input_file, newline="", encoding="latin-1")


def parse_input_file(input_file):
    """
    Parse the original CSV file into structured test cases.
    """
    with safe_open_csv(input_file) as f:
        reader = list(csv.reader(f))

    rows = reader[1:]  # Skip header
    cases, case = [], None

    for row in rows:
        row += [""] * (8 - len(row))  # Ensure row has at least 8 fields
        api_name, case_id, title, precond, step, expected, status, *_ = row
        if case_id:  # New test case starts
            if case:
                cases.append(case)
            case = {
                "id": "",
                "title": (title or "").strip(),
                "status": "Design",
                "preconditions": [],
                "steps": [],
                "expected": [],
            }
        if case:  # Continuation of the current test case
            if precond:
                cleaned = precond
                if precond.startswith("1-"):
                    cleaned = re.sub(
                        r"^\d+\s*-\s*|\d+\s*-\s*", "", precond, flags=re.MULTILINE
                    )
                preconds = cleaned.split("\n")
                case["preconditions"].extend(preconds)
            if step:
                # cleaned = re.sub(r"^\d+\s*-\s*|\d+\s*-\s*", "", step, flags=re.MULTILINE)
                detailedSteps = re.split(r"\d+\s*-\s+", step)
                finalStep = ""
                for s in detailedSteps:
                    cleaned = re.sub(
                        r"^\d+\s*-\s*|\d+\s*-\s*", "", s, flags=re.MULTILINE
                    )
                    # print(cleaned)
                    # print(step)
                    if "URL" in cleaned:
                        if cleaned.startswith("Navigate"):
                            pass
                        else:
                            cleaned = "Navigate to " + cleaned
                    finalStep += cleaned
                    if cleaned != "":
                        case["steps"].append(
                            {"action": cleaned.strip(), "expected": expected.strip()}
                        )
            if expected:
                # print("/////////////")
                print(expected)

    if case:
        cases.append(case)

    return cases


def write_output_file(output_file, cases):
    """
    Write the converted test cases to a new CSV file.
    """
    output_rows = []
    for c in cases:
        output_rows.extend(flush_case(c))

    # Clean up newlines inside cells
    output_rows_cleaned = [
        [
            (
                cell.replace("\n", " ").replace("\r", " ")
                if isinstance(cell, str)
                else cell
            )
            for cell in row
        ]
        for row in output_rows
    ]

    # Write to CSV
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(OUTPUT_HEADER)
        writer.writerows(output_rows_cleaned)

    print(f"Converted file saved to {output_file}")


if __name__ == "__main__":
    cases = parse_input_file(input_path)
    write_output_file(output_path, cases)
