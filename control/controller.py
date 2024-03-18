from __future__ import annotations
# from typing import override
from view.ssis_gui import SSISWindow, AddStudentWindow, AddProgramWindow
from model.student import Student, Program
from model.ssis import SSIS, DuplicateProgramError, DuplicateStudentError
from tkinter import Event, Menu, StringVar, messagebox, END

class AddProgramController:
    """Controller for adding a new program."""
    
    def __init__(
            self, 
            ssis: SSIS, 
            gui: AddProgramWindow,
            parent_controller: SSISController,
            add_student_controller: AddStudentController | None = None
        ) -> None:
        """
        Initialize the AddProgramController.

        Args:
            ssis (SSIS): The SSIS model.
            gui (AddProgramWindow): The GUI window for adding a program.
            parent_controller (SSISController): The parent controller.
            add_student_controller (AddStudentController | None, optional): The controller for adding a student. Defaults to None.
        """
        self.ssis = ssis
        self.gui = gui
        self.parent_controller = parent_controller
        self.add_student_controller = add_student_controller
        
        self.set_actions()
        self.set_validations()
    
    def set_actions(self) -> None:
        """Set actions for GUI elements."""
        self.gui.add_program_button.config(command=self.add_program_button_pressed)
        
    def set_validations(self) -> None:
        """Set input validations for program code and name."""
        self.program_code_validation()
        self.program_name_validation()
    
    def add_program_button_pressed(self) -> None:
        """Handle button press for adding a program."""
        code = self.gui.program_code_entry.get()
        name = self.gui.program_name_entry.get()
        
        # Validate program code and name
        if (pcv := Program.valid_program_code(code)) and (pnv := Program.valid_program_name(name)):
            try:
                # Attempt to add the program to the SSIS model
                self.ssis.add_program(program := Program(
                    code.upper().strip(),
                    name.upper().strip()
                ))
            
            except DuplicateProgramError:
                # If program already exists, show error message
                messagebox.showerror(
                    'Program Aleady Exists',
                    f'Program "{self.ssis.get_program_by_code(code)}" already exists.'
                )
                
                # Ask user if they want to edit the existing program
                if messagebox.askyesno('Program Aleady Exists', f'Do you want to edit the existing program instead?'):
                    # Initialize EditProgramController and destroy current window
                    EditProgramController(
                        self.ssis, 
                        AddProgramWindow(self.gui.master), 
                        self.parent_controller, 
                        code, 
                        self.add_student_controller
                    )
                    self.gui.destroy()
                
                return
            
            # Show success message and update parent controller
            messagebox.showinfo(
                'Program Added Successfully!',
                f'Program with:\n\tCode "{program.code}",\n\tName "{program.name}"\nadded successfully!'
            )
            
            self.parent_controller.load_programs()
            self.parent_controller.load_students()
            
            if self.add_student_controller is not None:
                self.add_student_controller.load_programs()
                
            self.gui.destroy()
        
        else:
            # Show error message for invalid input
            invalid_code_message = f'"{code.upper().strip()}" is not a valid program code.' * (not pcv)
            invalid_name_message = f'"{name.upper().strip()}" is not a valid program name.' * (not pnv)
            
            messagebox.showerror(
                'Invalid Input(s)', 
                f'{invalid_code_message}\n{invalid_name_message}'.strip()
            )
    
    def program_code_validation(self) -> None:
        """Set validation for program code entry."""
        validate_cmd = self.gui.register(lambda change: change.isalpha() or change in '()' or change.isspace())
        
        self.gui.program_code_entry.config(validate='key', validatecommand=(validate_cmd, '%S'))
        
    def program_name_validation(self) -> None:
        """Set validation for program name entry."""
        validate_cmd = self.gui.register(lambda change: change.isalpha() or change in '()' or change.isspace())
        
        self.gui.program_name_entry.config(validate='key', validatecommand=(validate_cmd, '%S'))

