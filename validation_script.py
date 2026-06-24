import json
from pathlib import Path

OUTPUT_DIR = Path("output")

def load_json(filepath):
    if not filepath.exists():
        return {}
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def run_traceability():
    req_file = OUTPUT_DIR / "requirements.json"
    intent_file = OUTPUT_DIR / "reporting_intent.json"
    def_file = OUTPUT_DIR / "report_definition.json"

    requirements = load_json(req_file)
    intent = load_json(intent_file)
    report_def = load_json(def_file)

    metrics = requirements.get("metrics", [])
    
    # Intent is a list of dictionaries
    intent_items = intent
    
    def_visuals = []
    for page in report_def.get("pages", []):
        for v in page.get("visuals", []):
            def_visuals.append(v.get("title", ""))
            
    with open("requirements_matrix.md", "w", encoding="utf-8") as f:
        f.write("# Requirement Traceability Matrix\n\n")
        f.write("| CMS Requirement | Present in Intent | Present in Report Definition | Status |\n")
        f.write("|---|---|---|---|\n")
        
        total = len(metrics)
        in_intent = 0
        in_def = 0
        
        for m in metrics:
            m_lower = m.lower()
            
            found_in_intent = False
            for i in intent_items:
                i_text = str(i).lower()
                if any(word in i_text for word in m_lower.split() if len(word) > 5):
                    found_in_intent = True
                    break
                    
            found_in_def = False
            for v in def_visuals:
                if any(word in v.lower() for word in m_lower.split() if len(word) > 5 and word not in ['number', 'total', 'count']):
                    found_in_def = True
                    break
                    
            if found_in_intent: in_intent += 1
            if found_in_def: in_def += 1
            status = "Full" if found_in_intent and found_in_def else ("Partial Drop" if found_in_intent else "Dropped")
            
            f.write(f"| {m} | {found_in_intent} | {found_in_def} | {status} |\n")

        f.write(f"\n**Summary**: {in_intent}/{total} requirements passed to Reporting Intent. {in_def}/{total} requirements passed to Report Definition.\n")

if __name__ == "__main__":
    run_traceability()
