# Runner do projeto (Windows PowerShell)
# 1) Ativa venv
# 2) Instala dependências
# 3) Executa tiering
# 4) Executa validação e gera scorecard
# 5) Mostra o scorecard no terminal

$ErrorActionPreference = "Stop"

if (!(Test-Path ".\.venv\Scripts\Activate.ps1")) {
  Write-Host "Virtual env nao encontrado. Criando .venv..."
  python -m venv .venv
}

.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip | Out-Null
pip install -r requirements.txt | Out-Null

python .\src\tiering.py
python .\src\validate.py

Write-Host "`n--- SCORECARD ---`n"
type .\reports\scorecard.md