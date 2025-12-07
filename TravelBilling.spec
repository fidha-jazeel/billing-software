# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['travel_billing_software/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        # Core files
        ('travel_billing_software/auth_data.json', 'travel_billing_software'),
        ('travel_billing_software/billing_app.ico', 'travel_billing_software'),
        ('pyproject.toml', '.'),  # Required for version checking in auto-updater
        
        # Directories (entire folders)
        ('travel_billing_software/fonts', 'travel_billing_software/fonts'),
        ('travel_billing_software/config', 'travel_billing_software/config'),
        ('travel_billing_software/auth', 'travel_billing_software/auth'),
        ('travel_billing_software/database', 'travel_billing_software/database'),
        ('travel_billing_software/ui', 'travel_billing_software/ui'),
        ('travel_billing_software/utils', 'travel_billing_software/utils'),
    ],
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'PyQt6.QtPrintSupport',
        'reportlab',
        'reportlab.lib',
        'reportlab.lib.pagesizes',
        'reportlab.lib.styles',
        'reportlab.lib.units',
        'reportlab.lib.colors',
        'reportlab.platypus',
        'reportlab.pdfgen',
        'reportlab.pdfgen.canvas',
        'pypdfium2',
        'sqlite3',
        'tomllib',  # Required for reading pyproject.toml in auto-updater
        'logging.handlers',  # Required for RotatingFileHandler
        'email.mime.text',
        'email.mime.multipart',
        'email.mime.application',
        'email.mime.base',
        'email.mime.image',
        'email.utils',
    ],
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
