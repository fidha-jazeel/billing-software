# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['travel_billing_software/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('travel_billing_software/auth_data.json', 'travel_billing_software'),
        ('travel_billing_software/fonts', 'travel_billing_software/fonts'),
        ('travel_billing_software/config', 'travel_billing_software/config'),
        ('travel_billing_software/ui', 'travel_billing_software/ui'),
        ('travel_billing_software/utils', 'travel_billing_software/utils'),
        ('travel_billing_software/database', 'travel_billing_software/database'),
        ('travel_billing_software/.env', 'travel_billing_software'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='TravelBilling',
    icon='travel_billing_software/billing_app.ico',
    console=False,
)
