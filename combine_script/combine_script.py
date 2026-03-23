import os

VALID_EXTENSIONS = {
    ".py", ".java", ".jsx", ".js", ".html", ".css", ".dart", ".ts", ".tsx", ".properties"
}

IGNORE_DIRS = {"node_modules", ".git", "build", "dist", "__pycache__"}

def should_ignore(file_name, ignore_list):
    return file_name in ignore_list

def collect_files(root_dir, ignore_list):
    collected_files = []

    for foldername, subfolders, filenames in os.walk(root_dir):

        subfolders[:] = [d for d in subfolders if d not in IGNORE_DIRS]

        for filename in filenames:
            if should_ignore(filename, ignore_list):
                continue

            _, ext = os.path.splitext(filename)

            MAX_FILE_SIZE = 200 * 1024  #200 KB
            if ext.lower() in VALID_EXTENSIONS:
                full_path = os.path.join(foldername, filename)

                if os.path.getsize(full_path) > MAX_FILE_SIZE:
                    continue

                collected_files.append(full_path)
    collected_files.sort()
    return collected_files

def read_and_write(files, output_file):
    with open(output_file, "w", encoding="utf-8") as outfile:
        for file_path in files:
            try:
                with open(file_path, "r", encoding="utf-8") as infile:
                    content = infile.read()

                outfile.write(f"--- FILE: {file_path} ---\n\n")
                outfile.write(content)
                outfile.write("\n\n\n")

            except Exception as e:
                print(f"Skipped {file_path}: {e}")

def main():
    root_dir = input("Enter root directory: ").strip().strip('"').strip("'")
    ignore_input = input("Enter file names to ignore (comma-separated): ").strip()

    ignore_list = [name.strip() for name in ignore_input.split(",") if name.strip()]

    OUTPUT_DIR = r"C:\Users\Administrator\OneDrive\Desktop\New folder\combine_script\combined_output"
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, "combined_output.txt")
    # output_file = "combined_output.txt"  #make this line comment and un-comment previous 3 lines and give output saving directory if in case you want to store output to a specific directory

    files = collect_files(root_dir, ignore_list)

    print(f"Found {len(files)} files. Processing...")

    read_and_write(files, output_file)

    print(f"Done. Output saved to {output_file}")

if __name__ == "__main__":
    main()
