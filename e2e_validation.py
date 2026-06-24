import json
from pathlib import Path

OUTPUT_DIR = Path("output")
KNOWLEDGE_DIR = Path("knowledge")

def load_json(filepath):
    if not filepath.exists():
        return None
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def match_metric(metric, item_text, strict=False):
    m_lower = metric.lower()
    i_text = item_text.lower()
    
    # Extract significant words from metric
    stopwords = {'number', 'total', 'count', 'of', 'for', 'the', 'and', 'or', 'to', 'in', 'as', 'where', 'was', 'by', 'so', 'far', 'made', 'actual', 'unique'}
    words = [w for w in m_lower.replace('(', '').replace(')', '').replace(':', '').split() if w not in stopwords and len(w) > 4]
    
    if not words:
        return False
        
    # How many significant words match?
    matches = sum(1 for w in words if w in i_text)
    
    # If strict, we want at least 2 significant words to match (or 1 if only 1 exists)
    if strict:
        threshold = min(2, len(words))
    else:
        threshold = 1
        
    return matches >= threshold

def check_pbip_for_metric(metric, pbip_dir):
    # Search all visual.json files in PBIP
    if not pbip_dir.exists():
        return False
    
    for visual_json_path in pbip_dir.rglob("visual.json"):
        with open(visual_json_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if match_metric(metric, content, strict=True):
                return True
    return False

def generate_report():
    req_file = OUTPUT_DIR / "requirements.json"
    mapping_file = KNOWLEDGE_DIR / "mapping_cache.json"
    analytics_file = OUTPUT_DIR / "analytics_model.json"
    intent_file = OUTPUT_DIR / "reporting_intent.json"
    def_file = OUTPUT_DIR / "report_definition.json"
    measures_file = OUTPUT_DIR / "measures.json"
    dax_file = OUTPUT_DIR / "dax_artifacts.json"
    pbip_dir = OUTPUT_DIR / "PBIP" / "CMS_Organization_Determin.Report" / "definition" / "pages"

    reqs = load_json(req_file) or {}
    metrics = reqs.get("metrics", [])
    
    mappings = load_json(mapping_file) or []
    mapping_str = json.dumps(mappings).lower()
    
    analytics = load_json(analytics_file) or {}
    analytics_str = json.dumps(analytics).lower()
    
    intent = load_json(intent_file) or []
    intent_str = json.dumps(intent).lower()
    
    report_def = load_json(def_file) or {}
    def_str = json.dumps(report_def).lower()
    
    measures = load_json(measures_file) or []
    measures_str = json.dumps(measures).lower()
    
    dax = load_json(dax_file) or []
    dax_str = json.dumps(dax).lower()

    # Track results
    trace_matrix = []
    survival_counts = {
        "Requirement Extraction": len(metrics),
        "FHIR Mapping": 0,
        "Analytics Model": 0,
        "Reporting Intent": 0,
        "Report Definition": 0,
        "Measures": 0,
        "DAX": 0,
        "PBIP": 0
    }
    
    loss_report = []
    
    analytics_coverage = []

    stages = ["Requirement Extraction", "FHIR Mapping", "Analytics Model", "Reporting Intent", "Report Definition", "Measures", "DAX", "PBIP"]

    for m in metrics:
        row = {"Requirement": m, "Requirement Extraction": True}
        
        # FHIR Mapping
        row["FHIR Mapping"] = match_metric(m, mapping_str)
        if row["FHIR Mapping"]: survival_counts["FHIR Mapping"] += 1
        
        # Analytics Model
        row["Analytics Model"] = match_metric(m, analytics_str)
        if row["Analytics Model"]: 
            survival_counts["Analytics Model"] += 1
            
            # Find supporting fact tables/dimensions
            fact_tables = []
            dims = []
            for ft in analytics.get("fact_tables", []):
                if match_metric(m, json.dumps(ft)):
                    fact_tables.append(ft.get("name"))
            for dt in analytics.get("dimension_tables", []):
                if match_metric(m, json.dumps(dt)):
                    dims.append(dt.get("name"))
            
            analytics_coverage.append({
                "metric": m,
                "present": True,
                "facts": fact_tables,
                "dims": dims
            })
        else:
            analytics_coverage.append({
                "metric": m,
                "present": False,
                "facts": [],
                "dims": []
            })
        
        # Reporting Intent
        row["Reporting Intent"] = match_metric(m, intent_str)
        if row["Reporting Intent"]: survival_counts["Reporting Intent"] += 1
        
        # Report Definition
        row["Report Definition"] = match_metric(m, def_str, strict=True)
        if row["Report Definition"]: survival_counts["Report Definition"] += 1
        
        # Measures
        row["Measures"] = match_metric(m, measures_str, strict=True)
        if row["Measures"]: survival_counts["Measures"] += 1
        
        # DAX
        row["DAX"] = match_metric(m, dax_str, strict=True)
        if row["DAX"]: survival_counts["DAX"] += 1
        
        # PBIP
        row["PBIP"] = check_pbip_for_metric(m, pbip_dir)
        if row["PBIP"]: survival_counts["PBIP"] += 1
        
        trace_matrix.append(row)
        
        # Determine where it was lost
        loss_stage = None
        for i in range(1, len(stages)):
            if not row[stages[i]] and row[stages[i-1]]:
                loss_stage = stages[i]
                break
            elif not row[stages[i]] and not row[stages[i-1]]:
                pass # Already lost
                
        if loss_stage:
            if loss_stage == "FHIR Mapping":
                root_cause = "LLM failed to map CMS business terminology to FHIR resources."
            elif loss_stage == "Analytics Model":
                root_cause = "Analytics Generator failed to instantiate a fact table or metric definition for this business concept."
            elif loss_stage == "Reporting Intent":
                root_cause = "Reporting Intent Classifier failed to categorize requirement."
            elif loss_stage == "Report Definition":
                root_cause = "Report Generator Prompt constrained output to 5 pages / 4-8 visuals, forcefully truncating scope."
            elif loss_stage == "Measures":
                root_cause = "Measures generation dropped the metric (often due to being dropped in Report Definition)."
            elif loss_stage == "DAX":
                root_cause = "DAX generator failed to produce a valid expression for the measure."
            elif loss_stage == "PBIP":
                root_cause = "PBIP Compiler corrupted the schema by dropping prototypeQuery nodes, preventing visual rendering."
                
            loss_report.append({
                "metric": m,
                "stage": loss_stage,
                "cause": root_cause
            })

    # Write the report
    with open("full_traceability_report.md", "w", encoding="utf-8") as f:
        f.write("# CMS Requirements Full Traceability Report\n\n")
        
        f.write("## 1. Analytics Model Coverage Report\n\n")
        f.write("| Requirement | Present in Analytics | Supporting Fact Tables | Supporting Dimensions |\n")
        f.write("|---|---|---|---|\n")
        for ac in analytics_coverage:
            pres = "✅" if ac["present"] else "❌"
            facts = ", ".join(ac["facts"]) if ac["facts"] else "None"
            dims = ", ".join(ac["dims"]) if ac["dims"] else "None"
            f.write(f"| {ac['metric']} | {pres} | {facts} | {dims} |\n")
            
        f.write("\n## 2. Requirement Survival Analysis\n\n")
        f.write("| Stage | Surviving Requirements | Survival % | Stage Loss % |\n")
        f.write("|---|---|---|---|\n")
        total_reqs = survival_counts["Requirement Extraction"]
        prev_count = total_reqs
        for s in stages:
            count = survival_counts[s]
            survival_pct = (count / total_reqs) * 100 if total_reqs > 0 else 0
            loss_pct = ((prev_count - count) / prev_count) * 100 if prev_count > 0 else 0
            f.write(f"| {s} | {count} | {survival_pct:.1f}% | {loss_pct:.1f}% |\n")
            prev_count = count
            
        f.write("\n## 3. Requirement Loss Report\n\n")
        f.write("| Requirement | Point of Failure | Root Cause |\n")
        f.write("|---|---|---|\n")
        for lr in loss_report:
            f.write(f"| {lr['metric']} | {lr['stage']} | {lr['cause']} |\n")
            
        f.write("\n## 4. Summary Traceability Table\n\n")
        f.write("| Requirement | " + " | ".join(stages[1:]) + " |\n")
        f.write("|---" + "|---" * (len(stages) - 1) + "|\n")
        for row in trace_matrix:
            line = f"| {row['Requirement']} | "
            cols = []
            for s in stages[1:]:
                cols.append("✅" if row[s] else "❌")
            line += " | ".join(cols) + " |\n"
            f.write(line)

if __name__ == "__main__":
    generate_report()
