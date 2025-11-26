# Task 2: Read a CSV File
import csv
import traceback
import sys
import os
import custom_module
from datetime import datetime

def read_employees():
    """
    Reads ../csv/employees.csv and returns a dict with:
      - "fields": list of column headers
      - "rows": list of data rows (each row is a list of strings)
    """
    data = {}
    rows = []

    try:
        # Open the CSV file for reading
        with open("../csv/employees.csv", "r", newline="") as f:
            reader = csv.reader(f)
            for idx, row in enumerate(reader):
                if idx == 0:
                    data["fields"] = row  # first row is headers
                else:
                    rows.append(row) # remaining rows are data

        data["rows"] = rows
        return data

    except Exception as e:
        # Detailed error output
        trace_back = traceback.extract_tb(e.__traceback__)
        stack_trace = []
        for trace in trace_back:
            stack_trace.append(
                f'File : {trace[0]} , Line : {trace[1]}, Func.Name : {trace[2]}, Message : {trace[3]}'
            )

        print("An exception occurred.")
        print(f"Exception type: {type(e).__name__}")
        message = str(e)
        if message:
            print(f"Exception message: {message}")
        print(f"Stack trace: {stack_trace}")
        sys.exit(1)

employees = read_employees()  # run the function to read the file


# Task 3: Find the Column Index
def column_index(column_name):
    return employees["fields"].index(column_name)


employee_id_column = column_index("employee_id")

# Task 4: Find the Employee First Name

def first_name(row_number):
    """Return the first_name value from employees['rows'][row_number]."""
    idx = column_index("first_name")
    return employees["rows"][row_number][idx]

# Task 5: Find the Employee: a Function in a Function
def employee_find(employee_id):
    """
    Return a list of rows whose employee_id equals the given employee_id (int-like).
    Uses an inner function + filter().
    """
    # inner function — sees employee_id from outside
    def employee_match(row):
        try:
            return int(row[employee_id_column]) == int(employee_id)
        except ValueError:
            # if garbage appears in the csv in id — just don't match such a row
            return False

    matches = list(filter(employee_match, employees["rows"]))
    return matches


# Task 6: Find the Employee with a Lambda
def employee_find_2(employee_id):
    # convert to int just in case, so '1' and 1 work the same
    target = int(employee_id)
    matches = list(filter(lambda row: int(row[employee_id_column]) == target, employees["rows"]))
    return matches


# Task 7: Sort the Rows by last_name Using a Lambda
def sort_by_last_name():
    """
    Sort employees['rows'] in place by the 'last_name' column and return the sorted rows.
    """
    idx = column_index("last_name")
    employees["rows"].sort(key=lambda row: row[idx])  # sorting
    return employees["rows"]
sort_by_last_name()
print(employees)

# Task 8: Create a dict for  an Employee
def employee_dict(row):
    """
    Build a dict for a single employee row.
    Keys come from employees['fields'], values from row.
    Skip the 'employee_id' field.
    """
    headers = employees["fields"]
    id_idx = column_index("employee_id")

    result = {}
    for i, header in enumerate(headers):
        if i == id_idx:
            continue  # skip employee_id
        # in case the row has fewer values than headers
        result[header] = row[i] if i < len(row) else ""
    return result

# Task 9: A dict of dicts, for All Employees
def all_employees_dict():
    """
    Build and return a dict-of-dicts for all employees.
    Keys: employee_id (int).
    Values: dict from employee_dict(row) (без employee_id внутри).
    """
    idx_id = employee_id_column  # index of the employee_id column
    result = {}

    for row in employees["rows"]:
        try:
            emp_id = row[idx_id]
        except (ValueError, TypeError, IndexError):
            # if garbage or incomplete row in CSV — skip
            continue
        result[emp_id] = employee_dict(row)

    return result


# Task 10: Use the os Module
def get_this_value():
    """
    Return the value of the environment variable THISVALUE.
    """
    return os.getenv("THISVALUE")

# Task 11: Creating Your Own Module
def set_that_secret(new_secret):
    """
    Set the secret inside custom_module using its set_secret function.
    """
    custom_module.set_secret(new_secret)

set_that_secret("abracadabra")


# Task 12: Read minutes1.csv and minutes2.csv
def read_csv_file(filename):
    """
    Helper function to read a CSV file and return a dict with:
      - "fields": list of column headers  
      - "rows": list of data rows (each row converted to a tuple)
    """
    data = {}
    rows = []
    
    try:
        csv_path = os.path.join(os.path.dirname(__file__), "..", "csv", filename)
        with open(csv_path, "r", newline="") as file:
            reader = csv.reader(file)
            for idx, row in enumerate(reader):
                if idx == 0:
                    data["fields"] = row  # first row is headers
                else:
                    rows.append(tuple(row))  # convert each row to a tuple
        
        data["rows"] = rows
        return data
        
    except Exception as e:
        # Detailed error output
        trace_back = traceback.extract_tb(e.__traceback__)
        stack_trace = []
        for trace in trace_back:
            stack_trace.append(
                f'File : {trace[0]} , Line : {trace[1]}, Func.Name : {trace[2]}, Message : {trace[3]}'
            )

        print("An exception occurred.")
        print(f"Exception type: {type(e).__name__}")
        message = str(e)
        if message:
            print(f"Exception message: {message}")
        print(f"Stack trace: {stack_trace}")
        sys.exit(1)


