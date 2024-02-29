from __future__ import annotations
from tkinter import Tk, Toplevel
from tkinter.ttk import Notebook, Treeview, Combobox, Style, Button, Label, Entry, Frame, Scrollbar

FONT_NORMAL = ('', 10)
FONT_BOLD = ('', 10, 'bold')
FONT_ITALIC = ('', 10, 'italic')

class AddProgramWindow(Toplevel):
    def __init__(self, master: SSISWindow) -> None:
        super().__init__(master)
        
        self.title('Add Program')
        
        self._set_labels()
        self._set_entries()
        self._set_button()
        
        self._set_layout()
        
        self.resizable(False, False)
        
        self.grab_set()
    
    def _set_labels(self) -> None:
        self.program_code_label = Label(self, text='Program Code')
        self.program_name_label = Label(self, text='Program Name')
    
    def _set_entries(self) -> None:
        self.program_code_entry = Entry(self, font=FONT_NORMAL)
        self.program_name_entry = Entry(self, font=FONT_NORMAL)
    
    def _set_button(self) -> None:
        self.add_program_button = Button(self, text='Add Program')
    
    def _set_layout(self) -> None:
        self.style = Style()
        
        width = int(self.winfo_screenwidth() / 2)
        height = int(width / 5)
        
        self.geometry(f'{width}x{height}')
        
        for row_col in range(0, 3):
            self.columnconfigure(row_col, weight=1)
            self.rowconfigure(row_col, weight=1)
        
        self.columnconfigure(row_col, weight=3)
        self.rowconfigure(row_col, weight=1)
        
        self.program_code_label.grid(row=0, column=0, rowspan=1, columnspan=1, sticky='w', padx=15, pady=(15, 5))
        self.program_name_label.grid(row=0, column=2, rowspan=1, columnspan=1, sticky='w', padx=15, pady=(15, 5))
        
        self.program_code_entry.grid(row=1, column=0, rowspan=1, columnspan=2, sticky='nsew', padx=15)
        self.program_name_entry.grid(row=1, column=2, rowspan=1, columnspan=2, sticky='nsew', padx=15)
        
        self.add_program_button.grid(row=3, column=3, rowspan=1, columnspan=1, sticky='nsew', padx=15, pady=15)
        
        self.style.configure('TLabel', font=FONT_BOLD)
        self.style.configure('TButton', font=FONT_BOLD)

class AddStudentWindow(Toplevel):
    def __init__(self, master: SSISWindow) -> None:
        super().__init__(master=master)
        
        self.title('Add Student')
        
        self._set_labels()
        self._set_entries()
        self._set_comboboxes()
        self._set_buttons()
        self._set_layout()
        
        self.resizable(False, False)
        
        self.grab_set()
        
    def _set_labels(self) -> None:
        self.id_label = Label(self, text='Student ID')
        
        self.surname_label = Label(self, text='Surname')
        self.firstname_label = Label(self, text='First Name')
        self.middlename_label = Label(self, text='Middle Name')
        self.suffix_label = Label(self, text='Suffix')
        
        self.year_label = Label(self, text='Year Level')
        
        self.gender_label = Label(self, text='Gender')
        
        self.program_label = Label(self, text='Program')
    
    def _set_entries(self) -> None:
        self.id_entry = Entry(self, font=FONT_NORMAL)
        
        self.surname_entry = Entry(self, font=FONT_NORMAL)
        self.firstname_entry = Entry(self, font=FONT_NORMAL)
        self.middlename_entry = Entry(self, font=FONT_NORMAL)
        self.suffix_entry = Entry(self, font=FONT_NORMAL)
        
        self.year_entry = Entry(self, font=FONT_NORMAL)
        
    def _set_comboboxes(self) -> None:
        self.gender_combobox = Combobox(self, font=FONT_NORMAL)
        self.program_combobox = Combobox(self, font=FONT_NORMAL)
    
    def _set_buttons(self) -> None:
        self.add_student_button = Button(self, text='Add Student', style='AddStudent.TButton')
        self.add_program_button = Button(self, text='Program not found? Add program here!', style='AddProgram.TButton')
        
    def _set_layout(self) -> None:        
        width = int(self.winfo_screenwidth() * 0.75)
        height = int(width * 2 / 5)
        
        self.geometry(f'{width}x{height}')
        
        for column in range(0, 7):
            self.columnconfigure(column, weight=1)
        
        for row in range(0, 13):
            self.rowconfigure(row, weight=1)
        
        self.id_label.grid(row=0, column=0, rowspan= 1, columnspan= 1, sticky='w', padx=(15, 0), pady=(15, 0))
        self.year_label.grid(row=0, column=2, rowspan=1, columnspan=1, sticky='w', padx=(15, 0), pady=(15, 0))
        self.surname_label.grid(row=3, column=0, rowspan= 1, columnspan= 1, sticky='w', padx=(15, 0), pady=0)
        self.firstname_label.grid(row=3, column=2, rowspan= 1, columnspan= 1, sticky='w', padx=(15, 0), pady=0)
        self.middlename_label.grid(row=3, column=4, rowspan= 1, columnspan= 1, sticky='w', padx=(15, 0), pady=0)
        self.suffix_label.grid(row=3, column=6, rowspan= 1, columnspan= 1, sticky='w', padx=(15, 0), pady=0)
        self.gender_label.grid(row=6, column=0, rowspan= 1, columnspan= 1, sticky='w', padx=(15, 0), pady=0)
        self.program_label.grid(row=9, column=0, rowspan= 1, columnspan= 1, sticky='w', padx=(15, 0), pady=0)
        
        self.id_entry.grid(row=1, column=0, rowspan=1, columnspan=2, sticky='nsew', padx=15)
        self.year_entry.grid(row=1, column=2, rowspan=1, columnspan=1, sticky='nsew', padx=15)
        self.surname_entry.grid(row=4, column=0, rowspan=1, columnspan=2, sticky='nsew', padx=15)
        self.firstname_entry.grid(row=4, column=2, rowspan=1, columnspan=2, sticky='nsew', padx=15)
        self.middlename_entry.grid(row=4, column=4, rowspan=1, columnspan=2, sticky='nsew', padx=15)
        self.suffix_entry.grid(row=4, column=6, rowspan=1, columnspan=1, sticky='nsew', padx=15)
        
        self.gender_combobox.grid(row=7, column=0, rowspan=1, columnspan=1, sticky='nsew', padx=15)
        self.program_combobox.grid(row=10, column=0, rowspan=1, columnspan=4, sticky='nsew', padx=15)
        
        self.add_program_button.grid(row=10, column=4, rowspan=1, columnspan=2, sticky='nsew', padx=15)
        self.add_student_button.grid(row=12, column=6, rowspan=1, columnspan=1, sticky='nsew', padx=15, pady=(0, 15))
        
        self.style = Style()
        
        self.option_add("*TCombobox*Listbox*Font", FONT_NORMAL)
        self.style.configure('TLabel', font=FONT_BOLD)
        self.style.configure('AddStudent.TButton', font=FONT_BOLD)
        self.style.configure('AddProgram.TButton', font=FONT_ITALIC)

