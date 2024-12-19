import os

# Blacklist examples: Contains filenames or folder names to be ignored
BLACKLIST = ["__pycache__", ".git", "venv", ".DS_Store", "project_description", "project_describer", "README.md", "user_project"]

# Output file
OUTPUT_FILE = "project_description.md"

def is_blacklisted(path_part: str, blacklist: list) -> bool:
    """
    Checks if any part of the path (file or folder) contains a blacklist entry as a substring.
    """
    return any(blacklisted in path_part for blacklisted in blacklist)

def collect_project_structure_and_contents(start_path: str, blacklist: list) -> str:
    """
    Scans all files and folders recursively from the start path and collects
    the project structure and the contents of the files in Markdown format.
    """
    markdown_output = "# Project Description\n\n"
    markdown_output += "## Project Structure\n\n"

    structure = ""
    contents = ""

    # Recursively walk through the file system
    for root, dirs, files in os.walk(start_path):
        # Apply blacklist filter to directories
        dirs[:] = [d for d in dirs if not is_blacklisted(os.path.join(root, d), blacklist)]

        # Display folder structure
        relative_path = os.path.relpath(root, start_path)
        if is_blacklisted(relative_path, blacklist):
            continue  # Skip blacklisted directories

        structure += f"- {relative_path}/\n"

        # Scan files
        for file in files:
            if is_blacklisted(file, blacklist):
                continue

            file_path = os.path.join(root, file)
            relative_file_path = os.path.relpath(file_path, start_path)

            if is_blacklisted(relative_file_path, blacklist):
                continue

            structure += f"    - {relative_file_path}\n"

            # Read file content
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    file_content = f.read()
            except Exception as e:
                file_content = f"[Error reading file: {e}]"

            # Markdown section for each file
            contents += f"\n## {relative_file_path}\n\n"
            contents += "```\n"
            contents += file_content
            contents += "\n```"

    markdown_output += structure
    markdown_output += contents
    return markdown_output

def write_to_markdown_file(content: str, output_path: str):
    """
    Writes the given content to a Markdown file.
    """
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Markdown file successfully created: {output_path}")

def main():
    """
    Main function of the program.
    """
    start_path = os.getcwd()  # Starts in the current directory
    print(f"Starting project analysis in folder: {start_path}")
    print(f"Ignoring files and folders containing: {BLACKLIST}")

    # Generate Markdown content
    markdown_content = collect_project_structure_and_contents(start_path, BLACKLIST)

    # Write to file
    write_to_markdown_file(markdown_content, OUTPUT_FILE)

if __name__ == "__main__":
    main()