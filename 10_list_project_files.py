
import os

# List all files in the project directory
project_root = "/home/mbuchhorn/projects/EU_GraphRAG"

def list_files_recursive(directory, prefix=""):
    """Recursively list all files in directory"""
    items = []
    try:
        entries = sorted(os.listdir(directory))
        for entry in entries:
            if entry.startswith('.'):
                continue
            path = os.path.join(directory, entry)
            if os.path.isdir(path):
                items.append(f"{prefix}📁 {entry}/")
                items.extend(list_files_recursive(path, prefix + "  "))
            else:
                size = os.path.getsize(path)
                size_kb = size / 1024
                items.append(f"{prefix}📄 {entry} ({size_kb:.1f} KB)")
    except Exception as e:
        items.append(f"{prefix}❌ Error: {e}")
    return items

print("="*70)
print("EU-GraphRAG Project Files")
print("="*70)
print()

files = list_files_recursive(project_root)
for f in files:
    print(f)

print()
print("="*70)
print(f"Total files: {len([f for f in files if '📄' in f])}")
print(f"Total directories: {len([f for f in files if '📁' in f])}")
print("="*70)
