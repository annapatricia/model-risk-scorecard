import os
import json
import pandas as pd
import numpy as np
import yaml

from sklearn.metrics import roc_auc_score, f1_score, mean_squared_error

def load_yaml(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def classification_metrics(df: pd.DataFrame):
    y_true = df["y_true"].astype(int).to_numpy()
    y_pred = df["y_pred"].astype(float).to_numpy()

    # threshold fixo simples (0.5) para F1
    y_hat = (y_pred >= 0.5).astype(int)

    auc = roc_auc_score(y_true, y_pred)
    f1 = f1_score(y_true, y_hat)

    # fairness simples: TPR gap entre grupos A e B
    tpr = {}
    for g in sorted(df["group"].unique()):
        sub = df[df["group"] == g]
        yt = sub["y_true"].astype(int).to_numpy()
        yp = (sub["y_pred"].astype(float).to_numpy() >= 0.5).astype(int)
        tp = np.sum((yp == 1) & (yt == 1))
        fn = np.sum((yp == 0) & (yt == 1))
        tpr[g] = tp / (tp + fn) if (tp + fn) > 0 else 0.0

    groups = sorted(tpr.keys())
    tpr_gap = abs(tpr[groups[0]] - tpr[groups[1]]) if len(groups) >= 2 else 0.0

    return {
        "auc": float(auc),
        "f1": float(f1),
        "tpr_by_group": {k: float(v) for k, v in tpr.items()},
        "tpr_gap": float(tpr_gap),
    }


def regression_metrics(df: pd.DataFrame):
    y_true = df["y_true"].astype(float).to_numpy()
    y_pred = df["y_pred"].astype(float).to_numpy()

    mse = mean_squared_error(y_true, y_pred)
    rmse = float(np.sqrt(mse))
    mape = float(np.mean(np.abs((y_true - y_pred) / np.maximum(np.abs(y_true), 1e-9))))
    return {"rmse": float(rmse), "mape": float(mape)}


def check_thresholds(model_type: str, metrics: dict, thresholds: dict):
    results = []

    if model_type == "classification":
        cfg = thresholds["classification"]
        results.append(("auc", metrics["auc"], ">=", cfg["auc_min"], metrics["auc"] >= cfg["auc_min"]))
        results.append(("f1", metrics["f1"], ">=", cfg["f1_min"], metrics["f1"] >= cfg["f1_min"]))

        fair = thresholds["fairness"]
        results.append(("tpr_gap", metrics["tpr_gap"], "<=", fair["max_tpr_gap"], metrics["tpr_gap"] <= fair["max_tpr_gap"]))

    elif model_type == "regression":
        cfg = thresholds["regression"]
        results.append(("rmse", metrics["rmse"], "<=", cfg["max_rmse"], metrics["rmse"] <= cfg["max_rmse"]))
        results.append(("mape", metrics["mape"], "<=", cfg["max_mape"], metrics["mape"] <= cfg["max_mape"]))

    else:
        raise ValueError(f"Unknown model_type: {model_type}")

    overall_pass = all(r[-1] for r in results)
    return overall_pass, results


def main():
    base_dir = os.path.dirname(os.path.dirname(__file__))

    thresholds = load_yaml(os.path.join(base_dir, "config", "thresholds.yaml"))

    preds_path = os.path.join(base_dir, "data", "sample_predictions.csv")
    df = pd.read_csv(preds_path)

    report = {"models": []}

    for model_id in sorted(df["model_id"].unique()):
        mdf = df[df["model_id"] == model_id].copy()

        # inferir tipo: se y_pred está entre 0 e 1 -> classification; senão regression
        yp = mdf["y_pred"].astype(float)
        model_type = "classification" if ((yp >= 0).all() and (yp <= 1).all()) else "regression"

        if model_type == "classification":
            metrics = classification_metrics(mdf)
        else:
            metrics = regression_metrics(mdf)

        ok, checks = check_thresholds(model_type, metrics, thresholds)

        report["models"].append(
            {
                "model_id": model_id,
                "model_type": model_type,
                "metrics": metrics,
                "checks": [
                    {"metric": c[0], "value": c[1], "op": c[2], "threshold": c[3], "pass": c[4]}
                    for c in checks
                ],
                "overall_pass": bool(ok),
            }
        )

    os.makedirs(os.path.join(base_dir, "reports"), exist_ok=True)

    out_json = os.path.join(base_dir, "reports", "validation_report.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    # report markdown (evitar emojis para não quebrar encoding em alguns terminais)
    out_md = os.path.join(base_dir, "reports", "scorecard.md")

    # carregar inventário e tiering para enriquecer o relatório
    inv_path = os.path.join(base_dir, "data", "inventory.csv")
    inv = pd.read_csv(inv_path)

    rules = load_yaml(os.path.join(base_dir, "config", "tiering_rules.yaml"))
    tier1_min = int(rules["tier_rules"]["tier1_min_score"])
    tier2_min = int(rules["tier_rules"]["tier2_min_score"])

    def calc_tier(materiality, complexity, usage):
        score = int(materiality) + int(complexity) + int(usage)
        if score >= tier1_min:
            return score, "Tier 1"
        if score >= tier2_min:
            return score, "Tier 2"
        return score, "Tier 3"

    def revalidation_freq(tier: str) -> str:
        if tier == "Tier 1":
            return "Mensal (ou após mudança relevante)"
        if tier == "Tier 2":
            return "Trimestral"
        return "Semestral"

    lines = ["# Model Risk Scorecard (MVP)\n"]
    lines.append("Este relatório consolida validação técnica + fairness básica, com base em thresholds operacionais.\n\n")

    # ordenar por tier e depois por nome
    enriched = []
    for m in report["models"]:
        row = inv[inv["model_id"] == m["model_id"]].iloc[0]
        score, tier = calc_tier(row["materiality"], row["complexity"], row["usage"])
        enriched.append((tier, score, m))
    enriched.sort(key=lambda x: (x[0], -x[1], x[2]["model_id"]))

    for tier, tier_score, m in enriched:
        status = "PASS" if m["overall_pass"] else "FAIL"
        lines.append(f"## {m['model_id']} — {m['model_type']} — {status}\n")
        lines.append(f"- Tier: **{tier}** (score={tier_score})\n")
        lines.append(f"- Revalidação recomendada: **{revalidation_freq(tier)}**\n\n")
        lines.append("### Checks\n")
        for c in m["checks"]:
            icon = "[OK]" if c["pass"] else "[FAIL]"
            val = c["value"]
            if isinstance(val, (int, float)):
                lines.append(f"- {icon} `{c['metric']}`: {val:.4f} {c['op']} {c['threshold']}\n")
            else:
                lines.append(f"- {icon} `{c['metric']}`: {val} {c['op']} {c['threshold']}\n")
        lines.append("\n")

        lines.append("### Recomendação\n")
        if m["overall_pass"]:
            lines.append("- Manter em produção dentro do ciclo de revalidação sugerido e monitorar métricas.\n\n")
        else:
            lines.append("- Bloquear promoção/uso, abrir ação corretiva e revalidar após ajuste.\n\n")

    with open(out_md, "w", encoding="utf-8") as f:
        f.writelines(lines)
        f.writelines(lines)

    print(f"\nGerado: {out_md}")
    print(f"Gerado: {out_json}\n")


if __name__ == "__main__":
    main()