class SSISWindow(Tk):
    def __init__(self) -> None:
        super().__init__()
        
        self._init_buttons()
        self._init_notebook()
        self._init_tabs()
        
        self._set_layout()
        
    def _init_buttons(self) -> None:
        self.save_button = Button(self, text='Save Changes')
        self.add_student_button = Button(self, text='Add Student')
        self.add_program_button = Button(self, text='Add Program')
    
    def _init_notebook(self) -> None:
        self.notebook = Notebook(self)
    
    def _init_tabs(self) -> None:
        self.student_tab = Frame(self.notebook)
        
        self.student_list = Treeview(
            self.student_tab, 
            columns=('id', 'name', 'year', 'gender', 'program_code'), 
            show='headings', 
            selectmode='browse'
        )
        
        self.student_list.heading(column='id', text='ID')
        self.student_list.heading(column='name', text='Name')
        self.student_list.heading(column='year', text='Year')
        self.student_list.heading(column='gender', text='Gender')
        self.student_list.heading(column='program_code', text='Program')
        
        self.student_list_scrollbar = Scrollbar(
            self.student_tab, 
            orient='vertical', 
            command=self.student_list.yview
        )
             
        self.program_tab = Frame(self.notebook)
        
        self.program_list = Treeview(
            self.program_tab,
            columns=('code', 'name'),
            show='headings',
            selectmode='browse'
        )
        
        self.program_list.heading(column='code', text='Program Code')
        self.program_list.heading(column='name', text='Program Name')
        
        self.program_list_scrollbar = Scrollbar(
            self.program_tab, 
            orient='vertical', 
            command=self.program_list.yview
        )
        
        self.notebook.add(self.student_tab, state='normal', text='Students')
        self.notebook.add(self.program_tab, state='normal', text='Programs')

    def _set_layout(self) -> None:
        self.title('Simple Student Information System')
        self.state('zoomed')
        self.resizable(False, True)
        
        self.rowconfigure(0, weight=100)
        self.rowconfigure(1, weight=1)
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=7)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        
        self.notebook.grid(row=0, column=0, rowspan=1, columnspan=4, sticky='nsew', padx=0, pady=0)
        self.save_button.grid(row=1, column=0, rowspan=1, columnspan=1, sticky='ew', padx=(14, 7), pady=(7, 14))
        self.add_student_button.grid(row=1, column=2, rowspan=1, columnspan=1, sticky='ew', padx=(7, 7), pady=(7, 14))
        self.add_program_button.grid(row=1, column=3, rowspan=1, columnspan=1, sticky='ew', padx=(7, 14), pady=(7, 14))
        
        for tab in (self.student_tab, self.program_tab):
            tab.columnconfigure(0, weight=1000)
            tab.columnconfigure(1, weight=1)
            
            tab.rowconfigure(0, weight=1)
        
        self.student_list.grid(row=0, column=0, rowspan=1, columnspan=1, sticky='nsew', padx=(14, 0), pady=(14, 0))
        self.student_list_scrollbar.grid(row=0, column=1, rowspan=1, columnspan=1, sticky='nsw', padx=(0, 0), pady=(14, 0))
        
        self.program_list.grid(row=0, column=0, rowspan=1, columnspan=1, sticky='nsew', padx=(14, 0), pady=(14, 0))
        self.program_list_scrollbar.grid(row=0, column=1, rowspan=1, columnspan=1, sticky='nsw', padx=(0, 0), pady=(14, 0))
        
        for list in (self.program_list, self.student_list):
            for column in list['columns']:
                list.column(column, anchor='center')
        
        self.style = Style()
        
        self.style.configure('Treeview.Heading', font=FONT_BOLD)
        self.style.configure('Treeview', font=FONT_NORMAL)
        self.style.configure('TButton', font=FONT_BOLD)
        self.style.configure('TNotebook.Tab', font=FONT_BOLD, padding=(5, 5))
        