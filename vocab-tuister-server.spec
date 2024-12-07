# -*- mode: python ; coding: utf-8 -*-

import argparse
import os
import sys

import lemminflect

parser = argparse.ArgumentParser()
parser.add_argument("--debug", action="store_true")
options = parser.parse_args()

target_arch = None
if sys.platform == "darwin":
    target_arch = "universal2"

    # fmt: off
    replaced_stdlib_extensions = ["_asyncio", "_bisect", "_blake2", "_bz2", "_codecs_cn", "_codecs_hk", "_codecs_iso2022", "_codecs_jp", "_codecs_kr", "_codecs_tw", "_contextvars", "_csv", "_ctypes", "_ctypes_test", "_curses", "_curses_panel", "_datetime", "_dbm", "_decimal", "_elementtree", "_hashlib", "_heapq", "_interpchannels", "_interpqueues", "_interpreters", "_json", "_lsprof", "_lzma", "_md5", "_multibytecodec", "_multiprocessing", "_opcode", "_pickle", "_posixshmem", "_posixsubprocess", "_queue", "_random", "_scproxy", "_sha1", "_sha2", "_sha3", "_socket", "_sqlite3", "_ssl", "_statistics", "_struct", "_testbuffer", "_testcapi", "_testclinic", "_testclinic_limited", "_testexternalinspection", "_testimportmultiple", "_testinternalcapi", "_testlimitedcapi", "_testmultiphase", "_testsinglephase", "_uuid", "_xxtestfuzz", "_zoneinfo", "array", "binascii", "cmath", "fcntl", "grp", "math", "mmap", "pyexpat", "readline", "resource", "select", "syslog", "termios", "unicodedata", "xxlimited", "xxlimited_35", "xxsubtype", "zlib"]
    # fmt: on

    def replace_extension(dep_list):
        def _replace_extension(location, file_path):
            for i, (name, path, binary_type) in enumerate(dep_list):
                if name == location:
                    dep_list[i] = (name, file_path, binary_type)
                    break

        for extension in replaced_stdlib_extensions:
            _replace_extension(
                f"lib-dynload/{extension}.cpython-313-darwin.so",
                f"src/_build/macos/stdlib/{extension}.cpython-313-darwin.so",
            )


name = f"vocab-tuister-server-{sys.platform}"


data_files = [
    ("nltk_data", "src/core/transfero/nltk_data"),
    ("src/core/transfero/adj_to_adv.json", "src/core/transfero"),
    ("src/server/templates", "src/server/templates"),
    ("src/server/static", "src/server/static"),
]

lemminflect_dir = os.path.dirname(lemminflect.__file__)
lemminflect_data_files = [
    (os.path.join(lemminflect_dir, "resources"), "lemminflect/resources"),
]

a = Analysis(
    ["src/__main__.py"],
    pathex=[],
    binaries=[],
    datas=data_files + lemminflect_data_files,
    hiddenimports=["numpy.core.multiarray"],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["typeguard", "tkinter"],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

if sys.platform == "darwin":
    replace_extension(a.binaries)
    replace_extension(pyz.dependencies)


if not options.debug:
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.datas,
        [],
        name=name,
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        upx_exclude=[],
        runtime_tmpdir=None,
        console=True,
        disable_windowed_traceback=False,
        argv_emulation=False,
        target_arch=target_arch,
        codesign_identity=None,
        entitlements_file=None,
    )

else:
    exe = EXE(
        pyz,
        a.scripts,
        [],
        exclude_binaries=True,
        name=name,
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        console=True,
        disable_windowed_traceback=False,
        argv_emulation=False,
        target_arch=target_arch,
        codesign_identity=None,
        entitlements_file=None,
    )
    coll = COLLECT(
        exe,
        a.binaries,
        a.datas,
        strip=False,
        upx=True,
        upx_exclude=[],
        name=name,
    )
