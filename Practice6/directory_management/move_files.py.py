import os
import shutil

# Task 4: Move/copy files between directories
if os.path.exists("sample.txt"):
    shutil.move("sample.txt", "nested_folder/sample.txt")