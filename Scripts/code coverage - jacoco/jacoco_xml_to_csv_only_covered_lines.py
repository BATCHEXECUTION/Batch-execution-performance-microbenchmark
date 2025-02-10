import xml.etree.ElementTree as ET
import csv
import sys
import re

def extract_namespace(element):
    """
    Extracts the namespace from an XML element tag.
    For example, given '{http://www.eclemma.org/jacoco/report}report'
    it returns 'http://www.eclemma.org/jacoco/report'.
    """
    m = re.match(r'\{(.*)\}', element.tag)
    return m.group(1) if m else ''

def extract_data(xml_file, csv_file):
    """
    Extracts data from a JaCoCo XML coverage report and writes to a CSV file only
    for source files that have covered lines (ci != "0").
    
    Args:
        xml_file (str): Path to the input JaCoCo XML coverage report.
        csv_file (str): Path to the output CSV file.
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Handle namespace if present
    namespace = extract_namespace(root)
    if namespace:
        ns = {'ns': namespace}
        package_tag = 'ns:package'
        sourcefile_tag = 'ns:sourcefile'
        line_tag = 'ns:line'
    else:
        ns = {}
        package_tag = 'package'
        sourcefile_tag = 'sourcefile'
        line_tag = 'line'

    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Package Name', 'Class Name', 'Covered Lines'])

        packages = root.findall('.//' + package_tag, ns)
        for package in packages:
            package_name = package.get('name')
            sourcefiles = package.findall(sourcefile_tag, ns)
            if not sourcefiles:
                continue
            for sourcefile in sourcefiles:
                class_name = sourcefile.get('name')
                covered_lines = []
                # Get all line elements and filter in Python
                lines = sourcefile.findall(line_tag, ns)
                for line in lines:
                    if line.get('ci') != "0":
                        line_number = line.get('nr')
                        if line_number:
                            covered_lines.append(line_number)
                if covered_lines:
                    writer.writerow([package_name, class_name, ';'.join(covered_lines)])

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_jacoco_xml_report> <output_extracted_data.csv>")
        sys.exit(1)
    input_xml = sys.argv[1]
    output_csv = sys.argv[2]
    extract_data(input_xml, output_csv)