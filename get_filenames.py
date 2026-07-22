import os

path = "/Users/aravindg/Downloads/Daivik Birthday"
output_file = "daivik_birthday_files.txt"

filenames = []
for root, dirs, files in os.walk(path):
    for filename in files:
        filenames.append(filename)

filenames.sort()

with open(output_file, "w") as f:
    for filename in filenames:
        f.write(filename + "\n")

print(f"Wrote {len(filenames)} filenames to {output_file}")
