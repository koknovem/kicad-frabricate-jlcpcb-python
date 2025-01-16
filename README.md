# KiCad JLCPCB Position File Generator

A Python utility for processing KiCad position files to match JLCPCB format requirements. This tool:
- Converts KiCad position CSV files to JLCPCB format
- Supports batch processing of multiple files
- Allows position and rotation adjustments for components

## Requirements

- Python 3.6+
- xsltproc (for BOM conversion)

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/koknovem/kicad-frabricate-jlcpcb-python.git
cd kicad-frabricate-jlcpcb-python
```

2. Place files:
   - Position files (.csv) → `input/` directory
   - KiCad Netlist files (.xml) → `input/` directory (Export from KiCad PCB Editor: File > Fabrication Outputs > Component Placement (.pos))
   - XSLT template → root directory as `bom2grouped_csv_jlcpcb.xsl`

## File Structure
```
./
├── bom2grouped_csv_jlcpcb.xsl    # XSLT template for BOM conversion
├── input/                         # Input directory for CSV/XML files
│   ├── your-board-top-pos.csv    # KiCad position file
│   └── your-board.xml            # KiCad netlist file in XML format
├── output/                        # Generated JLCPCB-compatible files
├── main.py                       # Main script
├── xml_converter.py              # BOM conversion helper
└── csv_header_replacer.py        # Position file converter
```

## KiCad Export Instructions

1. **Position Files (.csv)**
   - Open PCB in KiCad PCB Editor
   - File > Fabrication Outputs > Component Placement (.pos)
   - Select CSV format
   - Export to input directory

2. **Netlist Files (.xml)**
   - Open PCB in KiCad PCB Editor
   - File > Fabrication Outputs > Generate BOM
   - Select XML format
   - Export to input directory

## Usage Examples

### Basic Usage
```bash
# Process all files in input directory
python main.py

# Only convert position files
python main.py --replace-header

# Only convert BOM files
python main.py --convert-xml
```

### Component Position Adjustments
```bash
# Rotate components
python main.py --adjust-rotation "J2:-90,J3:-90"

# Move components (X/Y coordinates)
python main.py --adjust-x "C1:+1.5" --adjust-y "C1:-2.0"

# Combined adjustments
python main.py --adjust-rotation "J2:-90,J3:-90" --adjust-y "J2:-5.08,J3:-5.05"
```

## Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `--convert-xml` | Convert BOM XML to CSV | `--convert-xml` |
| `--replace-header` | Convert position files | `--replace-header` |
| `--adjust-rotation` | Adjust component rotation | `--adjust-rotation "C1:+90,R2:-180"` |
| `--adjust-x` | Adjust X coordinates | `--adjust-x "C1:+1.5,R2:-2.0"` |
| `--adjust-y` | Adjust Y coordinates | `--adjust-y "C1:+1.5,R2:-2.0"` |
| `--folder` | Input folder path | `--folder "./input"` |
| `--input` | Input file/folder | `--input "input/board.csv"` |
| `--output` | Output directory | `--output "output"` |

## File Format Conversion

### Position File
Input (KiCad):
```
Ref,Val,Package,PosX,PosY,Rot,Side
```

Output (JLCPCB):
```
Designator,Val,Package,Mid X,Mid Y,Rotation,Layer
```

### Notes
- Rotations are normalized to 0-360 degrees
- All adjustments are relative to current values
- Coordinates are in millimeters
- Layer is mapped from "top/bottom" to "Top/Bottom"
- Quotes in CSV files are handled automatically

## License

MIT License

## Links
- [GitHub Repository](https://github.com/koknovem/kicad-frabricate-jlcpcb-python)
- [KiCad Website](https://www.kicad.org/)
- [JLCPCB](https://jlcpcb.com/)