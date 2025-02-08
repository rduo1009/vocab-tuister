# -*- mode: python ; coding: utf-8 -*-

import argparse
import os
import platform
import sys

import lemminflect

parser = argparse.ArgumentParser()
parser.add_argument("--debug", action="store_true")
parser.add_argument("--target-arch", action="store", type=str)
options = parser.parse_args()

if options.target_arch and sys.platform != "darwin":
    raise ValueError("--target-arch is not supported on non-macOS platforms.")

target_arch = None

if sys.platform == "darwin":
    target_arch = options.target_arch
    if target_arch not in {"x86_64", "arm64", "universal2"}:
        raise ValueError(
            f"--target-arch value is not valid (got '{target_arch}')."
        )

    if target_arch == "universal2":
        # fmt: off
        replaced_stdlib_extensions = ("_asyncio", "_bisect", "_blake2", "_bz2", "_codecs_cn", "_codecs_hk", "_codecs_iso2022", "_codecs_jp", "_codecs_kr", "_codecs_tw", "_contextvars", "_csv", "_ctypes", "_curses", "_datetime", "_dbm", "_decimal", "_elementtree", "_hashlib", "_heapq", "_json", "_lzma", "_md5", "_multibytecodec", "_multiprocessing", "_opcode", "_pickle", "_posixshmem", "_posixsubprocess", "_queue", "_random", "_scproxy", "_sha1", "_sha2", "_sha3", "_socket", "_sqlite3", "_ssl", "_statistics", "_struct", "_uuid", "array", "binascii", "fcntl", "grp", "math", "mmap", "pyexpat", "readline", "resource", "select", "syslog", "termios", "unicodedata", "zlib")
        replaced_dylibs = ("libpython3.13", "libintl.8", "liblzma.5", "libmpdec.4", "libcrypto.3", "libb2.1", "libssl.3", "libncursesw.6", "libreadline.8", "liblz4.1", "libsqlite3.0")
        # fmt: on

        def replace_binaries(dep_list):
            def _replace_binary(location, file_path):
                for i, (name, _, binary_type) in enumerate(dep_list):
                    if name == location:
                        dep_list[i] = (name, file_path, binary_type)
                        # print("used:", location)
                        break
                # else:
                #     print("not used:", location)

            def _add_binary(location, file_path):
                dep_list.append((location, file_path, "BINARY"))

            for extension in replaced_stdlib_extensions:
                _replace_binary(
                    f"lib-dynload/{extension}.cpython-313-darwin.so",
                    f"src/_build/macos/stdlib/{extension}.cpython-313-darwin.so",
                )

            for dylib in replaced_dylibs:
                _replace_binary(
                    f"{dylib}.dylib", f"src/_build/macos/dylib/{dylib}.dylib"
                )

    name = f"vocab-tuister-server-darwin-{target_arch}"

elif sys.platform == "linux":
    name = f"vocab-tuister-server-linux-{platform.machine()}"
else:
    raise ValueError(f"Unsupported platform {sys.platform}")

data_files = [
    ("nltk_data", "src/core/transfero/nltk_data"),
    ("src/core/transfero/adj_to_adv.json", "src/core/transfero"),
    ("src/server/templates", "src/server/templates"),
    ("src/server/static", "src/server/static"),
    ("__version__.txt", "."),
]

lemminflect_dir = os.path.dirname(lemminflect.__file__)
lemminflect_data_files = [
    (os.path.join(lemminflect_dir, "resources"), "lemminflect/resources")
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

if sys.platform == "darwin" and target_arch == "universal2":
    replace_binaries(a.binaries)
    replace_binaries(pyz.dependencies)

# for binary in a.binaries:
#     print(binary)

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
