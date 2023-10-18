import sys
from cx_Freeze import setup, Executable

# Betiği ve bağımlılıkları ekleyin
includes = []
excludes = []
packages = []

# Executable (çalıştırılabilir) tanımı
exe = Executable(
    script="app.py",  # Dönüştürmek istediğiniz Python betiği
    base=None,
)

# Setup fonksiyonunu çağırın
setup(
    name="YourAppName",
    version="1.0",
    description="Your App Description",
    options={
        "build_exe": {
            "includes": includes,
            "excludes": excludes,
            "packages": packages,
            "include_files": [],  # Gerekli dosyaları buraya ekleyebilirsiniz
        }
    },
    executables=[exe],
)
