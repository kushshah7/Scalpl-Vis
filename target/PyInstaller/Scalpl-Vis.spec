# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['/Users/kushshah/Documents/Scalpl-Vis/ScBrowser/Test/src/main/python/main.py'],
             pathex=['/Users/kushshah/Documents/Scalpl-Vis/ScBrowser/Test/target/PyInstaller'],
             binaries=[],
             datas=[],
             hiddenimports=['cython', 'sklearn', 'sklearn.utils._cython_blas', 'sklearn.neighbors.typedefs', 'sklearn.neighbors.quad_tree', 'scipy._lib.messagestream', 'sklearn.tree', 'sklearn.tree._utils'],
             hookspath=['/Users/kushshah/Documents/Scalpl-Vis/ScBrowser/Test/venv/lib/python3.7/site-packages/fbs/freeze/hooks'],
             runtime_hooks=['/var/folders/1x/3yxs0z7x2xd1gqnw0qfq47b80000gn/T/tmp_g1y2pj0/fbs_pyinstaller_hook.py'],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Scalpl-Vis',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=False , icon='/Users/kushshah/Documents/Scalpl-Vis/ScBrowser/Test/target/Icon.icns')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               upx_exclude=[],
               name='Scalpl-Vis')
app = BUNDLE(coll,
             name='Scalpl-Vis.app',
             icon='/Users/kushshah/Documents/Scalpl-Vis/ScBrowser/Test/target/Icon.icns',
             bundle_identifier=None)
