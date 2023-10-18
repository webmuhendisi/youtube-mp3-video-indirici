from setuptools import setup

APP = ['app.py']  # Uygulamanızın ana dosyasının adını buraya yazın
DATA_FILES = []  # Gerekli veri dosyalarınızı burada belirtin (örneğin, ikon dosyaları, vs.)
OPTIONS = {
    'argv_emulation': True,
    'packages': ['pytube', 'tkinter', 'ttk'],  # Kullandığınız kütüphaneleri buraya ekleyin
    'iconfile': 'icon.icns',  # Uygulama simgesi (varsa) buraya ekleyin
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
