from abc import ABC, abstractmethod
from scrapers.ShiftCode import ShiftCode


class BaseScraper(ABC):
    PATTERN = r"[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}"

    @abstractmethod
    def find_codes(self) -> list[ShiftCode]:
        """
        Returns list of ShiftCode Objects
        """
        pass