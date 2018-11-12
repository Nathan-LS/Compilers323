# -*- mode: python -*-

block_cipher = None

from PyInstaller.utils.hooks import collect_submodules
added_hiddenimports = collect_submodules('colorama')

a = Analysis(['../src/__main__.py'],
             pathex=['./src'],
             binaries=[],
             datas=[],
             hiddenimports=added_hiddenimports,
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Compilers323',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
