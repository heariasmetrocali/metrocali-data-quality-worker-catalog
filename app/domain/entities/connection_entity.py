from dataclasses import dataclass


@dataclass
class Connection:
    id: str
    reachable: bool = True

    def ping(self) -> bool:
        return self.reachable