class EditProgramController(AddProgramController):
    """Controller for editing an existing program."""
    
    def __init__(
        self, 
        ssis: SSIS, 
        gui: AddProgramWindow, 
        parent_controller: SSISController, 
        program_code: str, 
        add_student_controller: AddStudentController | None = None
    ) -> None:
        """
        Initialize the EditProgramController.

        Args:
            ssis (SSIS): The SSIS model.
            gui (AddProgramWindow): The GUI window for editing a program.
            parent_controller (SSISController): The parent controller.
            program_code (str): The code of the program to edit.
            add_student_controller (AddStudentController | None, optional): The controller for adding a student. Defaults to None.
        """
        super().__init__(ssis, gui, parent_controller, add_student_controller)
        
        self.program = self.ssis.get_program_by_code(program_code)
        
        self.__load_data()
        
    def __load_data(self) -> None:
        """Load data for editing the program."""
        self.gui.title('Edit Program')
        self.gui.add_program_button.config(text='Edit Program')
        
        self.code_var = StringVar()
        self.name_var = StringVar()
        
        self.gui.program_code_entry.config(textvariable=self.code_var)
        self.gui.program_name_entry.config(textvariable=self.name_var)
        
        self.code_var.set(self.program.code)
        self.name_var.set(self.program.name)
    
    # @override
    def add_program_button_pressed(self) -> None:
        """Handle button press for editing a program."""
        code = self.gui.program_code_entry.get().upper().strip()
        name = self.gui.program_name_entry.get().upper().strip()
        
        if (pcv := Program.valid_program_code(code)) and (pnv := Program.valid_program_name(name)):
            # Update program details
            self.program.code = code
            self.program.name = name
            
            messagebox.showinfo(
                'Program Edited Successfully!',
                f'Program with:\n\tCode "{self.program.code}",\n\tName {self.program.name}\nadded successfully!'
            )
            
            self.parent_controller.load_programs()
            self.parent_controller.load_students()
            
            if self.add_student_controller is not None:
                self.add_student_controller.load_programs()
                
            self.gui.destroy()
        
        else:
            # Show error message for invalid input
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
        self.set_validations()
        
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
        
    def set_validations(self) -> None:
        self.id_validation()
        self.year_validation()
        self.surname_validation()
        self.firstname_validation()
        self.middlename_validation()
        self.suffix_validation()
    
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
    
    def id_validation(self) -> None:
        def id_val(text: str, change: str, new_text: str) -> bool:
            # Check if the length of new text is less than the length of old text
            if len(new_text) < len(text):
                return True
            
            # Check the length of the text
            if len(text) <= 8:
                # If the length is less than 3, only allow digits
                if len(text) < 3:
                    return change.isdigit()
                # If the length is 4, only allow '-'
                elif len(text) == 4:
                    return change == '-'
                # For other lengths, allow only digits
                else:
                    return change.isdigit()
            
            return False

        validation = self.gui.register(id_val)
        self.gui.id_entry.config(validate='key', validatecommand=(validation, '%s','%S', '%P'))
    
    def year_validation(self) -> None:
        def year_val(text: str) -> bool:
            if len(text) == 0:
                return True
            
            if text.isdigit():
                if Student.MIN_YEAR <= int(text) <= Student.MAX_YEAR:
                    return True
            
            return False
        
        validation = self.gui.register(year_val)
        self.gui.year_entry.config(validate='key', validatecommand=(validation, '%P'))
    
    def surname_validation(self) -> None:
        validation = self.gui.register(lambda change: change.isalpha() or change.isspace())
        self.gui.surname_entry.config(validate='key', validatecommand=(validation, '%S'))
    
    def firstname_validation(self) -> None:
        validation = self.gui.register(lambda change: change.isalpha() or change.isspace())
        self.gui.firstname_entry.config(validate='key', validatecommand=(validation, '%S'))
    
    def middlename_validation(self) -> None:
        validation = self.gui.register(lambda change: change.isalpha() or change.isspace())
        self.gui.middlename_entry.config(validate='key', validatecommand=(validation, '%S'))
    
    def suffix_validation(self) -> None:
        validation = self.gui.register(lambda change: change.isalpha() or change == '.')
        self.gui.suffix_entry.config(validate='key', validatecommand=(validation, '%S'))

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
        
        self.id_var = StringVar()
        self.year_var = StringVar()
        self.surname_var = StringVar()
        self.firstname_var = StringVar()
        self.middlename_var = StringVar()
        self.suffix_var = StringVar()
        
        for entry, string_var in (
            (self.gui.id_entry, self.id_var), 
            (self.gui.year_entry, self.year_var), 
            (self.gui.surname_entry, self.surname_var), 
            (self.gui.firstname_entry, self.firstname_var), 
            (self.gui.middlename_entry, self.middlename_var), 
            (self.gui.suffix_entry, self.suffix_var)
        ):
            entry.config(textvariable=string_var)
        
        self.id_var.set(self.student.id)
        self.year_var.set(str(self.student.year))
        self.surname_var.set(self.student.name[0])
        self.firstname_var.set(self.student.name[1])
        self.middlename_var.set(self.student.name[2])
        self.suffix_var.set(self.student.name[3])
        
        self.gui.id_entry.config(state='readonly')
        
        self.gui.gender_combobox.set(self.student.gender)
        
        self.gui.program_combobox.set(self.ssis.get_program_by_code(self.student.program_code))
    
    # @override
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
        
        self.set_context_menus()
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
        
        self.student_menu.add_command(label='Edit Student', command=self.edit_student)
        self.student_menu.add_command(label='Delete Student', command=self.delete_student)
        
        self.program_menu.add_command(label='Edit Program', command=self.edit_program)
        self.program_menu.add_command(label='Delete Program', command=self.delete_program)
        
        self.gui.student_list.bind('<Button-3>', self.show_student_menu)
        self.gui.program_list.bind('<Button-3>', self.show_program_menu)
    
    def save_button_pressed(self) -> None:
        self.ssis.save_programs()
        self.ssis.save_students()
        
        messagebox.showinfo(
            'Saved',
            'Changes have been saved successfully!'
        )
    
    def add_student_button_pressed(self) -> None:
        AddStudentController(self.ssis, AddStudentWindow(self.gui), self)
    
    def add_program_button_pressed(self, add_student_controller: AddStudentController | None = None) -> None:
        AddProgramController(self.ssis, AddProgramWindow(self.gui), self, add_student_controller)
        
    def set_context_menus(self) -> None:
        self.student_menu = Menu(self.gui.student_tab, tearoff=0)
        self.program_menu = Menu(self.gui.program_tab, tearoff=0)
        
    def show_student_menu(self, event: Event) -> None:
        student_id = self.gui.student_list.identify_row(event.y)
        
        if student_id:
            self.gui.student_list.selection_set(student_id)
            self.student_menu.post(event.x_root, event.y_root)
    
    def show_program_menu(self, event: Event) -> None:
        program_code = self.gui.program_list.identify_row(event.y)
        
        if program_code:
            self.gui.program_list.selection_set(program_code)
            self.program_menu.post(event.x_root, event.y_root)
    
    def edit_student(self) -> None:
        EditStudentController(
            self.ssis, 
            AddStudentWindow(self.gui), 
            self, 
            self.gui.student_list.selection()[0]
        )
    
    def edit_program(self) -> None:
        EditProgramController(
            self.ssis, 
            AddProgramWindow(self.gui),
            self,
            self.gui.program_list.selection()[0]
        )
    
    def delete_student(self) -> None:
        student = self.ssis.get_student_by_id(id := self.gui.student_list.selection()[0])
        
        if messagebox.askyesno(
            'Delete Student',
            f'Are you sure you want to delete student "{student.id}" with:\n\tName "{student.name_formatted}",\n\tYear "{student.year}",\n\tGender "{student.gender}",\n\tProgram Code "{student.program_code}"'
        ):
            student = self.ssis.delete_student_by_id(id)
            
            self.load_students()
        
            messagebox.showinfo(
                'Student Deleted Successfully',
                f'Student "{student.id}" was deleted successfully!'
            )
    
    def delete_program(self) -> None:
        program = self.ssis.get_program_by_code(code := self.gui.program_list.selection()[0])
        
        if messagebox.askyesno(
            'Delete Program',
            f'Are you sure you want to delete the program "{program}" ?'
        ):
            program = self.ssis.delete_program_by_code(code)
            
            self.load_programs()
            self.load_students()
        
            messagebox.showinfo(
                'Program Deleted Successfully',
                f'Program "{program.code}" was deleted successfully!'
            )
    