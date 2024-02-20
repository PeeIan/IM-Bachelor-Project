# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_submodules

a = Analysis(
    ['LoginPage.py','attendance.py','face_recognition.py','import_csv.py','lesson.py','main_upd.py','mahoa.py','report_attendance.py','search_image.py','student_upd.py','teacher.py'],
    pathex=['D:\Project(English)\DiemDanhHSAPP'],
    binaries=[],
    datas=[],
    hiddenimports=["babel.numbers"],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Check in',
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon = 'gaming.ico',
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='LoginPage',
)
