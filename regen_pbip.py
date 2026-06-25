import sys
from pathlib import Path
import modules.file_manager as fm

# Patch OUTPUT_DIR before importing pbip_generator
target_output = Path("projects/8b7f0306-436/output").resolve()
fm.OUTPUT_DIR = target_output

import modules.pbip_generator as pg
pg._ANALYTICS_MODEL_FILE = target_output / "analytics_model.json"
pg._REPORT_DEFINITION_FILE = target_output / "report_definition.json"
pg._INTENT_FILE = target_output / "reporting_intent.json"
pg._DATA_DICTIONARY_FILE = target_output / "data_dictionary.json"
pg._MEASURES_FILE = target_output / "measures.json"
pg._DAX_ARTIFACTS_FILE = target_output / "dax_artifacts.json"
pg._PBIP_DIR = target_output / "pbip"
pg._ZIP_FILE = target_output / "pbip_project.zip"
pg._REPORT_LAYOUT_FILE = target_output / "report_layout.json"
pg._REPORT_VISUALS_FILE = target_output / "report_visuals.json"

print("Compiling PBIP Project...")
config_path = Path("user_datasource_config.json").resolve()
config_arg = str(config_path) if config_path.exists() else None
result = pg.compile_pbip_project(datasource_config_path=config_arg)
print(f"Success: {result['is_valid']}")
print(f"ZIP Path: {result['zip_path']}")
