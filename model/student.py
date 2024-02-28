from __future__ import annotations
from typing import Literal
import re

class Student:
    MIN_YEAR = 1
    MAX_YEAR = 6
    
    VALID_ID_PATTERN = r'[0-9]{4}-[0-9]{4}'
    VALID_GENDER_OPTIONS = ('MALE', 'FEMALE', 'OTHER')
    
    def __init__(
        self,
        id: Literal[r'[0-9]{4}-[0-9]{4}'],
        name: tuple[str, str, str, str],
        year: int,
        gender: Literal['MALE', 'FEMALE', 'OTHER'],
        program_code: str = ''
    ) -> None:
        if not Student.valid_id(id):
            raise ValueError(f'ID must follow the format {Student.VALID_ID_PATTERN}')
        
        self._id = id
        self.name = name
        self.year = year
        self.gender = gender
        self.program_code = program_code
    
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def name(self) -> tuple[str, str, str, str]:
        return self._name
    
    @name.setter
    def name(self, name: tuple[str, str, str, str]) -> None:
        self._name = name
        
    @property
    def name_formatted(self) -> str:
        name = f'{self._name[0]}, {self._name[1]}'
        
        name += f' {self._name[2]}' * bool(len(self._name[2]))
        name += f' {self._name[3]}' * bool(len(self._name[3]))
        
        return name
        
    @property
    def year(self) -> int:
        return self._year
    
    @year.setter
    def year(self, year: int) -> None:
        if not Student.valid_year(year):
            raise ValueError(f'Invalid year level. Must be within {Student.MIN_YEAR} and {Student.MAX_YEAR}')
        
        self._year = year
    
    @property
    def gender(self) -> str:
        return self._gender
    
    @gender.setter
    def gender(self, gender: Literal['MALE', 'FEMALE', 'OTHER']) -> None:
        if not Student.valid_gender(gender):
            raise ValueError(f'Reconized gender values are {Student.VALID_GENDER_OPTIONS[0]}, {Student.VALID_GENDER_OPTIONS[1]}, {Student.VALID_GENDER_OPTIONS[2]}')
        
        self._gender = gender
    
    @property
    def program_code(self) -> str:
        return self._program_code
    
    @program_code.setter
    def program_code(self, program_code: str) -> None:
        self._program_code = program_code
    
    @staticmethod
    def valid_id(id: str) -> bool:
        return bool(re.match(Student.VALID_ID_PATTERN, id))
    
    @staticmethod
    def valid_year(year: int) -> bool:
        return Student.MIN_YEAR <= year <= Student.MAX_YEAR
    
    @staticmethod
    def valid_gender(gender: str) -> bool:
        return gender in Student.VALID_GENDER_OPTIONS
    
    def __str__(self) -> str:
        return f'{self._id} | Name: {self.name_formatted}; Year: {self._year}; Gender: {self._gender}; Program Code: {self._program_code}'

class Program:
    def __init__(self, code: str, name: str) -> None:
        self.code = code
        self.name = name
        
    @property
    def code(self) -> str:
        return self._code
    
    @code.setter
    def code(self, code: str) -> None:
        if not Program.valid_program_code(code):
            raise ValueError('Invalid program code.')
        
        self._code = code
    
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, name: str) -> None:
        if not Program.valid_program_name(name):
            raise ValueError('Invalid program name.')
        
        self._name = name
        
    @staticmethod
    def valid_program_code(code: str) -> bool:
        return len(code) > 2
        
    @staticmethod
    def valid_program_name(name: str) -> bool:
        return len(name) > 12
    
    def __str__(self) -> str:
        return f'{self.code} | {self.name}'
