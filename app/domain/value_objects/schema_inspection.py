from dataclasses import dataclass, field


@dataclass(frozen=True)
class InspectedColumn:
    name: str
    data_type: str


@dataclass(frozen=True)
class InspectedTable:
    name: str
    columns: list[InspectedColumn] = field(default_factory=list)
