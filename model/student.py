from __future__ import annotations
from typing import Literal, Optional
import re

class Student:
    MIN_YEAR = 1
    MAX_YEAR = 6
    
    VALID_ID_PATTERN = r'[0-9]{4}-[0-9]{4}'
    VALID_GENDER_OPTIONS = ('MALE', 'FEMALE', 'OTHER')
    
    def __init__(
        self, 
        id: str, 
        name: tuple[str, str, Optional[str], Optional[str]], 
        year: int, 
        gender: Literal['MALE', 'FEMALE', 'OTHER'], 
        program_code: Optional[str] = None
    ) -> None:
        if not Student.valid_id(id):
            raise ValueError(f'{id!r} does not match the valid pattern {Student.VALID_ID_PATTERN!r}')
        
        self.__id = id
        self.name = name
        self.year = year
        self.gender = gender
        self.program_code = program_code
    
    @property
    def id(self) -> str:
        return self.__id
    
    @property
    def name(self) -> tuple[str, str, Optional[str], Optional[str]]:
        return self.__name
    
    @property
    def name_formatted(self) -> str:
        name = f'{self.__name[0]}, {self.__name[1]}'
        
        name += f' {self.__name[2]}' * bool(self.__name[2])
        name += f' {self.__name[3]}' * bool(self.__name[3])
        
        return name
    
    @property
    def year(self) -> int:
        return self.__year
    
    @property
    def gender(self) -> str:
        return self.__gender
    
    @property
    def program_code(self) -> Optional[str]:
        return self.__program_code
    
    @name.setter
    def name(self, name: tuple[str, str, Optional[str], Optional[str]]) -> None:
        if not (v_name := Student.valid_name(name)):
            raise ValueError(f'{name} is not a valid name.')
        
        self.__name = v_name
    
    @year.setter
    def year(self, year: int) -> None:
        if not Student.valid_year(year):
            raise ValueError(f'Year must be in the range {Student.MIN_YEAR} to {Student.MAX_YEAR}.')
        
        self.__year = year
    
    @gender.setter
    def gender(self, gender: Literal['MALE', 'FEMALE', 'OTHER']) -> None:
        if not (v_gender := Student.valid_gender(gender)):
            raise ValueError(f'Invalid gender {gender!r} value entered.')
        
        self.__gender = v_gender
    
    @program_code.setter
    def program_code(self, program_code: Optional[str]) -> None:
        if not program_code:
            self.__program_code = None
            return
        
        if not Program.valid_code(program_code):
            raise ValueError(f'{program_code!r} is not a valid program code.')
        
        self.__program_code = program_code
        
    @staticmethod
    def valid_id(id: str) -> Optional[str]:
        if re.match(Student.VALID_ID_PATTERN, id):
            return id
        
        return None
    
    @staticmethod
    def valid_name(name: tuple[str, str, Optional[str], Optional[str]]) -> Optional[tuple[str, str, Optional[str], Optional[str]]]:
        if not (name[0] and name[1]):
            return None
        
        return (
            name[0], 
            name[1], 
            name[2] if name[2] else None, 
            name[3] if name[3] else None
        )
    
    @staticmethod
    def valid_year(year: int) -> Optional[int]:
        if Student.MIN_YEAR <= year <= Student.MAX_YEAR:
            return year
        
        return None
    
    @staticmethod
    def valid_gender(gender: str) -> Optional[str]:
        if (g := gender.upper()) in Student.VALID_GENDER_OPTIONS:
            return g
        
        return None
    
    def __str__(self) -> str:
        return f'{self.__id} | {self.name_formatted} | Year {self.__year} | {self.__gender} | {self.__program_code}'
    
    def __repr__(self) -> str:
        return f'Student(id={self.__id!r}, name={self.__name}, year={self.__year}, gender={self.__gender!r}, program_code={self.__program_code!r})'

class Program:
    def __init__(self, code: str, name: str) -> None:
        self.code = code
        self.name = name
    
    @property
    def code(self) -> str:
        return self.__code
    
    @property
    def name(self) -> str:
        return self.__name
    
    @code.setter
    def code(self, code: str) -> None:
        if not Program.valid_code(code):
            raise ValueError(f'{code!r} is an invalid program code.')
        
        self.__code = code
    
    @name.setter
    def name(self, name: str) -> None:
        if not Program.valid_name(name):
            raise ValueError(f'{name!r} is an invalid program name.')
        
        self.__name = name
    
    @staticmethod
    def valid_code(code: str) -> Optional[str]:
        if len(code) > 2:
            return code
        
        return None
    
    @staticmethod
    def valid_name(name: str) -> Optional[str]:
        if len(name) > 12:
            return name
        
        return None
    
    def __str__(self) -> str:
        return f'{self.__code} | {self.__name}'
    
    def __repr__(self) -> str:
        return f'Program(code={self.__code!r}, name={self.__name!r})'
