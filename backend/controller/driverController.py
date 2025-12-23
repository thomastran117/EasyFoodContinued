from service.driverService import DriverService


class DriverController:
    def __init__(self, driverservice: DriverService):
        self.driver_service = driverservice
