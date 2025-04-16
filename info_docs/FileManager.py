from utils.pathes import *

class FileManager:
    def __init__(self, costs_path: str, military_path: str, students_path: str):
        self.costs_path = costs_path
        self.military_path = military_path
        self.students_path = students_path

    def payment_order(self):
        return open(self.costs_path, 'rb')

    def military_order(self):
        return open(self.military_path, 'rb')

    def students_list(self):
        return open(self.students_path, 'rb')
    
file_manager_instance = FileManager(
    costs_order_path, 
    military_order_path, 
    students_list_path
)