# KiCad Fabrication Generator

A Python utility for processing KiCad fabrication files. This tool can:
- Convert XML BOM files to CSV using XSLT
- Replace CSV headers to match JLCPCB format

## Requirements

- Python 3.6+
- xsltproc (for XML conversion)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/kicad-fabrication-generator.git
cd kicad-fabrication-generator
```

2. Ensure xsltproc is installed:
```bash
# On Debian/Ubuntu
sudo apt-get install xsltproc

# On macOS
brew install libxslt
```

## Project Structure

```
./
├── bom2grouped_csv_jlpcb.xsl    # XSLT template in root directory
├── input/                       # Place input files here
├── output/                      # Generated files appear here
├── main.py
├── xml_converter.py
└── csv_header_replacer.py
```

## Setup
1. Place the XSLT file (bom2grouped_csv_jlpcb.xsl) in the current directory (same level as main.py)
2. Place your XML and CSV files in the ./input directory
3. Generated files will appear in the ./output directory

## Usage

First, place your input files in the `input` folder. The script will automatically create input and output folders if they don't exist.

### Quick Start
Simply run without arguments to process all files:
```bash
python main.py
```
This will:
1. Convert all XML files to CSV
2. Process all CSV files to replace headers

### Specific Operations

1. Convert XML to CSV only:
```bash
python main.py --convert-xml
```

2. Replace CSV Headers only:
```bash
python main.py --replace-header
```

### 3. Batch Processing
By default, the script will process all compatible files in the input directory:
- All XML files will be converted to CSV
- All CSV files will have their headers replaced

## Arguments

- `--convert-xml`: Enable XML to CSV conversion
- `--replace-header`: Enable CSV header replacement
- `--folder`: Folder path containing XML files (default: "./")
- `--xslt`: Path to XSLT template (default: "bom2grouped_csv_jlpcb.xsl")
- `--input`: Input CSV file path (default: "input.csv")
- `--output`: Output CSV file path (default: "output.csv")

## File Format

### Expected CSV Header Format

Original header:
```
Ref,Val,Package,PosX,PosY,Rot,Side
```

Converted header:
```
Designator,Val,Package,Mid X,Mid Y,Rotation,Layer
```

## License

MIT License