from application.usecases.get_seats.get_all_seats_interactor import GetAllSeatsUseCase
from adapters.gateways.get_seats.systemd_seats_reader import SystemdSeatReader

class SeatsController:
    def __init__(self):
        self.use_case = GetAllSeatsUseCase(SystemdSeatReader())

    def list_seats(self):
        return self.use_case.execute()
