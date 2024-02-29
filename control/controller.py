from __future__ import annotations
import stat
from typing import Literal, override
from model import student
from view.ssis_gui import SSISWindow, AddStudentWindow, AddProgramWindow
from model.student import Student, Program
from model.ssis import SSIS, DuplicateProgramError, DuplicateStudentError
from tkinter import Menu, messagebox, END

class AddProgramController:
    def __init__(
            self, 
            ssis: SSIS, 
            gui: AddProgramWindow,
            parent_controller: SSISController,
            add_student_controller: AddStudentController | None = None
        ) -> None:
        self.ssis = ssis
        self.gui = gui
        self.parent_controller = parent_controller
        self.add_student_controller = add_student_controller
        
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
            try:
                self.ssis.add_program(program := Program(
                    code.upper().strip(),
                    name.upper().strip()
                ))
            
            except DuplicateProgramError:
                messagebox.showerror(
                    'Program Aleady Exists',
                    f'Program "{self.ssis.get_program_by_code(code)}" already exists.'
                )
                
                if messagebox.askyesno('Program Aleady Exists', f'Do you want to edit the existing program instead?'):
                    EditProgramController(
                        self.ssis, 
                        AddProgramWindow(self.gui.master), 
                        self.parent_controller, 
                        code, 
                        self.add_student_controller
                    )
                    self.gui.destroy()
                
                return
            
            messagebox.showinfo(
                'Program Added Successfully!',
                f'Program with:\n\tCode "{program.code}",\n\tName {program.name}\nadded successfully!'
            )
            
            self.parent_controller.load_programs()
            
            if self.add_student_controller is not None:
                self.add_student_controller.load_programs()
                
            self.gui.destroy()
        
        else:
            invalid_code_message = f'"{code.upper().strip()}" is not a valid program code.' * (not pcv)
            invalid_name_message = f'"{name.upper().strip()}" is not a valid program name.' * (not pnv)
            
            messagebox.showerror(
                'Invalid Input(s)', 
                f'{invalid_code_message}\n{invalid_name_message}'.strip()
            )
    
    def program_code_validation(self) -> None:
        validate_cmd = self.gui.register(lambda change: change.isalpha() or change in '()' or change.isspace())
        
        self.gui.program_code_entry.config(validate='key', validatecommand=(validate_cmd, '%S'))
        
    def program_name_validation(self) -> None:
        validate_cmd = self.gui.register(lambda change: change.isalpha() or change in '()' or change.isspace())
        
        self.gui.program_name_entry.config(validate='key', validatecommand=(validate_cmd, '%S'))

class EditProgramController(AddProgramController):
    def __init__(
        self, 
        ssis: SSIS, 
        gui: AddProgramWindow, 
        parent_controller: SSISController, 
        program_code: str, 
        add_student_controller: AddStudentController | None = None
    ) -> None:
        super().__init__(ssis, gui, parent_controller, add_student_controller)
        
        self.program = self.ssis.get_program_by_code(program_code)
        
    def __load_data(self) -> None:
        self.gui.title('Edit Program')
        self.gui.add_program_button.config(text='Edit Program')
        
        self.gui.program_code_entry.insert(0, self.program.code)
        self.gui.program_name_entry.insert(0, self.program.name)
    
    @override
    def add_program_button_pressed(self) -> None:
        code = self.gui.program_code_entry.get().upper().strip()
        name = self.gui.program_name_entry.get().upper().strip()
        
        if (pcv := Program.valid_program_code(code)) and (pnv := Program.valid_program_name(name)):
            self.program.code = code
            self.program.name = name
            
            messagebox.showinfo(
                'Program Edited Successfully!',
                f'Program with:\n\tCode "{self.program.code}",\n\tName {self.program.name}\nadded successfully!'
            )
            
            self.parent_controller.load_programs()
            
            if self.add_student_controller is not None:
                self.add_student_controller.load_programs()
                
            self.gui.destroy()
        
        else:
            invalid_code_message = f'"{code.upper().strip()}" is not a valid program code.' * (not pcv)
            invalid_name_message = f'"{name.upper().strip()}" is not a valid program name.' * (not pnv)
            
            messagebox.showerror(
                'Invalid Input(s)', 
                f'{invalid_code_message}\n{invalid_name_message}'.strip()
            )

