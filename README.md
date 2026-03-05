# Model Risk Scorecard (MRM)

Mini framework em Python para **Model Risk Management (MRM)** aplicado a modelos de Machine Learning.

O projeto demonstra como estruturar:

- Inventário de modelos
- Classificação de risco (Tiering)
- Definição de métricas e thresholds
- Validação independente
- Scorecard de risco do modelo

Este tipo de estrutura é utilizado em instituições financeiras e empresas de tecnologia para governança e monitoramento do ciclo de vida de modelos.

---

# Estrutura do projeto

model-risk-scorecard/

data/
inventory.csv
sample_predictions.csv

config/
tiering_rules.yaml
thresholds.yaml

src/
tiering.py
validate.py

reports/
scorecard.md

---

# Inventário de modelos

O arquivo:

data/inventory.csv

define os modelos da organização e seus atributos:

- materialidade
- complexidade
- uso
- dados sensíveis
- responsável

Essas variáveis são usadas para calcular o **tier de risco**.

---

# Tiering de modelos

Score de risco:

score = materiality + complexity + usage

Classificação:

Tier 1 — alto risco  
Tier 2 — risco médio  
Tier 3 — baixo risco  

Modelos de maior risco exigem ciclos de validação mais frequentes.

---

# Validação de modelos

O script:

src/validate.py

executa validação baseada em thresholds definidos em:

config/thresholds.yaml

Exemplos de métricas avaliadas:

Classificação
- AUC
- F1 score
- fairness (TPR gap)

Regressão
- RMSE
- MAPE

---

# Scorecard

O resultado da validação gera um relatório:

reports/scorecard.md

O scorecard inclui:

- Tier do modelo
- Métricas avaliadas
- Status PASS/FAIL
- Recomendações operacionais

---

# Como executar

Criar ambiente virtual

python -m venv .venv

Ativar ambiente

.venv\Scripts\activate

Instalar dependências

pip install -r requirements.txt

Executar validação

python src/validate.py

---

# Objetivo do projeto

Demonstrar um exemplo simples de **governança e validação de modelos** dentro de um framework de Model Risk Management.