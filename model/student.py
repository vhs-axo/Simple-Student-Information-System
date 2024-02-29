from typing import Literal
import re

class Student:
    MIN_YEAR = 1
    MAX_YEAR = 6
    
    VALID_ID_PATTERN = r'[0-9]{4}-[0-9]{4}'
    VALID_GENDER_OPTIONS = ('MALE', 'FEMALE', 'OTHER')
    
    def __init__(
        self,
        id: str | Literal[r'[0-9]{4}-[0-9]{4}'],
        name: tuple[str, str, str, str],
        year: int,
        gender: str | Literal['MALE', 'FEMALE', 'OTHER'],
        program_code: str = ''
    ) -> None:
        """
        Initialize a Student object.

        Args:
            id (str): The ID of the student.
            name (tuple[str, str, str, str]): The name of the student, in the format (first_name, middle_name, last_name, suffix).
            year (int): The year level of the student.
            gender (str): The gender of the student.
            program_code (str, optional): The program code of the student. Defaults to ''.
        
        Raises:
            ValueError: If ID, name, year, or gender is invalid.
        """
        if not Student.valid_id(id):
            raise ValueError(f'ID must follow the format {Student.VALID_ID_PATTERN}')
        
        self.__id = id
        self.name = name
        self.year = year
        self.gender = gender
        self.program_code = program_code
    
    @property
    def id(self) -> str:
        """str: The ID of the student."""
        return self.__id
    
    @property
    def name(self) -> tuple[str, str, str, str]:
        """tuple[str, str, str, str]: The name of the student."""
        return self.__name
    
    @name.setter
    def name(self, name: tuple[str, str, str, str]) -> None:
        """
        Set the name of the student.

        Args:
            name (tuple[str, str, str, str]): The name of the student, in the format (first_name, middle_name, last_name, suffix).

        Raises:
            ValueError: If the name is invalid.
        """
        if not Student.valid_name(name):
            raise ValueError('Name entered is not valid.')
        
        self.__name = name
        
    @property
    def name_formatted(self) -> str:
        """
        str: The formatted name of the student.
        """
        name = f'{self.__name[0]}, {self.__name[1]}'
        
        name += f' {self.__name[2]}' * bool(len(self.__name[2]))
        name += f' {self.__name[3]}' * bool(len(self.__name[3]))
        
        return name
        
    @property
    def year(self) -> int:
        """int: The year level of the student."""
        return self.__year
    
    @year.setter
    def year(self, year: int) -> None:
        """
        Set the year level of the student.

        Args:
            year (int): The year level of the student.

        Raises:
            ValueError: If the year level is invalid.
        """
        if not Student.valid_year(year):
            raise ValueError(f'Invalid year level. Must be within {Student.MIN_YEAR} and {Student.MAX_YEAR}')
        
        self.__year = year
    
    @property
    def gender(self) -> str:
        """str: The gender of the student."""
        return self.__gender
    
    @gender.setter
    def gender(self, gender: str | Literal['MALE', 'FEMALE', 'OTHER']) -> None:
        """
        Set the gender of the student.

        Args:
            gender (str): The gender of the student.

        Raises:
            ValueError: If the gender is not recognized.
        """
        if not Student.valid_gender(gender):
            raise ValueError(f'Reconized gender values are {Student.VALID_GENDER_OPTIONS[0]}, {Student.VALID_GENDER_OPTIONS[1]}, {Student.VALID_GENDER_OPTIONS[2]}')
        
        self.__gender = gender
    
    @property
    def program_code(self) -> str:
        """str: The program code of the student."""
        return self.__program_code
    
    @program_code.setter
    def program_code(self, program_code: str) -> None:
        """
        Set the program code of the student.

        Args:
            program_code (str): The program code of the student.
        """
        self.__program_code = program_code
    
    @staticmethod
    def valid_id(id: str) -> bool:
        """
        Check if the provided ID is valid.

        Args:
            id (str): The ID to validate.

        Returns:
            bool: True if the ID is valid, False otherwise.
        """
        return bool(re.match(Student.VALID_ID_PATTERN, id))
    
    @staticmethod
    def valid_name(name: tuple[str, str, str, str]) -> bool:
        """
        Check if the provided name is valid.

        Args:
            name (tuple[str, str, str, str]): The name to validate.

        Returns:
            bool: True if the name is valid, False otherwise.
        """
        return len(name[0]) > 0 and \
               len(name[1]) > 0 and \
               len(name[2]) >= 0 and \
               len(name[3]) >= 0
    
    @staticmethod
    def valid_year(year: int) -> bool:
        """
        Check if the provided year is valid.

        Args:
            year (int): The year to validate.

        Returns:
            bool: True if the year is valid, False otherwise.
        """
        return Student.MIN_YEAR <= year <= Student.MAX_YEAR
    
    @staticmethod
    def valid_gender(gender: str) -> bool:
        """
        Check if the provided gender is valid.

        Args:
            gender (str): The gender to validate.

        Returns:
            bool: True if the gender is valid, False otherwise.
        """
        return gender in Student.VALID_GENDER_OPTIONS
    
    def __str__(self) -> str:
        """
        Return a string representation of the Student object.

        Returns:
            str: A string representation of the Student object.
        """
        return f'{self.__id} | Name: {self.name_formatted}; Year: {self.__year}; Gender: {self.__gender}; Program Code: {self.__program_code}'

class Program:
    def __init__(self, code: str, name: str) -> None:
        """
        Initialize a Program object.

        Args:
            code (str): The code of the program.
            name (str): The name of the program.

        Raises:
            ValueError: If code or name is invalid.
        """
        self.code = code
        self.name = name
        
    @property
    def code(self) -> str:
        """str: The code of the program."""
        return self.__code
    
    @code.setter
    def code(self, code: str) -> None:
        """
        Set the code of the program.

        Args:
            code (str): The code of the program.

        Raises:
            ValueError: If the code is invalid.
        """
        if not Program.valid_program_code(code):
            raise ValueError('Invalid program code.')
        
        self.__code = code
    
    @property
    def name(self) -> str:
        """str: The name of the program."""
        return self.__name
    
    @name.setter
    def name(self, name: str) -> None:
        """
        Set the name of the program.

        Args:
            name (str): The name of the program.

        Raises:
            ValueError: If the name is invalid.
        """
        if not Program.valid_program_name(name):
            raise ValueError('Invalid program name.')
        
        self.__name = name
        
    @staticmethod
    def valid_program_code(code: str) -> bool:
        """
        Check if the provided program code is valid.

        Args:
            code (str): The program code to validate.

        Returns:
            bool: True if the program code is valid, False otherwise.
        """
        return len(code) > 2
        
    @staticmethod
    def valid_program_name(name: str) -> bool:
        """
        Check if the provided program name is valid.

        Args:
            name (str): The program name to validate.

        Returns:
            bool: True if the program name is valid, False otherwise.
        """
        return len(name) > 12
    
    def __str__(self) -> str:
        """
        Return a string representation of the Program object.

        Returns:
            str: A string representation of the Program object.
        """
        return f'{self.__code} | {self.__name}'
