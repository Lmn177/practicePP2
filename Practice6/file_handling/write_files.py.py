import os
import shutil

sample_data = """Alice, 25, Engineer
Bob, 30, Designer
Charlie, 22, Artist"""

with open("sample.txt", "w") as f:
    f.write(sample_data)

with open("sample.txt", "r") as f:
    print("File Content:\n", f.read())

with open("sample.txt", "a") as f:
    f.write("\nDavid, 28, Analyst")

shutil.copy("sample.txt", "sample_backup.txt")

if os.path.exists("sample_backup.txt"):
    os.remove("sample_backup.txt")