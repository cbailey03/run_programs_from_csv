## Imports
# Standard
import csv
import subprocess
import os
import time
from datetime import datetime
import threading

def execute_python_program(file_path):
    """
    Tries to open a subprocess of the python file given.
    """
    try:
        subprocess.run(["python", file_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing {file_path}: {e}")

def thread_read_csv_and_execute(csv_file_path):
    """
    Opens the csv file, skips the header, reads each row.
    If the row and column 0 are populated, execute the file path.
    """
    active = True
    while active == True:    
        if threading.main_thread().is_alive() == False:
            break
        get_and_run_programs(csv_file_path)
        
        time.sleep(30)


def get_and_run_programs(csv_file_path):
    """
    Gets the list of programs and runs them.
    """
    # Get the current date.
    current_date = datetime.today()
    data = []

    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        
        # Read the header row.
        header_row = next(csv_reader)
        data.append(header_row)
        
        for row in csv_reader:
            if row:
                # Get the program file path, and store the flag.
                python_program_path = row[0]
                program_path_flag = is_valid_file_path(python_program_path)
                # Check to see if the file path is valid.
                if program_path_flag == False: 
                    print(f"{python_program_path} is not a valid file path.")
                    print("Please change this in the settings.")
                    continue
                # Look for the hourly setting, and store the flag.
                hourly_setting = row[1]
                hourly_flag = is_setting_true(hourly_setting)
                # Look for the daily setting, and store the flag.
                daily_setting = row[2]
                daily_flag = is_setting_true(daily_setting)
                # Look for the weekly setting, and store the flag.
                weekly_setting = row[3]
                weekly_flag = is_setting_true(weekly_setting)
                # Get the last execution time.
                last_execution = row[4]
                # Flag to see if the script was executed for the hour
                hourly_execution_flag = hourly_execution(
                    current_date=current_date, 
                    hourly_flag=hourly_flag, 
                    program=python_program_path, 
                    last_execution=last_execution
                )
                # Flag to see if the script was executed for the day
                daily_execution_flag = daily_execution(
                    current_date=current_date,
                    daily_flag=daily_flag, 
                    program=python_program_path,
                    last_execution=last_execution, 
                )
                # Flag to see if the script was executed for the week.
                weekly_execution_flag = weekly_execution(
                    current_date=current_date,
                    weekly_flag=weekly_flag, 
                    program=python_program_path,
                    last_execution=last_execution,
                )
                execution_time = write_execution_time(
                    hourly_execution_flag,
                    daily_execution_flag,
                    weekly_execution_flag,
                    current_date,
                    last_execution,
                )
                row[4] = execution_time
                data.append(row)
    try:
        with open(csv_file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)
    except:
        pass

def is_valid_file_path(path):
    """
    Checks to see if a given input is a valid
    file path.
    """
    if not os.path.exists(path):
        return False
    else:
        return True

def is_setting_true(setting):
    """
    Checks to see if a given setting in 
    the csv is set to yes or no.
    """
    if setting == "yes":
        return True
    else:
        return False

def write_execution_time(
        hourly_execution_flag,
        daily_execution_flag,
        weekly_execution_flag,
        current_date,
        last_execution
    ):
    """
    This takes the execution flags, csv_row, current_date, 
    and current_date. If an execution flag is true, it will
    write the current date and time to the last_execution column.
    """
    execution_time = current_date.strftime("%Y-%m-%d_%H")
    if hourly_execution_flag == True:
        return execution_time
    elif daily_execution_flag == True:
        return execution_time
    elif weekly_execution_flag == True:
        return execution_time
    else:
        return last_execution


def hourly_execution(
        current_date, 
        hourly_flag, 
        program, 
        last_execution
    ):
    """
    Checks to see if the hourly execution flag is set
    on the csv. If it is, compare the time with the current
    clock time to see if the script needs to run. 
    Returns true if the program executes. Else returns False.
    """
    execution_times = [
        "00", "01", "02", "03", "04", "05",
        "06", "07", "08", "09", "10", "11",
        "12", "13", "14", "15", "16", "17",
        "18", "19", "20", "21", "22", "23", 
        ]

    if hourly_flag == True:
        if current_date.strftime("%H") in execution_times:
            if current_date.strftime("%Y-%m-%d_%H") != last_execution:
                execute_python_program(program)
                return True
    else:
        return False

def daily_execution(
        current_date,
        daily_flag, 
        program,
        last_execution, 
    ):
    """
    Checks to see if the daily execution is set
    on the csv. If it is, compare the date with the current
    date to see if the script needs to run. 
    Returns true if the program executes. Else returns false.
    """
    if last_execution:
        last_date_executed = last_execution.split("_")[0]
    else:
        last_date_executed = last_execution
    
    if daily_flag == True:
        if current_date.strftime("%Y-%m-%d") != last_date_executed:
            execute_python_program(program)
            return True
    else:
        return False
    
def weekly_execution(
        current_date,
        weekly_flag,
        program,
        last_execution,
    ):
    """
    Checks to see if the weekly execution is set on the csv.
    If it is, compare the date with the current date to
    see if they are 7 days apart. If they are, the script will run.
    Returns true if the script runs, false if it does not run.
    """
    if last_execution:
        last_date_executed = last_execution.split("_")[0]
        date_obj = datetime.strptime(last_date_executed, "%Y-%m-%d")
    else:
        execute_python_program(program)
        return True
    
    if weekly_flag == True:
        days_diff = (current_date - date_obj).days
        if days_diff >= 7:
            execute_python_program(program)
            return True
        else:
            return False
    else:
        return False
