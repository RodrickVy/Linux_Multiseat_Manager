from abc import ABC, abstractmethod
from typing import List
from domain.entities.seat import Seat

class ISeatsReaderGateway(ABC):
    @abstractmethod
    def fetch_all_seats(self) -> List[Seat]:
        pass
