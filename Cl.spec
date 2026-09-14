# calculator.spec
# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path

# Путь к иконке (относительно корня проекта)
ICON_PATH = str(Path('assets') / 'icon.ico')

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],                          # если появятся доп. файлы (звёзды, шрифты) — добавь сюда
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.font',
    ],                                 # скрытые импорты для tkinter
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name='calculator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,                          # сжатие (можно отключить: upx=False)
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,                     # False — без консольного окна (для GUI)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
                        # ← ИКОНКА ПОДСТАВЛЯЕТСЯ ЗДЕСЬ
)

# Для macOS: создаём .app-бандл
if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name='calculator.app',
        icon=ICON_PATH,
        bundle_identifier='com.example.calculator',
    )