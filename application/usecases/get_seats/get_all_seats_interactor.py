# usecases/get_all_seats_interactor.py

from typing import List
from domain.entities.seat import Seat
from adapters.gateways.get_seats.seats_reader_gateway import ISeatsReaderGateway

class GetAllSeatsUseCase:
    def __init__(self, seat_reader: ISeatsReaderGateway):
        self.seat_reader = seat_reader

    def execute(self) -> List[Seat]:
        return self.seat_reader.fetch_all_seats()
