$ErrorActionPreference = "Stop"

$project = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $project

$python = Get-Command py -ErrorAction SilentlyContinue
if (-not $python) {
    $python = Get-Command python -ErrorAction SilentlyContinue
}
if (-not $python) {
    throw "No se encontró Python. Instala Python y Playwright para actualizar el catálogo."
}

& $python.Source scraper_productos.py
if ($LASTEXITCODE -ne 0) {
    throw "El scraper terminó con código $LASTEXITCODE."
}
