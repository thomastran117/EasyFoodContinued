from service.employeeService import EmployeeService


class EmployeeController:
    def __init__(self, employeeservice: EmployeeService):
        self.employee_service = employeeservice
