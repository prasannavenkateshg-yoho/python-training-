import csv
import json
import logging
import pymupdf

from pathlib import Path
from typing import List, Optional, Union

from openpyxl import Workbook, load_workbook


# -----------------------------------------
# 1. Logging Configuration
# -----------------------------------------

logging.basicConfig(
    level=logging.ERROR,
    format="%(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent


# -----------------------------------------
# 2. Read Employees from CSV
# -----------------------------------------

def read_employees() -> List[dict]:

    file_path = BASE_DIR / "employees.csv"
    employees: List[dict] = []

    with file_path.open(
        mode="r",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            employee = {
                key.strip().lower(): value.strip()
                for key, value in row.items()
                if key is not None and value is not None
            }

            employee["salary"] = int(employee["salary"])

            employees.append(employee)

    return employees


# -----------------------------------------
# 3. Write Employees to JSON
# -----------------------------------------

def write_employees_json(
    employees: List[dict]
) -> None:

    file_path = BASE_DIR / "employees.json"

    with file_path.open(
        mode="w",
        encoding="utf-8"
    ) as file:

        json.dump(
            employees,
            file,
            indent=4
        )


# -----------------------------------------
# 4. Write High Earners to CSV
# -----------------------------------------

def write_high_earners(
    employees: List[dict]
) -> int:

    high_earners = [
        employee
        for employee in employees
        if employee["salary"] > 50000
    ]

    file_path = BASE_DIR / "high_earners.csv"

    with file_path.open(
        mode="w",
        newline="",
        encoding="utf-8"
    ) as file:

        fieldnames = [
            "name",
            "department",
            "salary"
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(high_earners)

    return len(high_earners)


# -----------------------------------------
# 5. Create Excel File Using openpyxl
# -----------------------------------------

def create_salary_excel(
    employees: List[dict]
) -> int:

    file_path = BASE_DIR / "salary.xlsx"

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Employee Salaries"

    # Write column headings
    sheet.append([
        "Name",
        "Department",
        "Salary"
    ])

    # Write employee records
    for employee in employees:

        sheet.append([
            employee["name"],
            employee["department"],
            employee["salary"]
        ])

    workbook.save(file_path)

    # Read Excel file back
    loaded_workbook = load_workbook(file_path)

    loaded_sheet = loaded_workbook["Employee Salaries"]

    # Count employee rows (excluding header)
    row_count = loaded_sheet.max_row - 1

    loaded_workbook.close()

    return row_count


# -----------------------------------------
# 6. Extract Text from PDF Using PyMuPDF
# -----------------------------------------

def extract_pdf_text(
    pdf_path: Union[int, str, Path]
) -> str:

    file_path = Path(pdf_path)

    with pymupdf.open(file_path) as document:

        if len(document) == 0:
            return ""

        # Extract text from first page
        text = document[0].get_text()

        return text[:100]


# -----------------------------------------
# 7. Read JSON File with Exception Handling
# -----------------------------------------

def read_file(
    path: Union[int, str, Path]
) -> Optional[dict]:

    file_path = Path(path)

    try:

        with file_path.open(
            mode="r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

            if isinstance(data, dict):
                return data

            return None

    except FileNotFoundError:

        logger.error(
            "File not found: %s",
            file_path.name
        )

    except json.JSONDecodeError:

        logger.error(
            "Invalid JSON file: %s",
            file_path.name
        )

    return None


# -----------------------------------------
# 8. Find Employee by Name
# -----------------------------------------

def find_employee(
    name: str
) -> Optional[dict]:

    employees = read_employees()

    for employee in employees:

        if employee["name"].lower() == name.lower():

            return employee

    return None


# -----------------------------------------
# 9. Salary Type Conversion
# -----------------------------------------

def convert_salary(
    salary: Union[int, str]
) -> int:

    return int(salary)


# -----------------------------------------
# 10. Main Function
# -----------------------------------------

def main() -> None:

    # Read employee records
    employees = read_employees()

    # Write employees.json
    write_employees_json(employees)

    # Write high earners CSV
    high_earners_count = write_high_earners(employees)

    print(
        f"Rows read: {len(employees)} | "
        f"High earners written: {high_earners_count}"
    )

    # Create and read Excel file
    excel_rows = create_salary_excel(employees)

    print(
        f"salary.xlsx created and read back: "
        f"{excel_rows} rows"
    )

    # Extract PDF text if sample.pdf exists
    pdf_path = BASE_DIR / "sample.pdf"

    if pdf_path.exists():

        pdf_text = extract_pdf_text(pdf_path)

        print("PDF first 100 characters:")
        print(pdf_text)

    # Demonstrate find_employee()
    employee = find_employee("Divya")

    if employee:
        print("Employee found:", employee)

    # Demonstrate salary conversion
    salary = convert_salary("75000")

    # Demonstrate file-not-found logging
    read_file(BASE_DIR / "missing.txt")


# -----------------------------------------
# 11. Program Entry Point
# -----------------------------------------

if __name__ == "__main__":
    main()
