@echo off
setlocal enabledelayedexpansion

REM Unused by default, but useful if someone wants to build on their own computer.

if "%debug%"=="True" (
    echo ====== DEBUG MODE ======
)

REM Only install necessary deps to speed up build
REM poetry install --only main --sync REM slower
poetry env remove --all
poetry install --only main

REM Build python server
poetry run dunamai from any > __version__.txt
if "%debug%"=="True" (
    poetry run pyinstaller vocab-tuister-server.spec --clean -- --debug
) else (
    poetry run pyinstaller vocab-tuister-server.spec --clean
)

REM Determine client binary name
if "%OS%"=="Windows_NT" (
    set "clientbin_name=windows"
) else (
    echo Unknown OS
    exit /b 1
)

REM Build go client
for /f "tokens=*" %%v in ('dunamai from any') do set version=%%v
go mod tidy
go generate -x src/generate.go
go build ^
    -ldflags "-X github.com/rduo1009/vocab-tuister/src/client/internal.Version=!version!" ^
    -o ".\dist\vocab-tuister-%clientbin_name%.exe" ^
    .\src\main.go

REM echo Do you want to reinstall all deps? (Y/n)
REM set /p response=
REM echo.
REM if "%response%"=="" set response=Y
REM if /i "%response%"=="y" (
REM     poetry install --sync
REM ) else (
REM     poetry install --only main --sync
REM )