# ==============================================================================
# CRIMSON ORBIT – MUSICAL BAND
# Build Automation Helper Script (build.ps1)
# ==============================================================================

Write-Host "========================================" -ForegroundColor Red
Write-Host "   CRIMSON ORBIT :: BUILD HELPER" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Red

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$toolsDir = Join-Path $scriptDir "Tools"
$pyScript = Join-Path $toolsDir "build_floppy.py"

if (Test-Path $pyScript) {
    python $pyScript
} else {
    Write-Host "[ERROR] build_floppy.py not found in $toolsDir" -ForegroundColor Red
}
