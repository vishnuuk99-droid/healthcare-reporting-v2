import pandas as pd
from . import DatasourceAdapter, DatasourceValidationError

class ExcelAdapter(DatasourceAdapter):
    def __init__(self, file_path: str):
        self.file_path = file_path
        try:
            self.xl = pd.ExcelFile(self.file_path)
        except Exception as e:
            raise DatasourceValidationError(f"Failed to load Excel file '{self.file_path}': {e}")
            
    def get_schema(self, source_object: str) -> list[str]:
        if source_object not in self.xl.sheet_names:
            raise DatasourceValidationError(f"Sheet '{source_object}' not found in '{self.file_path}'. Available sheets: {self.xl.sheet_names}")
            
        try:
            # Read just the first row to get the columns
            df = self.xl.parse(source_object, nrows=0)
            return list(df.columns)
        except Exception as e:
            raise DatasourceValidationError(f"Failed to read schema from sheet '{source_object}': {e}")
