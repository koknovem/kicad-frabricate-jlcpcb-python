import csv
import os
from datetime import datetime

def parse_adjustments(adjustment_str, adjustment_type):
    """Parse adjustment string in format 'C1:+1.5,R2:-2.0'"""
    if not adjustment_str:
        return {}
    
    adjustments = {}
    try:
        for item in adjustment_str.split(','):
            designator, value = item.split(':')
            adjustments[designator.strip()] = float(value.strip())
        return adjustments
    except ValueError as e:
        print(f"Error parsing {adjustment_type} adjustments: {e}")
        print("Format should be: 'C1:+1.5,R2:-2.0'")
        return {}

def adjust_value(row, adjustments, designator_index, value_index, is_rotation=False):
    """Adjust numerical value for a component"""
    designator = row[designator_index].strip('"')  # Remove any quotes from designator
    if designator in adjustments:
        current_value = float(row[value_index].strip('"'))  # Remove any quotes from value
        new_value = current_value + adjustments[designator]
        if is_rotation:
            new_value = new_value % 360  # Normalize rotation to 0-360
        row[value_index] = f"{new_value:.6f}"
        print(f"Adjusted {designator}: {current_value} -> {new_value}")
    return row

def replace_header_single(input_file, output_file, rotation_adjustments=None, x_adjustments=None, y_adjustments=None):
    """Replace header and adjust component positions"""
    old_header = ["Ref", "Val", "Package", "PosX", "PosY", "Rot", "Side"]
    new_header = ["Designator", "Val", "Package", "Mid X", "Mid Y", "Rotation", "Layer"]
    
    rot_adj = parse_adjustments(rotation_adjustments, "rotation")
    x_adj = parse_adjustments(x_adjustments, "X coordinate")
    y_adj = parse_adjustments(y_adjustments, "Y coordinate")

    try:
        with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            file_header = next(reader)
            if file_header != old_header:
                print(f"Header mismatch in {input_file}")
                print(f"Expected: {old_header}")
                print(f"Found: {file_header}")
                return False

            rows = []
            for row in reader:
                new_row = row.copy()  # Make a copy to preserve original values
                if rot_adj:
                    new_row = adjust_value(new_row, rot_adj, 0, 5, is_rotation=True)
                if x_adj:
                    new_row = adjust_value(new_row, x_adj, 0, 3)
                if y_adj:
                    new_row = adjust_value(new_row, y_adj, 0, 4)
                rows.append(new_row)

            with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
                writer = csv.writer(outfile)
                writer.writerow(new_header)
                writer.writerows(rows)

            print(f"Successfully processed: {output_file}")
            return True

    except Exception as e:
        print(f"Error processing {input_file}: {e}")
        print(f"Details: {str(e)}")
        return False

def replace_header_batch(input_folder, output_folder, rotation_adjustments=None, x_adjustments=None, y_adjustments=None):
    """Replace headers for all CSV files in the input folder"""
    processed = False
    
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".csv"):
            input_file = os.path.join(input_folder, file_name)
            base_name = os.path.splitext(file_name)[0]
            output_name = f"pos_{base_name}.csv"  # Removed timestamp for clarity
            output_file = os.path.join(output_folder, output_name)
            
            if replace_header_single(input_file, output_file, rotation_adjustments, x_adjustments, y_adjustments):
                print(f"Generated position file: {output_name}")
                processed = True
    
    if not processed:
        print("No CSV files were processed.")
    return processed

def replace_header(input_path, output_path, rotation_adjustments=None, x_adjustments=None, y_adjustments=None):
    """Smart header replacement - handles both single files and directories"""
    if os.path.isdir(input_path):
        replace_header_batch(input_path, "output", rotation_adjustments, x_adjustments, y_adjustments)  # Always use output directory
    else:
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        output_file = os.path.join("output", f"pos-{base_name}.csv")
        replace_header_single(input_path, output_file, rotation_adjustments, x_adjustments, y_adjustments)

if __name__ == "__main__":
    replace_header("./input", "./output", "C1:+90,R2:-180", "C1:+1.5,R2:-2.0", "C1:+1.5,R2:-2.0")
