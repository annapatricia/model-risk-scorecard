import csv
import os
from dataclasses import dataclass
from typing import Dict, List

import yaml


@dataclass
class ModelRow:
    model_id: str
    model_type: str
    business_use: str
    materiality: int
    complexity: int
    usage: int
    is_automated_decision: str
    sensitive_data: str
    owner: str
    last_validated: str

    @property
    def tier_score(self) -> int:
        return int(self.materiality) + int(self.complexity) + int(self.usage)


def load_yaml(path: str) -> Dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_inventory(path: str) -> List[ModelRow]:
    rows: List[ModelRow] = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(
                ModelRow(
                    model_id=r["model_id"],
                    model_type=r["model_type"],
                    business_use=r["business_use"],
                    materiality=int(r["materiality"]),
                    complexity=int(r["complexity"]),
                    usage=int(r["usage"]),
                    is_automated_decision=r["is_automated_decision"],
                    sensitive_data=r["sensitive_data"],
                    owner=r["owner"],
                    last_validated=r["last_validated"],
                )
            )
    return rows


def assign_tier(score: int, rules: Dict) -> str:
    tier_rules = rules["tier_rules"]
    if score >= int(tier_rules["tier1_min_score"]):
        return "Tier 1"
    if score >= int(tier_rules["tier2_min_score"]):
        return "Tier 2"
    return "Tier 3"


def main() -> None:
    base_dir = os.path.dirname(os.path.dirname(__file__))
    inventory_path = os.path.join(base_dir, "data", "inventory.csv")
    rules_path = os.path.join(base_dir, "config", "tiering_rules.yaml")

    rules = load_yaml(rules_path)
    inventory = load_inventory(inventory_path)

    print("\nMODEL INVENTORY (WITH TIERING)\n")
    print(f"{'model_id':<20} {'score':<5} {'tier':<7} {'use':<18} {'type':<13} {'owner'}")
    print("-" * 80)
    for m in inventory:
        tier = assign_tier(m.tier_score, rules)
        print(f"{m.model_id:<20} {m.tier_score:<5} {tier:<7} {m.business_use:<18} {m.model_type:<13} {m.owner}")

    print("\nDone.\n")


if __name__ == "__main__":
    main()