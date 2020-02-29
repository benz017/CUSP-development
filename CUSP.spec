# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['CUSP\\manage.py'],
             pathex=['C:\\Users\\benZ\\PycharmProjects\\CUSP'],
             binaries=[],
             datas=[('C:\\Users\\benZ\\PycharmProjects\\CUSP\\CUSP\\templates','templates'),('C:\\Users\\benZ\\PycharmProjects\\CUSP\\CUSP\\static','static'),('C:\\Users\\benZ\\PycharmProjects\\CUSP\\CUSP\\home\\static','home\\static'),('C:\\Users\\benZ\\PycharmProjects\\CUSP\\CUSP\\contact\\static','contact\\static'),('C:\\Users\\benZ\\PycharmProjects\\CUSP\\CUSP\\media','media')],
             hiddenimports=['home','home.urls','contact','contact.urls','django.contrib.admin','django.contrib.auth','django.contrib.contenttypes','django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles',],
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
          [],
          exclude_binaries=True,
          name='CUSP',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='CUSP')
