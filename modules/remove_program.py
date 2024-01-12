## Imports
# Standard
import csv

def populate_listbox(
        csv_file_path,  
    ):
    """
    Opens the csv file, collects the file paths
    and appends them to a list. It then returns that list.
    """
    data = []
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        # Read the header row.
        next(csv_reader)

        for row in csv_reader:
            file_string = f"{row[0]}, {row[5]}"
            data.append(file_string)

    return data

def remove_selected_program(
        selected_program,
        csv_file_path
    ):
    """
    Finds the selected program in the csv.
    """
    data = []
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        
        # Read the header row.
        header_row = next(csv_reader)
        data.append(header_row)
        
        for row in csv_reader:
            file_string = f"{row[0]}, {row[5]}"
            if selected_program != file_string:
                data.append(row)
    
    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)
    

