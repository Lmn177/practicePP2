import os
import shutil

# Task 4 & 5: Copy and delete files safely
shutil.copy("sample.txt", "sample_backup.txt")

if os.path.exists("sample_backup.txt"):
    os.remove("sample_backup.txt")