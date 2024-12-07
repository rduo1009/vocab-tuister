#!/bin/zsh

if [[ $debug == "True" ]]; then
    echo "====== DEBUG MODE ======"
fi

# Only install necessary deps to speed up build
poetry install --only main --sync

# Install deps that need to be in universal2
if [[ "$(uname)" == "Darwin" ]]; then
    python3 -m pip install --force https://files.pythonhosted.org/packages/90/73/bcb0e36614601016552fa9344544a3a2ae1809dc1401b100eab02e772e1f/regex-2024.11.6-cp313-cp313-macosx_10_13_universal2.whl
    python3 -m pip install --force src/_build/macos/lz4-4.4.0-cp313-cp313-macosx_15_0_universal2.whl
    python3 -m pip install --force https://files.pythonhosted.org/packages/83/0e/67eb10a7ecc77a0c2bbe2b0235765b98d164d81600746914bebada795e97/MarkupSafe-3.0.2-cp313-cp313-macosx_10_13_universal2.whl
    python3 -m pip install --force src/_build/macos/numpy-2.1.3-cp313-cp313-macosx_14_0_universal2.whl
fi

# Build
if [[ $debug == "True" ]]; then
    pyinstaller vocab-tuister-server.spec --clean -- --debug
else
    pyinstaller vocab-tuister-server.spec --clean
fi

echo "Do you want to reinstall all deps? (Y/n)"
read -q response
echo
if [[ -z "$response" || "$response" == "y" || "$response" == "Y" ]]; then
    poetry install --sync
else
    poetry install --only main --sync
fi