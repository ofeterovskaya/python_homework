import csv

# Read the contents of ../csv/employees.csv into a list of lists
with open('../csv/employees.csv', 'r', newline='') as csvfile:
    csv_reader = csv.reader(csvfile)
    data = list(csv_reader)

# Using list comprehension, create a list of employee names (first_name + space + last_name)
# Skip the header row (first item)
employee_names = [f"{row[1]} {row[2]}" for row in data[1:]]
print("Employee names:")
print(employee_names)

# Using list comprehension, create another list with names that contain the letter "e"
names_with_e = [name for name in employee_names if 'e' in name]
print("\nNames containing the letter 'e':")
print(names_with_e)
