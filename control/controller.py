from typing import Literal
from view.ssis_gui import SSISWindow, AddStudentWindow, AddProgramWindow
from model.student import Student, Program
from model.ssis import SSIS
from tkinter import Menu, messagebox, END

class AddProgramController:
    def __init__(self, ssis: SSIS, gui: AddProgramWindow) -> None:
        self.ssis = ssis
        self.gui = gui
        
        self.set_actions()
        self.set_validations()
    
    def set_actions(self) -> None:
        self.gui.add_program_button.config(command=self.add_program_button_pressed)
        
    def set_validations(self) -> None:
        self.program_code_validation()
        self.program_name_validation()
        
    def add_program_button_pressed(self) -> None:
        code = self.gui.program_code_entry.get()
        name = self.gui.program_name_entry.get()
        
        if (pcv := Program.valid_program_code(code)) and (pnv := Program.valid_program_name(name)):
            self.ssis.add_program(program := Program(
                code.upper().strip(),
                name.upper().strip()
            ))
            
            messagebox.showinfo(
                'Program Added Successfully!',
                f'Program with:\n\
                    \tCode "{program.code}",\n\
                    \tName {program.name}\n\
                    added successfully!'
            )
            
            self.gui.destroy()
        
        else:
            invalid_code_message = f'"{code.upper().strip()}" is not a valid program code.' * (not pcv)
            invalid_name_message = f'"{name.upper().strip()}" is not a valid program name.' * (not pnv)
            
            messagebox.showerror(
                'Invalid Input(s)', 
                f'{invalid_code_message}\n{invalid_name_message}'.strip()
            )
    
    def program_code_validation(self) -> None:
        validate_cmd = self.gui.register(lambda change: change.isalpha() or change in '()', subst=str.upper)
        
        self.gui.program_code_entry.config(validate='key', validatecommand=(validate_cmd, '%S'))
        
    def program_name_validation(self) -> None:
        validate_cmd = self.gui.register(lambda change: change.isalpha() or change in '()')
        
        self.gui.program_name_entry.config(validate='key', validatecommand=(validate_cmd, '%S'))

class AddStudentController:
    def __init__(self, ssis: SSIS, gui: AddStudentWindow) -> None:
        self.ssis = ssis
        self.gui = gui
        
        self.set_actions()
        
    def set_actions(self) -> None:
        self.gui.add_program_button.config(command=self.add_program_button_pressed)
        self.gui.add_student_button.config(command=self.add_student_button_pressed)
    
    def add_program_button_pressed(self) -> None:
        add_p_gui = AddProgramWindow(self.gui)
        
        AddProgramController(self.ssis, add_p_gui)
    
    def add_student_button_pressed(self) -> None:
        valid_i = Student.valid_id(id := self.get_id())
        valid_n = Student.valid_name(name := self.get_name())
        valid_y = Student.valid_year(year := self.get_year())
        valid_g = Student.valid_gender(gender := self.get_gender())
        valid_p = len(program_code := self.get_program_code()) > 0
        
        if valid_i and valid_n and valid_y and valid_g and valid_p:
            self.ssis.add_student(student := Student(
                id=id,
                name=name,
                year=year,
                gender=gender,
                program_code=program_code
            ))
            
            messagebox.showinfo(
                'Student Added Successfully!',
                f'Student "{student.id}" with:\n\
                    \tName "{student.name_formatted}",\n\
                    \tYear "{student.year}",\n\
                    \tGender "{student.gender}",\n\
                    \tProgram Code "{student.program_code}"\n\
                    added successfully!'
            )
            
            self.gui.destroy()
        
        else:
            invalid_id_message = f'ID "{id}" is invalid.' * (not valid_i)
            invalid_name_message = f'Surname and First Name must not be blank.' * (not valid_n)
            invalid_year_message = f'Year "{year}" is invalid.' * (not valid_y)
            invalid_gender_message = f'Gender is invalid.' * (not valid_g)
            invalid_program_message = f'Program cannot be blank.' * (not valid_p)
            
            messagebox.showerror(
                'Invalid Student Input(s)',
                f'{invalid_id_message}\n\
                  {invalid_name_message}\n\
                  {invalid_program_message}\n\
                  {invalid_gender_message}\n\
                  {invalid_program_message}'.strip()
            )
    
    def get_id(self) -> str:
        return self.gui.id_entry.get().strip()
    
    def get_name(self) -> tuple[str, str, str, str]:
        surname = self.gui.surname_entry.get().upper().strip()
        firstname = self.gui.firstname_entry.get().upper().strip()
        middlename = self.gui.middlename_entry.get().upper().strip()
        suffix = self.gui.suffix_entry.get().upper().strip()
        
        return (surname, firstname, middlename, suffix)
    
    def get_year(self) -> int:
        return int(self.gui.year_entry.get().strip())
    
    def get_gender(self) -> str:
        return self.gui.gender_combobox.get()
    
    def get_program_code(self) -> str:
        return self.gui.program_combobox.get().split('|')[0].strip()

class SSISController:
    def __init__(self, ssis: SSIS, gui: SSISWindow) -> None:
        self.ssis = ssis
        self.gui = gui
        
        self.load_programs()
        self.load_students()
        
        self.set_actions()
    
    def load_programs(self) -> None:
        self.gui.program_list.delete(*self.gui.program_list.get_children())
        
        for program in sorted(self.ssis.programs.values(), key=lambda program: program.code):
            self.gui.program_list.insert(
                '',
                index=END,
                iid=program.code,
                values=(
                    program.code,
                    program.name
                )
            )
    
    def load_students(self) -> None:
        self.gui.student_list.delete(*self.gui.student_list.get_children())
        
        for student in sorted(self.ssis.students.values(), key=lambda student: student.id):
            self.gui.student_list.insert(
                '',
                index=END,
                iid=student.id,
                values=(
                    student.id,
                    student.name_formatted,
                    student.year,
                    student.gender,
                    self.ssis.programs.get(student.program_code, None)
                )
            )
            
    def set_actions(self) -> None:
        self.gui.save_button.config(command=self.save_button_pressed)
        self.gui.add_student_button.config(command=self.add_student_button_pressed)
        self.gui.add_program_button.config(command=self.add_program_button_pressed)

    def save_button_pressed(self) -> None:
        self.ssis.save_programs()
        self.ssis.save_students()
    
    def add_student_button_pressed(self) -> None:
        add_s_gui = AddStudentWindow(self.gui)
        
        AddStudentController(self.ssis, add_s_gui)
    
    def add_program_button_pressed(self) -> None:
        add_p_gui = AddProgramWindow(self.gui)
        
        AddProgramController(self.ssis, add_p_gui)