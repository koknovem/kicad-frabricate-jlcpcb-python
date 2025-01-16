import csv
import os
import subprocess
import argparse
from xml_converter import check_and_convert_xml
from csv_header_replacer import replace_header_single, replace_header_batch  # Updated imports

# Remove the duplicate check_and_convert_xml function
# Remove the duplicate replace_header function

def ensure_directories():
    """Create input and output directories if they don't exist"""
    os.makedirs("input", exist_ok=True)
    os.makedirs("output", exist_ok=True)

def main():
    ensure_directories()
    
    parser = argparse.ArgumentParser(description='KiCad Fabrication File Generator')
    parser.add_argument('--convert-xml', action='store_true', help='Convert XML to CSV')
    parser.add_argument('--replace-header', action='store_true', help='Replace CSV headers')
    parser.add_argument('--folder', default='input', help='Folder path for XML conversion')
    parser.add_argument('--xslt', default='bom2grouped_csv_jlcpcb.xsl', help='XSLT file path')
    parser.add_argument('--input', default='input', help='Input CSV file or folder')
    parser.add_argument('--output', default='output', help='Output directory')
    parser.add_argument('--adjust-rotation', help='Adjust rotation for specific components (format: "C1:+90,R2:-180")')
    parser.add_argument('--adjust-x', help='Adjust X coordinates (format: "C1:+1.5,R2:-2.0")')
    parser.add_argument('--adjust-y', help='Adjust Y coordinates (format: "C1:+1.5,R2:-2.0")')

    args = parser.parse_args()

    # Check for XSLT file
    if not os.path.isfile('bom2grouped_csv_jlcpcb.xsl'):
        print("Error: Required XSLT file 'bom2grouped_csv_jlcpcb.xsl' not found in current directory")
        print(f"Current working directory: {os.getcwd()}")
        return

    print("Starting file processing...")
    
    # If no specific operation is requested, do both
    if not (args.convert_xml or args.replace_header):
        print("Processing all files...")
        xml_result = check_and_convert_xml(args.folder, args.xslt)
        csv_result = replace_header_batch(args.input, args.output, 
                                          args.adjust_rotation,
                                          args.adjust_x,
                                          args.adjust_y)
        
        if not (xml_result or csv_result):
            print("No files were processed.")
        return

    if args.convert_xml:
        check_and_convert_xml(args.folder, args.xslt)
    
    if args.replace_header:
        if os.path.isfile(args.input):
            base_name = os.path.splitext(os.path.basename(args.input))[0]
            output_file = os.path.join(args.output, f"pos_{base_name}.csv")
            replace_header_single(args.input, output_file, 
                                  args.adjust_rotation,
                                  args.adjust_x,
                                  args.adjust_y)
        else:
            replace_header_batch(args.input, args.output,
                                 args.adjust_rotation,
                                 args.adjust_x,
                                 args.adjust_y)

if __name__ == "__main__":
    main()
