# Regression gate (PowerShell). Run from repository root.

Write-Host "RUNNING REGRESSION GATE"
python -m pytest tests/regression/ @args
if ($LASTEXITCODE -ne 0) {
    Write-Host "REGRESSION FAILED - BLOCK DEPLOY"
    exit $LASTEXITCODE
}
Write-Host "REGRESSION PASSED"
