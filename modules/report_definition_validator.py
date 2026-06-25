"""
Report Definition Validator.

A metadata-driven validation layer that ensures every visual specification
in the report definition satisfies the structural requirements of its target
Power BI visual type.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class VisualRoleRequirement:
    role_name: str
    min_count: int
    max_count: Optional[int] = None

class VisualRuleRegistry:
    def __init__(self):
        self._rules: Dict[str, List[VisualRoleRequirement]] = {}
        
    def register(self, visual_type: str, requirements: List[VisualRoleRequirement]):
        self._rules[visual_type] = requirements
        
    def get_requirements(self, visual_type: str) -> List[VisualRoleRequirement]:
        return self._rules.get(visual_type, [])

# Central registry for visual binding rules
registry = VisualRuleRegistry()

# Note: As binding metadata becomes richer, we can validate roles like "trend_axis", "target", etc.
# Currently, report_definition.json uses "dimensions" and "measures" generically.
# Below, we map logical roles into structural metadata limits.

# KPI requires an Indicator (Measure) and a Trend dimension.
registry.register("kpi", [
    VisualRoleRequirement("measures", 1, 1),
    VisualRoleRequirement("dimensions", 1, 1)
])

# Card requires exactly one Measure.
registry.register("card", [
    VisualRoleRequirement("measures", 1, 1),
    VisualRoleRequirement("dimensions", 0, 0)
])
registry.register("cardVisual", [
    VisualRoleRequirement("measures", 1, 1),
    VisualRoleRequirement("dimensions", 0, 0)
])

# Charts require at least one Dimension (Axis/Category) and one Measure (Values)
for chart_type in ["line_chart", "lineChart", "bar_chart", "barChart", "clustered_bar_chart", "columnChart", "clusteredColumnChart", "donut_chart", "pieChart"]:
    registry.register(chart_type, [
        VisualRoleRequirement("measures", 1),
        VisualRoleRequirement("dimensions", 1)
    ])

# Matrix requires Rows (Dimensions) and Values (Measures)
registry.register("matrix", [
    VisualRoleRequirement("measures", 1),
    VisualRoleRequirement("dimensions", 1)
])
registry.register("pivotTable", [
    VisualRoleRequirement("measures", 1),
    VisualRoleRequirement("dimensions", 1)
])

# Gauge requires a Value (Measure) and optionally a Target/Max/Min (additional Measures)
registry.register("gauge", [
    VisualRoleRequirement("measures", 1, 4), # Value, Target, Min, Max
    VisualRoleRequirement("dimensions", 0, 0)
])


def validate_report_definition(report_def: dict) -> list[str]:
    """
    Validate a report definition's visual specifications against structural requirements.
    
    Args:
        report_def: The generated report definition dictionary.
        
    Returns:
        A list of error strings. Empty list if validation passes.
    """
    errors = []
    
    for page in report_def.get("pages", []):
        page_name = page.get("page_name", "Unknown Page")
        for visual in page.get("visuals", []):
            visual_title = visual.get("title", "Unknown Visual")
            visual_type = visual.get("visual_type", "")
            
            requirements = registry.get_requirements(visual_type)
            if not requirements:
                # Optionally warn on unknown visual types, or skip since the compiler might map it.
                continue
                
            for req in requirements:
                role_items = visual.get(req.role_name, [])
                count = len(role_items)
                
                if count < req.min_count:
                    errors.append(
                        f"Page '{page_name}' -> Visual '{visual_title}' ({visual_type}): "
                        f"Missing required role '{req.role_name}'. Expected at least {req.min_count}, found {count}."
                    )
                if req.max_count is not None and count > req.max_count:
                    errors.append(
                        f"Page '{page_name}' -> Visual '{visual_title}' ({visual_type}): "
                        f"Too many items for role '{req.role_name}'. Expected at most {req.max_count}, found {count}."
                    )
                    
    return errors
