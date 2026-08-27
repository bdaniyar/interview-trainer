from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class BookingWindow:
    start: int
    end: int

    def __post_init__(self):
        if self.end <= self.start:
            raise ValueError("end must be after start")

    @property
    def duration(self):
        return self.end - self.start
