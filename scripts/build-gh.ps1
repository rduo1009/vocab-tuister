#Requires -Version 5.1
$ErrorActionPreference = 'Stop'

# Set GOEXPERIMENT for encoding/json/v2
$env:GOEXPERIMENT = 'jsonv2'

mkdir dist -Force

# Check generated files are up to date
# HACK: poe is not working properly; but problems will be caught by other runs
# poe generate
# & 'C:\Program Files\Git\bin\git.exe' diff --quiet
# if ($LASTEXITCODE -ne 0) {
#     Write-Error 'Error: Code changes after poe generate.'
#     exit 1
# }

# Determine binary name
$binary_name = ''
$arch = (Get-CimInstance Win32_Processor).Architecture
switch ($arch) {
    9 { $binary_name = 'windows-x86_64' }  
    12 { $binary_name = 'windows-arm64' }  
    default { throw "Unsupported architecture: $arch" }
}

# Build python server
uv venv --allow-existing
uv sync --no-group=types --no-dev 
$version = uv run dunamai from any --style=semver
$version | Set-Content -NoNewline -Path '__version__.txt'
uv run nuitka src --output-filename="./dist/vocab-tuister-server-$binary_name.exe" --assume-yes-for-downloads --deployment

# Build go client
$version = Get-Content '__version__.txt'
go build `
    -ldflags "-X github.com/rduo1009/vocab-tuister/src/client/internal.Version=$version" `
    -o ".\dist\vocab-tuister-$binary_name.exe" `
    .\src\main.go
