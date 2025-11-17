from service.driverService import DriverService


class DriverController:
    def __init__(self, driver_service: DriverService):
        self.driver_service = driver_service
