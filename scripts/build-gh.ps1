#Requires -Version 5.1
# Stop on first error
$ErrorActionPreference = "Stop"

# HACK: Using full paths to avoid issues (likely not needed on someone's own machine)

if ($env:debug -eq "True") {
    Write-Host "====== DEBUG MODE ======"
}

# Only install necessary deps to speed up build
poetry sync --only main # slower but works better?
# poetry env remove --all
# poetry install --only main

# Build python server
poetry run dunamai from any | Set-Content -Path "__version__.txt"
if ($env:debug -eq "True") {
    poetry run pyinstaller vocab-tuister-server.spec -- --clean
}
else {
    poetry run pyinstaller vocab-tuister-server.spec
}

# Determine client binary name
$clientbin_name = ""
if ($IsWindows) {
    $arch = (Get-CimInstance Win32_Processor).Architecture
    switch ($arch) {
        9 { $clientbin_name = "windows-x86_64" }  
        12 { $clientbin_name = "windows-arm64" }  
        default { throw "Unsupported architecture: $arch" }
    }
}
else {
    Write-Host "Unknown OS"
    exit 1
}

# Build go client
$version = Get-Content "__version__.txt"
go mod tidy
# HACK: go generate is not working properly; but problems will be caught by other runs
# go generate -x ./...; if (-not (& "C:\Program Files\Git\bin\git.exe" diff --quiet)) { Write-Error "Error: Code changes after go generate."; exit 1 }
go build `
    -ldflags "-X github.com/rduo1009/vocab-tuister/src/client/internal.Version=$version" `
    -o ".\dist\vocab-tuister-$clientbin_name.exe" `
    .\src\main.go

# Write-Host "Do you want to reinstall all deps? (Y/n)"
# $response = Read-Host
# Write-Host ""
# if ([string]::IsNullOrEmpty($response)) { $response = "Y" }
# if ($response -eq "y" -or $response -eq "Y") {
#     poetry install --sync
# }
# else {
#     poetry install --only main --sync
# }