from service.employeeService import EmployeeService


class EmployeeController:
    def __init__(self, employee_service: EmployeeService):
        self.employee_service = employee_service
