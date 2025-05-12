#Requires -Version 5.1
# Stop on first error
$ErrorActionPreference = "Stop"

# HACK: For some reason poetry installed on a github actions runner (using pipx) doesn't work.
# Using full path in this script to fix this.

if ($env:debug -eq "True") {
    Write-Host "====== DEBUG MODE ======"
}

# Only install necessary deps to speed up build
& "C:\Program Files (x86)\pipx_bin\poetry.exe" sync --only main # slower but works better?
# & "C:\Program Files (x86)\pipx_bin\poetry.exe" env remove --all
# & "C:\Program Files (x86)\pipx_bin\poetry.exe" install --only main

# Build python server
& "C:\Program Files (x86)\pipx_bin\poetry.exe" run dunamai from any | Set-Content -Path "__version__.txt"
if ($env:debug -eq "True") {
    & "C:\Program Files (x86)\pipx_bin\poetry.exe" run pyinstaller vocab-tuister-server.spec -- --clean
}
else {
    & "C:\Program Files (x86)\pipx_bin\poetry.exe" run pyinstaller vocab-tuister-server.spec
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
$version = (& "C:\Program Files (x86)\pipx_bin\poetry.exe" run dunamai from any)
go mod tidy
go generate -x ./...; if (-not (git diff --quiet)) { Write-Error "Error: Code changes after go generate."; exit 1 }
go build `
    -ldflags "-X github.com/rduo1009/vocab-tuister/src/client/internal.Version=$version" `
    -o ".\dist\vocab-tuister-$clientbin_name.exe" `
    .\src\main.go

# Write-Host "Do you want to reinstall all deps? (Y/n)"
# $response = Read-Host
# Write-Host ""
# if ([string]::IsNullOrEmpty($response)) { $response = "Y" }
# if ($response -eq "y" -or $response -eq "Y") {
#     & "C:\Program Files (x86)\pipx_bin\poetry.exe" install --sync
# }
# else {
#     & "C:\Program Files (x86)\pipx_bin\poetry.exe" install --only main --sync
# }