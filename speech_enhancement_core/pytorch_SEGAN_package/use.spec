# -*- mode: python ; coding: utf-8 -*-
# from PyInstaller.utils.hooks import collect_data_files
import sys
sys.setrecursionlimit(5000)

block_cipher = None


a = Analysis(['use.py'],
             pathex=["r'C:\DevelopmentTools\Miniconda3\miniconda3\envs\package_pytorch\Lib\site-packages",r"C:\Users\wp\Desktop\graduation_project\speech_enhancement_core\pytorch_SEGAN_package\u"],
             binaries=[],
             datas=[(r'C:\DevelopmentTools\Miniconda3\miniconda3\envs\package_pytorch\Lib\site-packages\librosa\util\example_data\index.json',r'librosa\util\example_data'),
                  (r'C:\DevelopmentTools\Miniconda3\miniconda3\envs\package_pytorch\Lib\site-packages\librosa\util\example_data\registry.txt',r'librosa\util\example_data')
             ],
             hiddenimports=['sklearn.utils._typedefs','sklearn', 'sklearn.tree', 'sklearn.tree._utils', 'sklearn.neighbors._quad_tree',
                           'sklearn.neighbors._typedefs', 'sklearn.utils._cython_blas',
                           'sklearn.utils.sparsetools._graph_validation','sklearn.neighbors._partition_nodes',
                           'sklearn.utils.sparsetools._graph_tools', 'sklearn.utils.lgamma'
             ],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
for d in a.datas:
  if '_C.cp38-win_amd64.pyd' in d[0]:
    a.datas.remove(d)
    break

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='use',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None,
          version="file_verison_info.txt")
