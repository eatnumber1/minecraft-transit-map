from lxml import etree
import sys

def get_viewbox_dimensions(root):
    """Extracts width and height from the SVG viewBox attribute."""
    viewbox = root.get('viewBox').split()
    return float(viewbox[2]), float(viewbox[3])

def combine_svgs(map_file, legend_file, output_file):
    """
    Combines two SVG files using the lxml library for robust handling
    of namespaces and coordinate systems, preventing xmlns redefinition.
    """
    # Parse the SVG files
    map_doc = etree.parse(map_file)
    map_root = map_doc.getroot()
    legend_doc = etree.parse(legend_file)
    legend_root = legend_doc.getroot()

    # Get dimensions from viewBox
    map_width, map_height = get_viewbox_dimensions(map_root)
    legend_width, legend_height = get_viewbox_dimensions(legend_root)

    # Calculate dimensions for the new SVG
    padding = 50
    total_width = legend_width + map_width + padding * 3
    total_height = max(map_height, legend_height) + padding * 2

    # Create a new, clean SVG root element
    new_root = etree.Element('svg', nsmap={
        None: "http://www.w3.org/2000/svg"
    })
    new_root.set('width', f'{total_width}pt')
    new_root.set('height', f'{total_height}pt')
    new_root.set('viewBox', f'0 0 {total_width} {total_height}')

    # Extract and place the legend content
    legend_content = legend_root.find('{http://www.w3.org/2000/svg}g')
    if legend_content is not None:
        legend_wrapper = etree.SubElement(new_root, 'g', {'transform': f'translate({padding}, {padding})'})
        legend_wrapper.append(legend_content)

    # Extract and place the map content
    map_content = map_root.find('{http://www.w3.org/2000/svg}g')
    if map_content is not None:
        map_wrapper = etree.SubElement(new_root, 'g', {'transform': f'translate({legend_width + padding * 2}, {padding})'})
        map_wrapper.append(map_content)

    # Write the new, clean SVG to the output file
    etree.ElementTree(new_root).write(output_file, pretty_print=True, xml_declaration=True, encoding='utf-8')

    # Print the final dimensions for ImageMagick
    print(f"{int(total_width)}x{int(total_height)}", file=sys.stderr)

if __name__ == '__main__':
    combine_svgs('map_body.svg', 'legend.svg', 'map.svg')
