# -*- mode: python ; coding: utf-8 -*-

import lemminflect
import os

data_files = [
    ("nltk_data", "src/core/transfero/nltk_data"),
    ("src/core/transfero/adj_to_adv.json", "src/core/transfero"),
    ("src/server/templates", "src/server/templates"),
    ("src/server/static", "src/server/static"),
]

lemminflect_dir = os.path.dirname(lemminflect.__file__)
lemminflect_data_files = [
    (os.path.join(lemminflect_dir, "resources"), "lemminflect/resources"),
    (os.path.join(lemminflect_dir, "resources"), "lemminflect/resources"),
    (os.path.join(lemminflect_dir, "resources"), "lemminflect/resources"),
    (os.path.join(lemminflect_dir, "resources"), "lemminflect/resources"),
    (os.path.join(lemminflect_dir, "resources"), "lemminflect/resources"),
    (os.path.join(lemminflect_dir, "resources"), "lemminflect/resources"),
]

a = Analysis(
    ["src/__main__.py"],
    pathex=[],
    binaries=[],
    datas=data_files + lemminflect_data_files,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["typeguard"],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="vocab-tuister-server",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
