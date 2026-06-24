class CatalogException(Exception):
    """Domain error for catalog-related business rule violations."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)
