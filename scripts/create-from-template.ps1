#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Crea un nuevo repositorio desde un template de scaffolder cuando la GitHub App no tiene permisos.

.DESCRIPTION
    Este script automatiza la creación manual de repositorios usando los templates de scaffolder
    cuando Roadie no puede crear repos por falta de permisos de la GitHub App.

.PARAMETER TemplateName
    Nombre del template: nodejs-api, angular-component, o spring-boot-service

.PARAMETER ProjectName
    Nombre del nuevo proyecto/repositorio

.PARAMETER Description
    Descripción del proyecto

.PARAMETER Owner
    Owner del componente en Backstage (ej: team-eulen-backend)

.PARAMETER Port
    Puerto (solo para nodejs-api, default: 3000)

.EXAMPLE
    .\create-from-template.ps1 -TemplateName nodejs-api -ProjectName Vivo -Description "API de ejemplo" -Owner team-eulen-backend
#>

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("nodejs-api", "angular-component", "spring-boot-service")]
    [string]$TemplateName,
    
    [Parameter(Mandatory=$true)]
    [string]$ProjectName,
    
    [Parameter(Mandatory=$true)]
    [string]$Description,
    
    [Parameter(Mandatory=$false)]
    [string]$Owner = "team-eulen-backend",
    
    [Parameter(Mandatory=$false)]
    [int]$Port = 3000
)

$ErrorActionPreference = "Stop"

# Configuración
$GitHubOwner = "AngC1"
$TemplateRepo = "Roadie"
$WorkDir = "E:\_DevOps"
$SkeletonPath = "$WorkDir\MCP\scaffolder-templates\skeleton\$TemplateName"

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Creando proyecto desde template" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Template:    $TemplateName" -ForegroundColor Yellow
Write-Host "Proyecto:    $ProjectName" -ForegroundColor Yellow
Write-Host "Descripción: $Description" -ForegroundColor Yellow
Write-Host "Owner:       $Owner" -ForegroundColor Yellow
if ($TemplateName -eq "nodejs-api") {
    Write-Host "Puerto:      $Port" -ForegroundColor Yellow
}
Write-Host ""

# Verificar que existe el skeleton
if (-not (Test-Path $SkeletonPath)) {
    Write-Error "El template '$TemplateName' no existe en $SkeletonPath"
    exit 1
}

# Paso 1: Crear repositorio en GitHub
Write-Host "[1/5] Creando repositorio en GitHub..." -ForegroundColor Green
try {
    gh repo create "$GitHubOwner/$ProjectName" --public --description $Description
    Write-Host "  ✓ Repositorio creado: https://github.com/$GitHubOwner/$ProjectName" -ForegroundColor Green
} catch {
    Write-Error "Error creando repositorio. ¿Tienes GitHub CLI instalado y autenticado? Ejecuta: gh auth login"
    exit 1
}

# Paso 2: Clonar el nuevo repositorio
Write-Host "[2/5] Clonando repositorio..." -ForegroundColor Green
$ProjectPath = "$WorkDir\$ProjectName"
if (Test-Path $ProjectPath) {
    Write-Host "  ! El directorio $ProjectPath ya existe. Eliminándolo..." -ForegroundColor Yellow
    Remove-Item -Path $ProjectPath -Recurse -Force
}

Set-Location $WorkDir
gh repo clone "$GitHubOwner/$ProjectName"
Set-Location $ProjectPath

# Paso 3: Copiar archivos del template
Write-Host "[3/5] Copiando archivos del template..." -ForegroundColor Green
Get-ChildItem -Path $SkeletonPath -Recurse | ForEach-Object {
    $targetPath = $_.FullName.Replace($SkeletonPath, $ProjectPath)
    if ($_.PSIsContainer) {
        if (-not (Test-Path $targetPath)) {
            New-Item -ItemType Directory -Path $targetPath -Force | Out-Null
        }
    } else {
        Copy-Item -Path $_.FullName -Destination $targetPath -Force
        Write-Host "  ✓ $($_.Name)" -ForegroundColor Gray
    }
}

# Paso 4: Personalizar archivos
Write-Host "[4/5] Personalizando archivos..." -ForegroundColor Green

# Reemplazar placeholders en todos los archivos
$files = Get-ChildItem -Path $ProjectPath -Recurse -File
foreach ($file in $files) {
    $content = Get-Content -Path $file.FullName -Raw -ErrorAction SilentlyContinue
    if ($content) {
        $content = $content -replace '\$\{\{\s*values\.name\s*\}\}', $ProjectName.ToLower()
        $content = $content -replace '\$\{\{\s*parameters\.name\s*\}\}', $ProjectName.ToLower()
        $content = $content -replace '\$\{\{\s*values\.description\s*\}\}', $Description
        $content = $content -replace '\$\{\{\s*parameters\.description\s*\}\}', $Description
        $content = $content -replace '\$\{\{\s*values\.owner\s*\}\}', $Owner
        $content = $content -replace '\$\{\{\s*parameters\.owner\s*\}\}', $Owner
        $content = $content -replace '\$\{\{\s*values\.port\s*\}\}', $Port
        $content = $content -replace '\$\{\{\s*parameters\.port\s*\}\}', $Port
        $content = $content -replace '\$\{\{\s*values\.destination\.repo\s*\}\}', $ProjectName
        $content = $content -replace '\$\{\{\s*parameters\.repoUrl\s*\|\s*parseRepoUrl\s*\}\}\.repo', $ProjectName
        
        Set-Content -Path $file.FullName -Value $content -NoNewline
    }
}

Write-Host "  ✓ Placeholders reemplazados" -ForegroundColor Green

# Paso 5: Commit y push
Write-Host "[5/5] Haciendo commit y push..." -ForegroundColor Green
git add .
git commit -m "feat: initial commit from $TemplateName template"
git push origin main

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  ✓ Proyecto creado exitosamente" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Repositorio: https://github.com/$GitHubOwner/$ProjectName" -ForegroundColor Yellow
Write-Host ""
Write-Host "Próximos pasos:" -ForegroundColor Cyan
Write-Host "1. Registrar en Roadie:" -ForegroundColor White
Write-Host "   - Ve a: https://ayesa.roadie.so/catalog-import" -ForegroundColor Gray
Write-Host "   - Pega: https://github.com/$GitHubOwner/$ProjectName/blob/main/catalog-info.yaml" -ForegroundColor Gray
Write-Host "   - Click en 'Analyze' y luego 'Import'" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Verificar en catálogo:" -ForegroundColor White
Write-Host "   - https://ayesa.roadie.so/catalog" -ForegroundColor Gray
Write-Host ""
