
import os

# Create project structure
base_path = "/home/mbuchhorn/projects/EU_GraphRAG"
directories = [
    "tests",
    "data/raw",
    "data/processed",
    "notebooks",
    "scripts"
]

created_dirs = []
for dir_path in directories:
    full_path = os.path.join(base_path, dir_path)
    try:
        os.makedirs(full_path, exist_ok=True)
        created_dirs.append(full_path)
    except Exception as e:
        print(f"Error creating {full_path}: {e}")

print(f"Created {len(created_dirs)} directories:")
for d in created_dirs:
    print(f"  - {d}")
