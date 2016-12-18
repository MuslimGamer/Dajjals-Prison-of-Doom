# -*- mode: python -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['D:\\dropbox\\Python\\pcg-shooter'],
             binaries=None,
             # Nothing seems to work here. Just ship with datas.
             # They are correctly bundled (see: temp path on run has them),
             # they're just impossible to reference correctly. We get a crash
             # with no explanation of which file was missing.
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='main',
          debug=False,
          strip=False,
          upx=True,
          console=False )
