# -*- mode: python -*-
a = Analysis(['main.py'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
def extra_datas(mydir):
    def rec_glob(p, files):
        import os
        import glob
        for d in glob.glob(p):
            if os.path.isfile(d):
                files.append(d)
            rec_glob("%s/*" % d, files)
    files = []
    rec_glob("%s/*" % mydir, files)
    extra_datas = []
    for f in files:
        extra_datas.append((f, f, 'DATA'))

    return extra_datas
a.datas += extra_datas('trans')
a.datas += extra_datas('gui/img')
a.datas += extra_datas('gui/style')
a.datas += extra_datas('reports')
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='MeX-LMS.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False,
          uac_admin=True,
          icon='gui/img/logo.ico' )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas +
               [('config.json','config.json','DATA'),
                ('gdrive/drive_config.json','gdrive/drive_config.json','DATA'),
                ('client_secrets.json','client_secrets.json','DATA')],
               strip=None,
               upx=True,
               name='MeX-LMS',
               uac_admin=True,
               icon='gui/img/logo.ico')