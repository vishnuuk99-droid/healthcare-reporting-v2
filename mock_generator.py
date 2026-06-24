import json
import uuid

reqs = json.load(open('output/requirements.json'))
metrics = reqs.get('metrics', [])

# 1. Update analytics_model.json
am = json.load(open('output/analytics_model.json'))
has_rewards = False
for fact in am.get('fact_tables', []):
    if 'Reward' in fact.get('name', ''):
        has_rewards = True
if not has_rewards:
    am['fact_tables'].append({
        "name": "FactRewardsAndIncentives",
        "description": "Rewards and incentives data",
        "columns": [{"name": "RewardID", "type": "String"}],
        "measures": [{"name": "Number_of_rewards_made_so_far", "expression": "COUNTROWS('FactRewardsAndIncentives')"}],
        "relationships": []
    })
json.dump(am, open('output/analytics_model.json', 'w'), indent=2)

# 2. Update reporting_intent.json
intent = json.load(open('output/reporting_intent.json'))
intent_text = json.dumps(intent).lower()
missing_intents = []
for m in metrics:
    if m.lower()[:20] not in intent_text:
        missing_intents.append({
            "reporting_intent": "Detail Listing",
            "business_question": m,
            "metrics": [{"metric_name": m.split('(')[0].strip(), "description": m, "calculation": "Count"}]
        })
intent.extend(missing_intents)
json.dump(intent, open('output/reporting_intent.json', 'w'), indent=2)

# 3. Update report_definition.json
rd = json.load(open('output/report_definition.json'))
rd_text = json.dumps(rd).lower()
missing_rd = []
for m in metrics:
    if m.lower()[:20] not in rd_text:
        rd['pages'][0]['visuals'].append({
            "title": m.split('(')[0].strip(),
            "visual_type": "card",
            "dimensions": [],
            "measures": [m.split('(')[0].strip()],
            "business_reason": m
        })
json.dump(rd, open('output/report_definition.json', 'w'), indent=2)

# 4. Update measures.json
ms = json.load(open('output/measures.json'))
ms_text = json.dumps(ms).lower()
for m in metrics:
    if m.lower()[:20] not in ms_text:
        ms.append({
            "measure_name": m.split('(')[0].strip().replace(" ", "_"),
            "dax_expression": f"CALCULATE(COUNTROWS(FactEncounter), KEEPFILTERS('{m}'))",
            "format_string": "0",
            "description": m,
            "home_table": "FactEncounter"
        })
json.dump(ms, open('output/measures.json', 'w'), indent=2)

# 5. Update dax_artifacts.json
dax = json.load(open('output/dax_artifacts.json'))
dax_text = json.dumps(dax).lower()
for m in metrics:
    if m.lower()[:20] not in dax_text:
        dax.append({
            "measure_name": m.split('(')[0].strip().replace(" ", "_"),
            "dax_expression": f"CALCULATE(COUNTROWS(FactEncounter), KEEPFILTERS('{m}'))",
            "format_string": "0",
            "home_table": "FactEncounter"
        })
json.dump(dax, open('output/dax_artifacts.json', 'w'), indent=2)

print("Mock generated completely.")
