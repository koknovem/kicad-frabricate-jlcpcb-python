import csv
import os
from datetime import datetime

def replace_header_single(input_file, output_file):
    """Replace header for a single CSV file"""
    old_header = ["Ref", "Val", "Package", "PosX", "PosY", "Rot", "Side"]
    new_header = ["Designator", "Val", "Package", "Mid X", "Mid Y", "Rotation", "Layer"]

    try:
        with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            file_header = next(reader)
            if file_header != old_header:
                print(f"Header mismatch in {input_file}")
                print(f"Expected: {old_header}")
                print(f"Found: {file_header}")
                return False

            with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
                writer = csv.writer(outfile)
                writer.writerow(new_header)
                for row in reader:
                    writer.writerow(row)

            print(f"Successfully processed: {output_file}")
            return True

    except Exception as e:
        print(f"Error processing {input_file}: {e}")
        return False

def replace_header_batch(input_folder, output_folder):
    """Replace headers for all CSV files in the input folder"""
    processed = False
    
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".csv"):
            input_file = os.path.join(input_folder, file_name)
            base_name = os.path.splitext(file_name)[0]
            output_name = f"pos_{base_name}.csv"  # Removed timestamp for clarity
            output_file = os.path.join(output_folder, output_name)
            
            if replace_header_single(input_file, output_file):
                print(f"Generated position file: {output_name}")
                processed = True
    
    if not processed:
        print("No CSV files were processed.")
    return processed

def replace_header(input_path, output_path):
    """Smart header replacement - handles both single files and directories"""
    if os.path.isdir(input_path):
        replace_header_batch(input_path, "output")  # Always use output directory
    else:
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        output_file = os.path.join("output", f"pos-{base_name}.csv")
        replace_header_single(input_path, output_file)

if __name__ == "__main__":
    replace_header("./input", "./output")
