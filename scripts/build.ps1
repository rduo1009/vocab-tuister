#Requires -Version 5.1
$ErrorActionPreference = 'Stop'

# Set GOEXPERIMENT for encoding/json/v2
$env:GOEXPERIMENT = 'jsonv2'

# CI is set to "true" automatically by GitHub Actions
$isCI = $env:CI -eq 'true'

mkdir dist -Force

# NOTE: poe is not working properly in CI; but problems will be caught by other runs
if (-not $isCI) {
    # Check generated files are up to date
    poe generate
    & 'C:\Program Files\Git\bin\git.exe' diff --quiet
    if ($LASTEXITCODE -ne 0) {
        Write-Error 'Error: Code changes after poe generate.'
        exit 1
    }
}

# Determine binary name
$arch = (Get-CimInstance Win32_Processor).Architecture
$binary_name = switch ($arch) {
    9 { 'windows-x86_64' }
    12 { 'windows-arm64' }
    default { throw "Unsupported architecture: $arch" }
}

# Build python server
uv venv --allow-existing
uv sync --no-group=types --no-dev
$version = uv run dunamai from any --style=semver
$version | Set-Content -NoNewline -Path '__version__.txt'

$nuitkaArgs = @('src', "--output-filename=./dist/vocab-tuister-server-$binary_name.exe")
if ($isCI) { $nuitkaArgs += '--assume-yes-for-downloads', '--deployment', '--mingw64' }
uv run nuitka @nuitkaArgs

# Build go client
go build `
    -ldflags "-X github.com/rduo1009/vocab-tuister/src/client/internal.Version=$version" `
    -o ".\dist\vocab-tuister-$binary_name.exe" `
    .\src\main.go