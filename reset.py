import shutil
import os

base_path = r"C:\Users\smfse\OneDrive\Masaüstü\project_folder"
os.chdir(base_path)

if os.path.exists("dataset"):
    shutil.rmtree("dataset")
if os.path.exists("trainer.yml"):
    os.remove("trainer.yml")
if os.path.exists("labels.txt"):
    os.remove("labels.txt")

os.makedirs("dataset", exist_ok=True)
print("Sistem tamamen sıfırlandı.")
