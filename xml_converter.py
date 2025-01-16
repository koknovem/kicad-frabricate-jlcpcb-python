import os
import subprocess
from datetime import datetime

def check_and_convert_xml(folder_path, xslt_file):
    """
    Check if the folder contains an XML file and convert it to CSV using xsltproc.
    """
    processed = False
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".xml"):
            xml_file = os.path.join(folder_path, file_name)
            base_name = os.path.splitext(file_name)[0]
            output_name = f"bom_{base_name}.csv"
            output_csv = os.path.join("output", output_name)  # Always use output directory
            
            try:
                subprocess.run(["xsltproc", "-o", output_csv, xslt_file, xml_file], check=True)
                print(f"Generated BOM file: {output_name}")
                processed = True
            except subprocess.CalledProcessError as e:
                print(f"Error converting BOM file {file_name}: {e}")
                continue

    if not processed:
        print("No XML files were found for BOM generation.")
    
    return processed

if __name__ == "__main__":
    folder_path = "./input"
    xslt_file = "./bom2grouped_csv_jlpcb.xsl"
    check_and_convert_xml(folder_path, xslt_file)
