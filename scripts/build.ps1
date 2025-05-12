#Requires -Version 5.1
# Stop on first error
$ErrorActionPreference = "Stop"

if ($env:debug -eq "True") {
    Write-Host "====== DEBUG MODE ======"
}

# Only install necessary deps to speed up build
# poetry install --only main --sync # slower
poetry.exe env remove --all
poetry.exe install --only main

# Build python server
poetry.exe run dunamai from any | Set-Content -Path "__version__.txt"
if ($env:debug -eq "True") {
    poetry.exe run pyinstaller vocab-tuister-server.spec -- --clean
}
else {
    poetry.exe run pyinstaller vocab-tuister-server.spec
}

# Determine client binary name
$clientbin_name = ""
if ($IsWindows) {
    $clientbin_name = "windows"
}
else {
    Write-Host "Unknown OS"
    exit 1
}

# Build go client
$version = (poetry.exe run dunamai from any)
go mod tidy
go generate -x src/generate.go
go build `
    -ldflags "-X github.com/rduo1009/vocab-tuister/src/client/internal.Version=$version" `
    -o ".\dist\vocab-tuister-$clientbin_name.exe" `
    .\src\main.go

# Write-Host "Do you want to reinstall all deps? (Y/n)"
# $response = Read-Host
# Write-Host ""
# if ([string]::IsNullOrEmpty($response)) { $response = "Y" }
# if ($response -eq "y" -or $response -eq "Y") {
#     poetry.exe install --sync
# }
# else {
#     poetry.exe install --only main --sync
# }