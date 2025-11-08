import os
import random
import string

ELEMENTS = ["letter", "note", "message", "entry", "record", "item", "doc"]

def random_letter():
    """Return a single random uppercase letter."""
    return random.choice(string.ascii_uppercase)

def write_element(f, depth=0, max_depth=10):
    """
    Write a random element with a letter attribute.
    Randomly decide whether to nest children.
    """
    tag = random.choice(ELEMENTS)
    letter_val = random_letter()
    indent = "  " * depth
    f.write(f'{indent}<{tag} letter="{letter_val}">\n')

    # Randomly add children if depth < max_depth
    if depth < max_depth and random.random() < 0.5:
        num_children = random.randint(1, 5)
        for _ in range(num_children):
            write_element(f, depth + 1, max_depth)

    f.write(f'{indent}</{tag}>\n')

def generate_large_xml(filename="huge_nested.xml", target_size_mb=300):
    target_size_bytes = target_size_mb * 1024 * 1024
    written = 0

    with open(filename, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<root>\n')
        written = f.tell()

        while written < target_size_bytes:
            write_element(f, depth=1, max_depth=9)
            written = f.tell()

        f.write('</root>\n')

    print(f"XML file '{filename}' created with size {os.path.getsize(filename)/(1024*1024):.2f} MB")

if __name__ == "__main__":
    generate_large_xml("example.xml", target_size_mb=100)

