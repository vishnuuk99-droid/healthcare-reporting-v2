import json
import urllib.request
from jsonschema import validate, exceptions
from pathlib import Path

def validate_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    schema_url = data.get("$schema")
    if not schema_url:
        print(f"[{file_path.name}] No $schema property found.")
        return
    
    print(f"[{file_path.name}] Downloading schema from {schema_url}...")
    try:
        req = urllib.request.Request(schema_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            schema = json.loads(response.read())
    except Exception as e:
        print(f"  Failed to download schema: {e}")
        return
    
    try:
        validate(instance=data, schema=schema)
        print(f"  [PASS] Validation passed!")
    except exceptions.ValidationError as err:
        print(f"  [FAIL] Validation failed!")
        print(f"     Path: {' -> '.join([str(x) for x in err.absolute_path])}")
        print(f"     Message: {err.message}")

if __name__ == "__main__":
    pbip_dir = Path("projects/8b7f0306-436/output/pbip/Prior_Authorization_Metri.Report")
    
    print("=== Validating Report Level ===")
    validate_json_file(pbip_dir / "definition.pbir")
    validate_json_file(pbip_dir / "definition" / "version.json")
    validate_json_file(pbip_dir / "definition" / "report.json")
    
    print("\n=== Validating Pages ===")
    pages_dir = pbip_dir / "definition" / "pages"
    if pages_dir.exists():
        validate_json_file(pages_dir / "pages.json")
        for page_dir in pages_dir.iterdir():
            if page_dir.is_dir():
                page_json = page_dir / "page.json"
                if page_json.exists():
                    validate_json_file(page_json)
                
                visuals_dir = page_dir / "visuals"
                if visuals_dir.exists():
                    for visual_dir in visuals_dir.iterdir():
                        if visual_dir.is_dir():
                            visual_json = visual_dir / "visual.json"
                            if visual_json.exists():
                                validate_json_file(visual_json)
                                # Just test one visual to prevent spam
                                break
                break
