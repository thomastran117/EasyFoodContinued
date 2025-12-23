from service.comboService import ComboService


class ComboControler:
    def __init__(self, comboservice: ComboService):
        self.combo_service = comboservice
