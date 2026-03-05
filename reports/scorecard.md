# Model Risk Scorecard (MVP)
Este relatório consolida validação técnica + fairness básica, com base em thresholds operacionais.

## credit_scoring_v1 — classification — PASS
- Tier: **Tier 1** (score=14)
- Revalidação recomendada: **Mensal (ou após mudança relevante)**

### Checks
- [OK] `auc`: 1.0000 >= 0.75
- [OK] `f1`: 1.0000 >= 0.6
- [OK] `tpr_gap`: 0.0000 <= 0.05

### Recomendação
- Manter em produção dentro do ciclo de revalidação sugerido e monitorar métricas.

## fraud_detector_v2 — classification — PASS
- Tier: **Tier 1** (score=12)
- Revalidação recomendada: **Mensal (ou após mudança relevante)**

### Checks
- [OK] `auc`: 1.0000 >= 0.75
- [OK] `f1`: 1.0000 >= 0.6
- [OK] `tpr_gap`: 0.0000 <= 0.05

### Recomendação
- Manter em produção dentro do ciclo de revalidação sugerido e monitorar métricas.

## demand_forecast_v1 — regression — PASS
- Tier: **Tier 2** (score=8)
- Revalidação recomendada: **Trimestral**

### Checks
- [OK] `rmse`: 5.6679 <= 20
- [OK] `mape`: 0.0476 <= 0.2

### Recomendação
- Manter em produção dentro do ciclo de revalidação sugerido e monitorar métricas.

# Model Risk Scorecard (MVP)
Este relatório consolida validação técnica + fairness básica, com base em thresholds operacionais.

## credit_scoring_v1 — classification — PASS
- Tier: **Tier 1** (score=14)
- Revalidação recomendada: **Mensal (ou após mudança relevante)**

### Checks
- [OK] `auc`: 1.0000 >= 0.75
- [OK] `f1`: 1.0000 >= 0.6
- [OK] `tpr_gap`: 0.0000 <= 0.05

### Recomendação
- Manter em produção dentro do ciclo de revalidação sugerido e monitorar métricas.

## fraud_detector_v2 — classification — PASS
- Tier: **Tier 1** (score=12)
- Revalidação recomendada: **Mensal (ou após mudança relevante)**

### Checks
- [OK] `auc`: 1.0000 >= 0.75
- [OK] `f1`: 1.0000 >= 0.6
- [OK] `tpr_gap`: 0.0000 <= 0.05

### Recomendação
- Manter em produção dentro do ciclo de revalidação sugerido e monitorar métricas.

## demand_forecast_v1 — regression — PASS
- Tier: **Tier 2** (score=8)
- Revalidação recomendada: **Trimestral**

### Checks
- [OK] `rmse`: 5.6679 <= 20
- [OK] `mape`: 0.0476 <= 0.2

### Recomendação
- Manter em produção dentro do ciclo de revalidação sugerido e monitorar métricas.