def read_minutes():
    """
    Read both minutes1.csv and minutes2.csv files.
    Returns two dicts (minutes1, minutes2), each with fields and rows.
    Rows are converted to tuples.
    """
    minutes1 = read_csv_file("minutes1.csv")
    minutes2 = read_csv_file("minutes2.csv")
    
    return minutes1, minutes2


# Call the function and store the results in global variables
minutes1, minutes2 = read_minutes()


# Task 13: Create minutes_set
def create_minutes_set():
    """
    Create two sets from the rows of minutes1 and minutes2 dicts.
    Combine them into one single set (union operation).
    Returns the resulting set.
    """
    # Convert rows to sets (rows are already tuples, which are hashable)
    set1 = set(minutes1["rows"])
    set2 = set(minutes2["rows"])
    
    # Combine both sets using union operation
    combined_set = set1.union(set2)
    
    return combined_set


# Call the function and store the result in global variable
minutes_set = create_minutes_set()


# Task 14: Convert to datetime
def create_minutes_list():
    """
    Create a list from minutes_set and convert date strings to datetime objects.
    Uses map() to convert each element into a tuple where:
    - First element: name (unchanged)
    - Second element: date string converted to datetime object
    """
    # Convert set to list
    minutes_list_raw = list(minutes_set)
    
    # Use map with lambda to convert date strings to datetime objects
    minutes_list_converted = list(map(lambda x: (x[0], datetime.strptime(x[1], "%B %d, %Y")), minutes_list_raw))
    
    return minutes_list_converted


# Call the function and store the result in global variable
minutes_list = create_minutes_list()


# Task 15: Write Out Sorted List
def write_sorted_list():
    """
    Sort minutes_list by datetime in ascending order, convert dates back to strings,
    and write the sorted data to ./minutes.csv file.
    Returns the converted list.
    """
    # Sort minutes_list in ascending order of datetime (second element of each tuple)
    sorted_list = sorted(minutes_list, key=lambda x: x[1])
    
    # Use map to convert datetime back to string format
    converted_list = list(map(lambda x: (x[0], x[1].strftime("%B %d, %Y")), sorted_list))
    
    # Write to CSV file
    with open("./minutes.csv", "w", newline="") as f:
        writer = csv.writer(f)
        
        # Write header row (fields from minutes1 dict)
        writer.writerow(minutes1["fields"])
        
        # Write data rows
        for row in converted_list:
            writer.writerow(row)
    
    return converted_list


# Call the function
sorted_minutes = write_sorted_list()


if __name__ == "__main__":
    print("Task 2 → employees (raw):")
    print(employees)
    print()  # just for better readability

    print("Task 3 → employee_id_column:", employee_id_column)
    print()

    print("Task 4 → first_name(0):", first_name(0))

    print("Task 5 → employee_find(1):", employee_find(1))
    print("Task 5 → employee_find('2'):", employee_find("2"))
    print()

    print("Task 6 → employee_find_2(1):", employee_find_2(1))
    print("Task 6 → employee_find_2('2'):", employee_find_2("2"))
    print()

    sort_by_last_name()
    print("Task 7 → after sort_by_last_name():")
    print(employees)
    print()

    print("Task 8 → employee_dict(rows[0]) (без employee_id):")
    print(employee_dict(employees["rows"][0]))
    print()

    all_dict = all_employees_dict()
    print("Task 9 → all_employees_dict() keys count:", len(all_dict))
    example_key = list(all_dict.keys())[0]
    print("Task 9 → example:", example_key, "=>", all_dict[example_key])
    print()

    print("Task 10 → get_this_value():", get_this_value())
    print()

    set_that_secret("Code The Dream")
    print("Task 11 → custom_module.secret:", custom_module.secret)
    print()
    
    print("Task 12 → minutes1 dict:")
    print(minutes1)
    print()
    
    print("Task 12 → minutes2 dict:")
    print(minutes2)
    print()
    
    print("Task 13 → minutes_set:")
    print(f"Type: {type(minutes_set).__name__}")
    print(f"Length: {len(minutes_set)}")
    print("First few elements:")
    for i, item in enumerate(sorted(minutes_set)):
        if i < 5:  # show first 5 elements
            print(f"  {item}")
        else:
            break
    print()
    
    print("Task 14 → minutes_list:")
    print(f"Type: {type(minutes_list).__name__}")
    print(f"Length: {len(minutes_list)}")
    print("First few elements:")
    for i, item in enumerate(sorted(minutes_list, key=lambda x: x[1])):
        if i < 5:  # show first 5 elements sorted by date
            print(f"  Name: {item[0]}, Date: {item[1]} (type: {type(item[1]).__name__})")
        else:
            break
    print()
    
    print("Task 15 → write_sorted_list:")
    print(f"Sorted list type: {type(sorted_minutes).__name__}")
    print(f"Sorted list length: {len(sorted_minutes)}")
    print("First few elements from sorted list:")
    for i, item in enumerate(sorted_minutes):
        if i < 5:  # show first 5 elements
            print(f"  Name: {item[0]}, Date: {item[1]}")
        else:
            break
    
    # Check if file was created
    import os
    if os.path.exists("./minutes.csv"):
        print("✓ File './minutes.csv' created successfully!")
        # Read and show first few lines
        with open("./minutes.csv", "r") as f:
            lines = f.readlines()
            print(f"File contains {len(lines)} lines (including header)")
            print("First few lines:")
            for i, line in enumerate(lines):
                if i < 6:  # show header + first 5 data rows
                    print(f"  {line.strip()}")
                else:
                    break
    else:
        print("✗ File './minutes.csv' was not created!")
    print()