class AddStudentController:
    def __init__(
        self, 
        ssis: SSIS, 
        gui: AddStudentWindow, 
        parent_controller: SSISController
    ) -> None:
        self.ssis = ssis
        self.gui = gui
        self.parent_controller = parent_controller
        
        self.set_actions()
        
        self.load_genders()
        self.load_programs()
    
    def load_genders(self) -> None:
        self.gui.gender_combobox.config(
            state='readonly',
            values=Student.VALID_GENDER_OPTIONS
        )
    
    def load_programs(self) -> None:
        self.gui.program_combobox.config(
            state='readonly', 
            values=sorted([program for program in self.ssis.programs.values()], key=lambda program: program.code) # type: ignore
        )
    
    def set_actions(self) -> None:
        self.gui.add_program_button.config(
            command=lambda: self.parent_controller.add_program_button_pressed(self)
        )
        self.gui.add_student_button.config(
            command=self.add_student_button_pressed
        )
    
    def add_student_button_pressed(self) -> None:
        valid_i = Student.valid_id(id := self.get_id())
        valid_n = Student.valid_name(name := self.get_name())
        valid_y = Student.valid_year(year := self.get_year())
        valid_g = Student.valid_gender(gender := self.get_gender())
        valid_p = Program.valid_program_code(program_code := self.get_program_code())
        
        if valid_i and valid_n and valid_y and valid_g and valid_p:
            try:
                self.ssis.add_student(student := Student(
                    id=id,
                    name=name,
                    year=year,
                    gender=gender,
                    program_code=program_code
                ))
            
            except DuplicateStudentError:
                messagebox.showerror(
                    'Student Aleady Exists',
                    f'Student with ID "{id}" already exists.'
                )
                
                if messagebox.askyesno('Student Aleady Exists', f'Do you want to edit the existing student instead?'):
                    EditStudentController(
                        self.ssis, 
                        AddStudentWindow(self.gui.master), 
                        self.parent_controller, 
                        id
                    )
                    self.gui.destroy()
                
                return
                
            messagebox.showinfo(
                'Student Added Successfully!',
                f'Student "{student.id}" with:\n\tName "{student.name_formatted}",\n\tYear "{student.year}",\n\tGender "{student.gender}",\n\tProgram Code "{student.program_code}"\nadded successfully!'
            )
            
            self.parent_controller.load_students()
            
            self.gui.destroy()
        
        else:
            invalid_id_message = f'ID "{id}" is invalid.' * (not valid_i)
            invalid_name_message = f'Surname and First Name must not be blank.' * (not valid_n)
            invalid_year_message = f'Year "{year}" is invalid.' * (not valid_y)
            invalid_gender_message = f'Gender is invalid.' * (not valid_g)
            invalid_program_message = f'Program cannot be blank.' * (not valid_p)
            
            messagebox.showerror(
                'Invalid Student Input(s)',
                f'{invalid_id_message}\n{invalid_name_message}\n{invalid_year_message}\n{invalid_gender_message}\n{invalid_program_message}'.strip()
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
        try:
            return int(self.gui.year_entry.get().strip())
        
        except ValueError:
            return -1
    
    def get_gender(self) -> str:
        return self.gui.gender_combobox.get()
    
    def get_program_code(self) -> str:
        return self.gui.program_combobox.get().split('|')[0].strip()

class EditStudentController(AddStudentController):
    def __init__(
        self, 
        ssis: SSIS, 
        gui: AddStudentWindow, 
        parent_controller: SSISController,
        student_id: str
    ) -> None:
        super().__init__(ssis, gui, parent_controller)
        
        self.student = self.ssis.get_student_by_id(student_id)
        
        self.__load_data()
        
    def __load_data(self):
        self.gui.title('Edit Student')
        self.gui.add_student_button.config(text='Edit Student')
        
        self.gui.id_entry.insert(0, self.student.id)
        self.gui.id_entry.config(state='readonly')
        
        self.gui.year_entry.insert(0, str(self.student.year))
        
        self.gui.surname_entry.insert(0, self.student.name[0])
        self.gui.firstname_entry.insert(0, self.student.name[1])
        self.gui.middlename_entry.insert(0, self.student.name[2])
        self.gui.suffix_entry.insert(0, self.student.name[3])
        
        self.gui.gender_combobox.set(self.student.gender)
        
        self.gui.program_combobox.set(self.ssis.get_program_by_code(self.student.program_code))
    
    @override
    def add_student_button_pressed(self) -> None:
        valid_i = Student.valid_id(id := super().get_id())
        valid_n = Student.valid_name(name := super().get_name())
        valid_y = Student.valid_year(year := super().get_year())
        valid_g = Student.valid_gender(gender := super().get_gender())
        valid_p = Program.valid_program_code(program_code := super().get_program_code())
        
        if valid_i and valid_n and valid_y and valid_g and valid_p:
            self.student.name = name
            self.student.year = year
            self.student.gender = gender
            self.student.program_code = program_code
                
            messagebox.showinfo(
                'Student Edited Successfully!',
                f'Student "{self.student.id}" with:\n\tName "{self.student.name_formatted}",\n\tYear "{self.student.year}",\n\tGender "{self.student.gender}",\n\tProgram Code "{self.student.program_code}"\nadded successfully!'
            )
            
            self.parent_controller.load_students()
            
            self.gui.destroy()
        
        else:
            invalid_id_message = f'ID "{id}" is invalid.' * (not valid_i)
            invalid_name_message = f'Surname and First Name must not be blank.' * (not valid_n)
            invalid_year_message = f'Year "{year}" is invalid.' * (not valid_y)
            invalid_gender_message = f'Gender is invalid.' * (not valid_g)
            invalid_program_message = f'Program cannot be blank.' * (not valid_p)
            
            messagebox.showerror(
                'Invalid Student Input(s)',
                f'{invalid_id_message}\n{invalid_name_message}\n{invalid_year_message}\n{invalid_gender_message}\n{invalid_program_message}'.strip()
            )

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
        AddStudentController(self.ssis, AddStudentWindow(self.gui), self)
    
    def add_program_button_pressed(self, add_student_controller: AddStudentController | None = None) -> None:
        AddProgramController(self.ssis, AddProgramWindow(self.gui), self, add_student_controller)
