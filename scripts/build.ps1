#Requires -Version 5.1
$ErrorActionPreference = 'Stop'

# Set GOEXPERIMENT for encoding/json/v2
$env:GOEXPERIMENT = 'jsonv2'

if ($env:debug -eq 'True') {
    Write-Host '====== DEBUG MODE ======'
}

# INSTALL DEPS
uv sync --no-dev # slower but works better?
# uv venv --allow-existing
# uv sync --no-dev

# BUILD PYTHON SERVER
uv run dunamai from any | Set-Content -Path '__version__.txt'
if ($env:debug -eq 'True') {
    uv run pyinstaller vocab-tuister-server.spec -- --clean
} else {
    uv run pyinstaller vocab-tuister-server.spec
}

# BUILD GO CLIENT
$clientbin_name = ''
if ($IsWindows) {
    $arch = (Get-CimInstance Win32_Processor).Architecture
    switch ($arch) {
        9 { $clientbin_name = 'windows-x86_64' }  
        12 { $clientbin_name = 'windows-arm64' }  
        default { throw "Unsupported architecture: $arch" }
    }
} else {
    Write-Host 'Unknown OS'
    exit 1
}

$version = Get-Content '__version__.txt'
go mod tidy
go generate -x ./...; if (-not (git diff --quiet)) { Write-Error 'Error: Code changes after go generate.'; exit 1 }
go build `
    -ldflags "-X github.com/rduo1009/vocab-tuister/src/client/internal.Version=$version" `
    -o ".\dist\vocab-tuister-$clientbin_name.exe" `
    .\src\main.go

# CLEAN UP
# Write-Host 'Do you want to reinstall all deps? (Y/n)'
# $response = Read-Host
# Write-Host ''
# if ([string]::IsNullOrEmpty($response)) { $response = 'Y' }
# if ($response -eq 'y' -or $response -eq 'Y') {
#     uv sync
# } # else {
#     uv sync --no-dev
# }