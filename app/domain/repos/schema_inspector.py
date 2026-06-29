from abc import ABC, abstractmethod

from app.domain.value_objects.schema_inspection import InspectedTable


class SchemaInspector(ABC):
    @abstractmethod
    def inspect(self, connection_id: str) -> list[InspectedTable]:
        pass
