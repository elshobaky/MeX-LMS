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
a.datas += extra_datas('img')
a.datas += extra_datas('gui/img')
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='MeX-LMS.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas +
               [('README.md', 'README.md', 'DATA'),('LICENSE', 'LICENSE', 'DATA'), ('options.json','options.json','DATA')],
               strip=None,
               upx=True,
               name='MeX-LMS',
               icon='img/logo.png')
