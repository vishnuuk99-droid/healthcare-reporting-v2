from abc import ABC, abstractmethod

class DatasourceValidationError(Exception):
    pass

class DatasourceAdapter(ABC):
    @abstractmethod
    def get_schema(self, source_object: str) -> list[str]:
        """
        Returns a list of physical column names present in the specified source_object 
        (e.g., an Excel sheet name or a SQL table name).
        """
        pass

def get_adapter(config: dict) -> DatasourceAdapter:
    source_type = config.get("source_type", "").lower()
    
    if source_type == "excel":
        from .excel_adapter import ExcelAdapter
        file_path = config.get("file_path")
        if not file_path:
            raise DatasourceValidationError("Excel configuration is missing 'file_path'.")
        return ExcelAdapter(file_path)
    
    raise DatasourceValidationError(f"Unsupported source_type: '{source_type}'")
