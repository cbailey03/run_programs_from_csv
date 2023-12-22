## Imports
# Standard
import csv
import subprocess
import os
from datetime import datetime
# Tkinter 
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
# Local
from execute_program import read_csv_and_execute
from add_new_program import add_new_program_to_csv

current_directory = os.getcwd()
sub_directory = 'input_csv'
csv_file_name = 'input.csv'
csv_file_path = os.path.join(current_directory, sub_directory, csv_file_name)
program_file_path = ''

class RunFromCSV:
    """
    Overall class to manage program assets and
    behavior.
    """

    def __init__(self):
        """
        Initialize the program and create
        resources.
        """
        self.csv_file_path = self._get_csv()
        self.new_program = ''
        self.execution = ''
        self.root_window = None
        self.file_options_window = None

    def _get_csv(self):
        """
        Get's the csv that the programs are stored in.
        """
        current_directory = os.getcwd()
        sub_directory = 'input_csv'
        csv_file_name = 'input.csv'
        csv_file_path = os.path.join(
            current_directory, 
            sub_directory, 
            csv_file_name
        )
        return csv_file_path
    
    def run_program(self):
        """
        Start the main loop for the program.
        """
        self.root_window = self._root_window()
        self.root_window.mainloop()

    def _root_window(self):
        """
        Set the attributes for the main
        tkinter window.
        """
        root = Tk()
        #Define the window.
        root.title("Program Scheduler")
        label1=Label(root, text='Add a new program to execute:', font=('Aerial',10))
        label1.pack()
        button1=Button(root, text='Select Program', command=self._add_program_window)
        button1.pack()
        rpg_button=Button(root, text='Execute Programs', command=self._execute_programs)
        rpg_button.pack()
        
        return root
    
    def _execute_programs(self):
        """
        Calls the read_csv_and_execute function.
        """
        read_csv_and_execute(self.csv_file_path)

    # Function to open another window with file options
    def _add_program_window(self):
        self.file_options_window = Toplevel(self.root_window)
        self.file_options_window.title("File Options")

        label2=Label(
            self.file_options_window, 
            text='Add a Program', 
            font=('Aerial',10)
        )
        label2.pack()

        choose_file = Button(
            self.file_options_window, 
            text='Choose file',
            command=self._load_file_path
        )
        choose_file.pack()


        label3=Label(
            self.file_options_window, 
            text='Set execution interval', 
            font=('Aerial',10)
        )
        label3.pack()
        
        def _set_exec(event):
            self.execution = execution.get()
        
        execution_style = StringVar()
        execution = ttk.Combobox(self.file_options_window, textvariable=execution_style)
        execution['values'] = ('Hourly', 'Daily', 'Weekly', 'None')
        execution.state(["readonly"])
        execution.bind("<<ComboboxSelected>>", _set_exec)
        execution.pack()

        label4=Label(
            self.file_options_window, 
            text='Submit the new program', 
            font=('Aerial',10)
        )
        label4.pack()

        submit = Button(
            self.file_options_window,
            text="Submit",
            command=self._submit_new_program
        )
        submit.pack()
       
    def _load_file_path(self):
        """
        Opens a tkinter filedialog box in order to load a program.
        """
        file_path = filedialog.askopenfilename(title="Select a python program")
        self.new_program = file_path
        selected_label_text = f"Selected file: {self.new_program}"
        selected_label=Label(
            self.file_options_window, 
            text=selected_label_text, 
            font=('Aerial',10)
        )
        selected_label.pack()
        self.file_options_window.update()

    def _submit_new_program(self):
        """
        Submits a new program to be stored in the csv. 
        """
        print(self.execution)
        add_new_program_to_csv(
            self.csv_file_path,
            self.new_program,
            self.execution
        )
    
    

if __name__ == '__main__':
    # Make a program instance, and run.
    rfc = RunFromCSV()
    rfc.run_program()

    

    