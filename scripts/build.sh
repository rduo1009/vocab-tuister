#!/bin/bash

if [[ $debug == "True" ]]; then
    echo "====== DEBUG MODE ======"
fi

# Only install necessary deps to speed up build
# poetry install --only main --sync # slower
poetry env remove --all
poetry install --only main

# Install deps that need to be in universal2
if [[ "$target_arch" == "universal2" ]]; then
    if [[ "$(uname)" == "Darwin" ]]; then
        python3 -m pip install --force https://files.pythonhosted.org/packages/90/73/bcb0e36614601016552fa9344544a3a2ae1809dc1401b100eab02e772e1f/regex-2024.11.6-cp313-cp313-macosx_10_13_universal2.whl
        python3 -m pip install --force https://files.pythonhosted.org/packages/83/0e/67eb10a7ecc77a0c2bbe2b0235765b98d164d81600746914bebada795e97/MarkupSafe-3.0.2-cp313-cp313-macosx_10_13_universal2.whl
        python3 -m pip install --force src/_build/macos/wheels/*.whl
    fi
fi

# Build
dunamai from any > __version__.txt
if [[ -z "$target_arch" ]]; then
    if [[ $debug == "True" ]]; then
        pyinstaller vocab-tuister-server.spec --clean -- --debug
    else
        pyinstaller vocab-tuister-server.spec --clean
    fi
else
    if [[ $debug == "True" ]]; then
        pyinstaller vocab-tuister-server.spec --clean -- --debug --target-arch $target_arch
    else
        pyinstaller vocab-tuister-server.spec --clean -- --target-arch $target_arch
    fi
fi

echo -n "Do you want to reinstall all deps? (Y/n) "
read -r response
echo
if [[ -z "$response" || "$response" == "y" || "$response" == "Y" ]]; then
    poetry install --sync
else
    poetry install --only main --sync
fi