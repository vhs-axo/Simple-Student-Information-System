from model.student import Student, Program
from csv import DictReader, DictWriter
from typing import Iterable

class DuplicateProgramError(Exception):
    def __init__(self, program_code: str) -> None:
        super().__init__(f'Program with code "{program_code}" already exists.')
        
class DuplicateStudentError(Exception):
    def __init__(self, student_id: str) -> None:
        super().__init__(f'Student with ID "{student_id}" already exists.')
        
class ProgramNotFoundError(Exception):
    def __init__(self, program_code: str) -> None:
        super().__init__(f'Program with code "{program_code}" not found.')
        
class StudentNotFoundError(Exception):
    def __init__(self, student_id: str) -> None:
        super().__init__(f'Student with ID "{student_id}" not found.')

class SSIS:
    STUDENT_FIELD_NAMES = ('id', 'surname', 'firstname', 'middlename', 'suffix', 'year', 'gender', 'program_code')
    PROGRAM_FIELD_NAMES = ('code', 'name')

    UNENROLLED = 'NOT ENROLLED'
    
    def __init__(self, programs_path: str, students_path: str) -> None:
        self.programs_path = programs_path
        self.students_path = students_path
        
        self.programs: dict[str, Program] = {}
        self.students: dict[str, Student] = {}
        
        self._load_programs()
        self._load_students()
    
    @staticmethod
    def create_csv_file(file_path: str, fieldnames: Iterable[str]) -> None:
        with open(file_path, 'w', newline='') as file:
            writer = DictWriter(file, fieldnames)
            
            writer.writeheader()
    
    def _load_programs(self) -> None:
        try:
            with open(self.programs_path, 'r') as prog_file:
                next(prog_file)
                
                reader = DictReader(prog_file, SSIS.PROGRAM_FIELD_NAMES)
                
                for row in reader:
                    self.add_program(Program(
                        code=row['code'],
                        name=row['name']
                    ))
            
        except FileNotFoundError:
            SSIS.create_csv_file(self.programs_path, SSIS.PROGRAM_FIELD_NAMES)
    
    def _load_students(self) -> None:
        try:
            with open(self.students_path, 'r') as stud_file:
                next(stud_file)
                
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
        with open(self.programs_path, 'w', newline='') as prog_file:
            writer = DictWriter(prog_file, SSIS.PROGRAM_FIELD_NAMES)
            
            writer.writeheader()
            
            for program in sorted(self.programs.values(), key=lambda program: program.code):
                if program is SSIS.UNENROLLED_PROGRAM:
                    continue
                
                writer.writerow({
                    'code': program.code,
                    'name': program.name
                })
    
    def save_students(self) -> None:
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
        if program.code in self.programs:
            raise DuplicateProgramError(program.code)
        
        self.programs[program.code] = program
    
    def add_student(self, student: Student) -> None:
        if student.id in self.students:
            raise DuplicateStudentError(student.id)
        
        self.students[student.id] = student
        
    def get_program_by_code(self, program_code) -> Program:
        if program_code not in self.programs:
            raise ProgramNotFoundError(program_code)
        
        return self.programs[program_code]
    
    def get_student_by_id(self, student_id: str) -> Student:
        if not Student.valid_id(student_id):
            raise ValueError(f'ID must follow the format {Student.VALID_ID_PATTERN}')
        
        if student_id not in self.students:
            raise StudentNotFoundError(student_id)
        
        return self.students[student_id]
    
    def delete_program_by_code(self, program_code: str) -> Program:
        if program_code not in self.programs:
            raise ProgramNotFoundError(program_code)
        
        return self.programs.pop(program_code)
    
    def delete_student_by_id(self, student_id: str) -> Student:
        if not Student.valid_id(student_id):
            raise ValueError(f'ID must follow the format {Student.VALID_ID_PATTERN}')
        
        if student_id not in self.students:
            raise StudentNotFoundError(student_id)
        
        return self.students.pop(student_id)
