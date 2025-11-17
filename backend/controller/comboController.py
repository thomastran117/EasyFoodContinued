from service.comboService import ComboService


class ComboControler:
    def __init__(self, combo_service: ComboService):
        self.combo_service = combo_service
