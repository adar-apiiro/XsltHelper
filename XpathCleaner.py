import re
from lxml import etree

def remove_xpath_indexes(xpath: str) -> str:
    return re.sub(r'\[\d+\]', '', xpath)

def normalize_xpath(xpath: str) -> str:
    return re.sub(r'//+', '/', xpath.strip())

def replace_nodes_with_wildcards(xpath: str, node_names: list) -> str:
    for node in node_names:
        xpath = xpath.replace(node, '*')
    return xpath

def find_common_prefix(xpaths: list) -> str:
    common_prefix = xpaths[0].split('/')
    for xpath in xpaths[1:]:
        xpath_parts = xpath.split('/')
        common_prefix = [c for i, c in enumerate(common_prefix) if i < len(xpath_parts) and c == xpath_parts[i]]
    return '/'.join(common_prefix)

def xpath_to_css(xpath: str) -> str:
    css = xpath.replace('/', ' > ').replace('[', ':nth-of-type(').replace(']', ')')
    css = re.sub(r"@([\w-]+)", r"[\1]", css)
    return css

def extract_node_names(xpath: str) -> list:
    xpath = re.sub(r'\[\d+\]', '', xpath)
    return [node for node in xpath.split('/') if node]

def is_valid_xpath(xpath: str) -> bool:
    try:
        etree.XPath(xpath)
        return True
    except etree.XPathSyntaxError:
        return False

def extract_attributes(xpath: str) -> list:
    return re.findall(r'@([\w-]+)="([^"]+)"', xpath)

def beautify_xpath(xpath: str) -> str:
    return "\n".join([" " * i + part for i, part in enumerate(xpath.split("/")) if part])

def autocomplete_xpath(xpath: str) -> str:
    return xpath + '/*' * (5 - xpath.count('/'))

def ask_for_methods():
    print("\nAvailable Methods:")
    print("1. Remove XPath Indexes")
    print("2. Normalize XPath")
    print("3. Replace Nodes with Wildcards")
    print("4. Find Common Parent Node (For multiple XPaths)")
    print("5. Convert XPath to CSS Selector")
    print("6. Extract Node Names from XPath")
    print("7. Validate XPath")
    print("8. Extract Attributes from XPath")
    print("9. Beautify XPath")
    print("10. Autocomplete XPath")

    selected_methods = input("Please enter the numbers of the methods you'd like to apply (comma separated): ")
    return [int(x.strip()) for x in selected_methods.split(',')]

def main():
    while True:
        xpath_input = input("\nPlease enter the XPath: ")
        methods = ask_for_methods()

        if 1 in methods:
            xpath_input = remove_xpath_indexes(xpath_input)
            print("Removed Indexes XPath:", xpath_input)

        if 2 in methods:
            xpath_input = normalize_xpath(xpath_input)
            print("Normalized XPath:", xpath_input)

        if 3 in methods:
            node_names = input("Enter the node names to replace with wildcards (comma separated): ").split(',')
            xpath_input = replace_nodes_with_wildcards(xpath_input, node_names)
            print("Wildcard XPath:", xpath_input)

        if 4 in methods:
            xpaths = []
            while True:
                xpath = input("Enter another XPath (or 'done' to finish): ")
                if xpath.lower() == 'done':
                    break
                xpaths.append(xpath)
            if xpaths:
                common_parent = find_common_prefix(xpaths)
                print("Common Parent Node:", common_parent)

        if 5 in methods:
            css_selector = xpath_to_css(xpath_input)
            print("CSS Selector:", css_selector)

        if 6 in methods:
            node_names = extract_node_names(xpath_input)
            print("Node Names:", node_names)

        if 7 in methods:
            is_valid = is_valid_xpath(xpath_input)
            print("Is valid XPath:", is_valid)

        if 8 in methods:
            attributes = extract_attributes(xpath_input)
            print("Attributes:", attributes)

        if 9 in methods:
            pretty_xpath = beautify_xpath(xpath_input)
            print("Beautified XPath:\n", pretty_xpath)

        if 10 in methods:
            autocompleted_xpath = autocomplete_xpath(xpath_input)
            print("Autocompleted XPath:", autocompleted_xpath)

        another_round = input("\nDo you need help with another XPath? (yes/no): ")
        if another_round.lower() != 'yes':
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()
