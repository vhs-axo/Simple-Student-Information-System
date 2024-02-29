from view.ssis_gui import SSISWindow
from model.ssis import SSIS
from control.controller import SSISController

def main() -> None:
    programs_path = 'data/programs.csv'
    students_path = 'data/students.csv'
    
    main_window = SSISWindow()
    info_sys = SSIS(programs_path, students_path)
    
    SSISController(info_sys, main_window)
    
    main_window.mainloop()

if __name__ == '__main__':
   main()
