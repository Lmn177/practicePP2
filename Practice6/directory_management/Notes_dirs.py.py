import os
import glob

# Task 1, 2, 3: Nested dirs, Listing, and Finding by extension
os.makedirs("nested_folder/sub_folder", exist_ok=True)

print("Current Directory Items:", os.listdir("."))

txt_files = glob.glob("*.txt")
print("Found these .txt files:", txt_files)