from model.student import Student, Program
from csv import DictReader, DictWriter
from typing import Collection

class DuplicateProgramError(Exception):
    """Exception raised when attempting to add a program with a duplicate code."""

    def __init__(self, program_code: str) -> None:
        super().__init__(f'Program with code "{program_code}" already exists.')

class DuplicateStudentError(Exception):
    """Exception raised when attempting to add a student with a duplicate ID."""

    def __init__(self, student_id: str) -> None:
        super().__init__(f'Student with ID "{student_id}" already exists.')

class ProgramNotFoundError(Exception):
    """Exception raised when a program with a specified code is not found."""

    def __init__(self, program_code: str) -> None:
        super().__init__(f'Program with code "{program_code}" not found.')

class StudentNotFoundError(Exception):
    """Exception raised when a student with a specified ID is not found."""

    def __init__(self, student_id: str) -> None:
        super().__init__(f'Student with ID "{student_id}" not found.')

class SSIS:
    """Simple Student Information System class."""

    # Define field names for CSV files
    STUDENT_FIELD_NAMES = ('id', 'surname', 'firstname', 'middlename', 'suffix', 'year', 'gender', 'program_code')
    PROGRAM_FIELD_NAMES = ('code', 'name')

    UNENROLLED = 'NOT ENROLLED'
    
    def __init__(self, programs_path: str, students_path: str) -> None:
        """
        Initialize the SSIS instance.

        Args:
            programs_path (str): Path to the programs CSV file.
            students_path (str): Path to the students CSV file.
        """
        self.programs_path = programs_path
        self.students_path = students_path
        
        # Dictionaries to store programs and students
        self.programs: dict[str, Program] = {}
        self.students: dict[str, Student] = {}
        
        # Load programs and students from CSV files
        self.__load_programs()
        self.__load_students()
    
    @staticmethod
    def create_csv_file(file_path: str, fieldnames: Collection[str]) -> None:
        """
        Create a new CSV file with the specified field names as header.

        Args:
            file_path (str): Path to the CSV file.
            fieldnames (Collection[str]): Field names to be used as header.
        """
        with open(file_path, 'w', newline='') as file:
            writer = DictWriter(file, fieldnames)
            writer.writeheader()
    
    def __load_programs(self) -> None:
        """Load programs from the programs CSV file."""
        try:
            with open(self.programs_path, 'r') as prog_file:
                next(prog_file)  # Skip header
                
                reader = DictReader(prog_file, SSIS.PROGRAM_FIELD_NAMES)
                
                for row in reader:
                    self.add_program(Program(
                        code=row['code'],
                        name=row['name']
                    ))
            
        except FileNotFoundError:
            SSIS.create_csv_file(self.programs_path, SSIS.PROGRAM_FIELD_NAMES)
    
    def __load_students(self) -> None:
        """Load students from the students CSV file."""
        try:
            with open(self.students_path, 'r') as stud_file:
                next(stud_file)  # Skip header
                
                reader = DictReader(stud_file, SSIS.STUDENT_FIELD_NAMES, restval='')
                
                for row in reader:
                    self.add_student(Student(
                        id=row['id'],
                        name=(
                            row['surname'],
                            row['firstname'],
                            row['middlename'],
                            row['suffix']
                        ),
                        year=int(row['year']),
                        gender=row['gender'],
                        program_code=row['program_code']
                    ))
            
        except FileNotFoundError:
            SSIS.create_csv_file(self.students_path, SSIS.STUDENT_FIELD_NAMES)
    
    def save_programs(self) -> None:
        """Save programs to the programs CSV file."""
        with open(self.programs_path, 'w', newline='') as prog_file:
            writer = DictWriter(prog_file, SSIS.PROGRAM_FIELD_NAMES)
            writer.writeheader()
            
            for program in sorted(self.programs.values(), key=lambda program: program.code):
                writer.writerow({
                    'code': program.code,
                    'name': program.name
                })
    
    def save_students(self) -> None:
        """Save students to the students CSV file."""
        with open(self.students_path, 'w', newline='') as stud_file:
            writer = DictWriter(stud_file, SSIS.STUDENT_FIELD_NAMES)
            writer.writeheader()
            
            for student in sorted(self.students.values(), key=lambda student: student.id):
                writer.writerow({
                    'id': student.id,
                    'surname': student.name[0],
                    'firstname': student.name[1],
                    'middlename': student.name[2],
                    'suffix': student.name[3],
                    'year': student.year,
                    'gender': student.gender,
                    'program_code': student.program_code
                })
    
    def add_program(self, program: Program) -> None:
        """
        Add a new program.

        Args:
            program (Program): Program to be added.

        Raises:
            DuplicateProgramError: If a program with the same code already exists.
        """
        if program.code in self.programs:
            raise DuplicateProgramError(program.code)
        
        self.programs[program.code] = program
    
    def add_student(self, student: Student) -> None:
        """
        Add a new student.

        Args:
            student (Student): Student to be added.

        Raises:
            DuplicateStudentError: If a student with the same ID already exists.
        """
        if student.id in self.students:
            raise DuplicateStudentError(student.id)
        
        self.students[student.id] = student
        
    def get_program_by_code(self, program_code: str) -> Program:
        """
        Get a program by its code.

        Args:
            program_code (str): Code of the program to retrieve.

        Returns:
            Program: Program with the specified code.

        Raises:
            ProgramNotFoundError: If no program with the specified code is found.
        """
        if program_code not in self.programs:
            raise ProgramNotFoundError(program_code)
        
        return self.programs[program_code]
    
    def get_student_by_id(self, student_id: str) -> Student:
        """
        Get a student by their ID.

        Args:
            student_id (str): ID of the student to retrieve.

        Returns:
            Student: Student with the specified ID.

        Raises:
            ValueError: If the student ID does not match the valid pattern.
            StudentNotFoundError: If no student with the specified ID is found.
        """
        if not Student.valid_id(student_id):
            raise ValueError(f'ID must follow the format {Student.VALID_ID_PATTERN}')
        
        if student_id not in self.students:
            raise StudentNotFoundError(student_id)
        
        return self.students[student_id]
    
    def delete_program_by_code(self, program_code: str) -> Program:
        """
        Delete a program by its code.

        Args:
            program_code (str): Code of the program to delete.

        Returns:
            Program: Program that was deleted.

        Raises:
            ProgramNotFoundError: If no program with the specified code is found.
        """
        if program_code not in self.programs:
            raise ProgramNotFoundError(program_code)
        
        return self.programs.pop(program_code)
    
    def delete_student_by_id(self, student_id: str) -> Student:
        """
        Delete a student by their ID.

        Args:
            student_id (str): ID of the student to delete.

        Returns:
            Student: Student that was deleted.

        Raises:
            ValueError: If the student ID does not match the valid pattern.
            StudentNotFoundError: If no student with the specified ID is found.
        """
        if not Student.valid_id(student_id):
            raise ValueError(f'ID must follow the format {Student.VALID_ID_PATTERN}')
        
        if student_id not in self.students:
            raise StudentNotFoundError(student_id)
        
        return self.students.pop(student_id)
