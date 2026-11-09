
import csv
from pathlib import Path


# -----------------------------------
# 1. Function with *args and **kwargs
# -----------------------------------

def calculate_bonus(salary, rate=0.1, *extras, **options):
    """
    Calculate employee bonus.
    Bonus = salary * rate + sum of extras.
    If cap is provided, bonus cannot exceed cap.
    """

    bonus = salary * rate + sum(extras)

    if "cap" in options:
        bonus = min(bonus, options["cap"])

    return bonus


# -----------------------------------
# 2. Decorator
# -----------------------------------

def log_call(func):
    def wrapper(*args, **kwargs):
        print("Calling get_details")
        return func(*args, **kwargs)

    return wrapper


# -----------------------------------
# 3. Employee Class
# -----------------------------------

class Employee:

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def get_details(self):
        return f"{self.name} - {self.salary}"

    @property
    def annual_salary(self):
        return self.salary * 12


# -----------------------------------
# 4. Manager Class (Inheritance)
# -----------------------------------

class Manager(Employee):

    def __init__(self, name, salary, team_size):
        super().__init__(name, salary)
        self.team_size = team_size

    @log_call
    def get_details(self):
        return (
            f"{self.name} - {self.salary} "
            f"- Team Size: {self.team_size}"
        )


# -----------------------------------
# 5. Read CSV and Categorize Salaries
# -----------------------------------

def read_employees():
    file_path = Path(__file__).parent / "employees.csv"

    with file_path.open(mode="r", newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for employee in reader:

            name = employee["name"]
            department = employee["department"]
            salary = int(employee["salary"])

            if salary < 50000:
                category = "Low"
            elif salary < 70000:
                category = "Medium"
            else:
                category = "High"

            print(f"{name} - {category} Salary")


# -----------------------------------
# 6. Main Function
# -----------------------------------

def main():

    # Read employee information from CSV
    read_employees()

    print()

    # Create a Manager object
    manager = Manager("Divya", 75000, 5)

    # Call overridden get_details()
    print(manager.get_details())

    print()

    # Demonstrate bonus calculation
    bonus = calculate_bonus(50000, 0.1, 1000, 2000)
    print(f"Employee Bonus: {bonus}")

    # Demonstrate bonus cap
    capped_bonus = calculate_bonus(
        50000, 0.1, 1000, 2000, cap=4000
    )
    print(f"Capped Bonus: {capped_bonus}")

    # Demonstrate annual salary property
    employee = Employee("Arun", 30000)
    print(f"Annual Salary: {employee.annual_salary}")


# -----------------------------------
# 7. Program Entry Point
# -----------------------------------

if __name__ == "__main__":
    main()
