import xml.etree.ElementTree as ET
import re
from xml.dom import minidom

# Hardcoded XML AST
xml_string = """

"""

# Function to remove unnecessary attributes from the XML
def clean_ast_attributes(xml_tree, attributes_to_remove):
    for elem in xml_tree.iter():
        for attr in attributes_to_remove:
            if attr in elem.attrib:
                del elem.attrib[attr]
    return xml_tree

# Function to pretty print the XML tree after cleaning
def prettify(elem):
    """Return a pretty-printed XML string for the Element."""
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="    ")

# Function to remove XPath indexes
def remove_xpath_indexes(xpath: str) -> str:
    return re.sub(r'\[\d+\]', '', xpath)

# Function to extract node names from the AST and generate XPath
def generate_xpath(elem):
    paths = []
    for e in elem.iter():
        if e.tag:
            path = []
            for parent in e.iterancestors():
                path.insert(0, parent.tag)
            path.append(e.tag)
            paths.append("/" + "/".join(path))
    return paths

# Function to find the common ancestor for two or more XPaths
def find_common_parent(xpaths):
    split_xpaths = [xpath.split('/') for xpath in xpaths]
    common_path = []

    for i in range(min(len(path) for path in split_xpaths)):
        if all(path[i] == split_xpaths[0][i] for path in split_xpaths):
            common_path.append(split_xpaths[0][i])
        else:
            break

    return "/" + "/".join(common_path)

# Menu function to interact with the user
def menu():
    print("\nMenu:")
    print("1. Clean specific attributes (e.g., Order, StartLine, etc.)")
    print("2. Generate XPaths from the XML tree")
    print("3. Remove indexes from an XPath")
    print("4. Pretty print the cleaned XML")
    print("5. Find common parent for two or more XPaths")
    print("6. Exit")
    choice = input("Choose an option (1-6): ")
    return choice

# Main function to run the menu and handle user choices
def main():
    try:
        # Parse the hardcoded XML string
        root = ET.fromstring(xml_string)

        while True:
            choice = menu()

            if choice == '1':
                # Clean specific attributes
                attributes_to_remove = input("Enter the attributes you want to remove (comma-separated): ").split(',')
                attributes_to_remove = [attr.strip() for attr in attributes_to_remove]
                cleaned_tree = clean_ast_attributes(root, attributes_to_remove)
                print("Attributes removed. Use option 4 to see the cleaned XML.")

            elif choice == '2':
                # Generate XPath
                xpaths = generate_xpath(root)
                print("Generated XPaths:")
                for xpath in xpaths:
                    print(xpath)

            elif choice == '3':
                # Remove indexes from XPath
                xpath_input = input("Enter the XPath with indexes to remove: ")
                cleaned_xpath = remove_xpath_indexes(xpath_input)
                print("Cleaned XPath:", cleaned_xpath)

            elif choice == '4':
                # Pretty print the cleaned XML
                print("Cleaned XML AST:")
                print(prettify(root))

            elif choice == '5':
                # Find common parent for two or more XPaths
                xpaths = []
                while True:
                    xpath = input("Enter an XPath (or type 'done' to finish): ")
                    if xpath.lower() == 'done':
                        break
                    xpaths.append(xpath)

                if len(xpaths) >= 2:
                    common_parent = find_common_parent(xpaths)
                    print("Common Parent XPath:", common_parent)
                else:
                    print("Please enter at least two XPaths.")

            elif choice == '6':
                # Exit the script
                print("Exiting...")
                break

            else:
                print("Invalid option. Please choose a number between 1 and 6.")

    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")

if __name__ == "__main__":
    main()
