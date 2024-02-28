from view.ssis_gui import SSISWindow, AddStudentWindow, AddProgramWindow
from model.student import Student, Program
from model.ssis import SSIS
from tkinter import Menu, messagebox, END, dialog

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
            self.ssis.add_program(Program(
                code.upper().strip(),
                name.upper().strip()
            ))
            
            self.gui.destroy()
        
        else:
            invalid_code_message = f'"{code.upper().strip()}" is not a valid program code.' * (not pcv)
            invalid_name_message = f'"{name.upper().strip()}" is not a valid program name.' * (not pnv)
            
            messagebox.showerror('Invalid Input(s)', f'{invalid_code_message}\n{invalid_name_message}'.strip())
    
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
        self.gui.add_program_button.config(command=self.add_program_button_pressed)

    def save_button_pressed(self) -> None:
        self.ssis.save_programs()
        self.ssis.save_students()
    
    def add_program_button_pressed(self) -> None:
        add_p_gui = AddProgramWindow(self.gui)
        
        AddProgramController(self.ssis, add_p_gui)