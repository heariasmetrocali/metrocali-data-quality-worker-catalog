from dataclasses import dataclass


@dataclass
class Connection:
    id: str
    host: str
    reachable: bool = True

    def ping(self) -> bool:
        return self.reachable
