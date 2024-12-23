import os
import shutil

def read_file_stack(file, chars):
    with open(file, encoding="utf-8") as f:
        data = f.read()
    stack = []
    string = ""
    for char in data:
        if char in chars:
            if string.find("/"):
                stack.append(string)
            string = ""
            continue
        string = string + char
    stack2 = [s for s in stack if s and not s.startswith('\n')]
    return stack2


def print_list_between_strings(my_list, left_string, right_string):
    printing = False
    for item in my_list:
        if item == left_string:
            printing = True
        elif item == right_string:
            printing = False
        if printing and item not in [left_string, right_string]:
            print(item)


def remove_content_after_group_and_add_end(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding="utf-8") as file:
                lines = file.readlines()

            with open(file_path, 'w', encoding="utf-8") as file:
                for line in lines:
                    file.write(line)
                    if line.strip() == "</group>":
                        break
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding="utf-8") as file:
                lines = file.readlines()

            if len(lines) >= 2:
                second_row = lines[1].strip()
                modified_second_row = second_row[:1] + '/' + second_row[1:]

                with open(file_path, 'a', encoding="utf-8") as file:
                    file.write('\n' + modified_second_row)

def move_files_from_subfolders(main_folder):
    # Get a list of all subfolders in the main folder
    subfolders = [f.path for f in os.scandir(main_folder) if f.is_dir()]

    # Move files from each subfolder to the main folder
    for subfolder in subfolders:
        for filename in os.listdir(subfolder):
            file_path = os.path.join(subfolder, filename)
            new_path = os.path.join(main_folder, filename)

            # Handle file name collisions
            counter = 1
            while os.path.exists(new_path):
                base, extension = os.path.splitext(filename)
                new_path = os.path.join(main_folder, f"{base}_{counter}{extension}")
                counter += 1

            shutil.move(file_path, new_path)

    # Remove empty subfolders
    for subfolder in subfolders:
        os.rmdir(subfolder)


def merge_files(input_folder, output_file):
    with open(output_file, 'w', encoding='utf-8') as output_file:
        for filename in os.listdir(input_folder):
            file_path = os.path.join(input_folder, filename)
            if os.path.isfile(file_path):
                with open(file_path, 'r', encoding='utf-8') as input_file:
                    # Skip the first line of each file
                    lines = input_file.readlines()[1:]
                    output_file.write(''.join(lines))
                    output_file.write('\n')  # Add a line between files


def remove_text_between_lines(file_path, start_line, end_line):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    inside_section = False
    new_lines = []

    for line in lines:
        if start_line in line:
            inside_section = True
        elif end_line in line and inside_section:
            inside_section = False
        elif not inside_section:
            new_lines.append(line)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(new_lines)

import xml.etree.ElementTree as ET

def main():
    # Load the XML file
    tree = ET.parse("Games.xml")
    root = tree.getroot()

    # Find events with at least one restot less than 0
    events_to_remove = []

    for event in root.iter():
        if event.tag.startswith("event-"):
            has_negative_restot = False
            
            # Check all pairs within the event
            for pair in event.findall('.//pair'):
                restot_element = pair.find('restot')
                if restot_element is not None and restot_element.text:
                    try:
                        restot_value = float(restot_element.text)
                        if restot_value < 0:
                            has_negative_restot = True
                            break
                    except ValueError:
                        print(f"Warning: Could not convert restot value '{restot_element.text}' to float.")

            if has_negative_restot:
                events_to_remove.append(event)

    # Remove the events with negative restot
    for event in events_to_remove:
        print("hi")
        root.remove(event)

    # Save the modified XML back to a file
    tree.write("Modified_Games.xml")

    # Print a message indicating the operation is complete
    print("Finished processing. Modified file saved as 'Modified_Games.xml'.")

if __name__ == "__main__":
    main()
