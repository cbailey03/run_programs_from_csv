## Imports
# Standard
import csv
import uuid

def add_new_program_to_csv(
        csv_file_path,
        program_file_path, 
        execution_style,    
    ):
    """
    Opens the csv file, and adds a new program to
    the list of executions.
    """
    data = []
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            data.append(row)

    new_list = build_new_program_list(
        program_file_path,
        execution_style
    )
    data.append(new_list)

    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)
    
def build_new_program_list(
        program_file_path, 
        execution_style
    ):
    """
    Will build out the list that is going to
    be written back to the csv based on the 
    execution style.
    """
    new_list = []
    if execution_style == "None":
        new_list = [program_file_path, "no", "no", "no", "", generate_unique_id()]
        return new_list
    elif execution_style == "Hourly":
        new_list = [program_file_path, "yes", "no", "no", "", generate_unique_id()]
        return new_list
    elif execution_style == "Daily":
        new_list = [program_file_path, "no", "yes", "no", "", generate_unique_id()]
        return new_list
    else:
        new_list = [program_file_path, "no", "no", "yes", "", generate_unique_id()]
        return new_list


def generate_unique_id():
    unique_id = uuid.uuid4()
    return str(unique_id)