# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['link_card_generator_v4.0.py'],
    pathex=[],
    binaries=[],
    datas=[('ah9v5-zy2rl.png', '.')],
    hiddenimports=['pywinstyles'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['copy'],
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
    name='链接卡片生成器',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
