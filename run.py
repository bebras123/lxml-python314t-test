import time
from concurrent.futures import ThreadPoolExecutor
from lxml import etree

# Path to your XML file
XML_FILE = "example.xml"

def load_xml(path):
    with open(path, "rb") as f:
        tree = etree.parse(f)
    return tree

def check_xpath(tree, xpath_expr, description):
    results = tree.xpath(xpath_expr)
    print(f"[{description}] XPath: {xpath_expr}")
    print(f"  -> {len(results)}" if results else "  -> No matches found")

def main(max_threads=None):
    tree = load_xml(XML_FILE)

    all_checks = [
        ("//letter", "letters"),
        ("//entry", "entries"),
        ("//doc", "docs"),
        ("//other", "others"),
        ("//note", "notes"),
        ("//message", "messages"),
        ("//item", "items"),
        ("//letter", "letters"),
        ("//entry", "entries"),
        ("//doc", "docs"),
        ("//other", "others"),
        ("//note", "notes"),
        ("//message", "messages"),
        ("//item", "items"),
        ("//letter", "letters"),
        ("//entry", "entries"),
        ("//doc", "docs"),
        ("//other", "others"),
        ("//note", "notes"),
        ("//message", "messages"),
        ("//item", "items"),
    ]
    if max_threads is None:
        max_threads = len(all_checks)

    # Run checks with a thread pool
    beg = time.time()
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [executor.submit(check_xpath, tree, xp, desc) for xp, desc in all_checks]
        for f in futures:
            f.result()  # wait for completion

    print(f"Time {time.time() - beg:.2f}s")

if __name__ == "__main__":
    # You can change these values as needed
    main(max_threads=8)

