import heapq
from collections import Counter, namedtuple
import math


# Node structure for Huffman tree
class Node(namedtuple("Node", ["char", "freq", "left", "right"])):
    def __lt__(self, other):
        return self.freq < other.freq


# Function to build the Huffman tree
def build_huffman_tree(frequencies):
    heap = [Node(char, freq, None, None) for char, freq in frequencies.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(None, left.freq + right.freq, left, right)
        heapq.heappush(heap, merged)

    return heap[0]


# Function to generate Huffman codes
def generate_huffman_codes(tree):
    codes = {}

    def _generate_codes(node, current_code):
        if node.char is not None:
            codes[node.char] = current_code
            return
        if node.left:
            _generate_codes(node.left, current_code + "0")
        if node.right:
            _generate_codes(node.right, current_code + "1")

    _generate_codes(tree, "")
    return codes


# Function to calculate entropy
def calculate_entropy(frequencies, total_chars):
    entropy = 0
    for freq in frequencies.values():
        prob = freq / total_chars
        entropy -= prob * math.log2(prob)
    return entropy


# Function to calculate encoding lengths
def calculate_lengths(frequencies, codes):
    huffman_length = sum(frequencies[char] * len(code) for char, code in codes.items())
    return huffman_length


# Function to calculate average bits per character
def calculate_avg_bits_per_char(huffman_length, total_chars):
    return huffman_length / total_chars


# Function to calculate compression percentage
def calculate_compression(ascii_length, huffman_length):
    return ((ascii_length - huffman_length) / ascii_length) * 100


# Load the text file and preprocess
file_path = "To_Build_A_Fire.txt"
with open(file_path, "r", encoding="utf-8") as file:
    text = file.read().lower().replace("\n", "")  # Convert to lowercase and remove newlines

# Count all characters, including spaces and punctuation
frequencies = Counter(text)
total_chars = sum(frequencies.values())

# Display character frequencies
print("Total Characters:", total_chars)
print("\nCharacter Frequency Count:")
for char, freq in frequencies.items():
    print(f"'{char}': {freq}")

# Step 2: Build Huffman tree
huffman_tree = build_huffman_tree(frequencies)

# Step 3: Generate Huffman codes
huffman_codes = generate_huffman_codes(huffman_tree)

# Step 4: Calculate entropy
entropy = calculate_entropy(frequencies, total_chars)

# Step 5: Calculate ASCII and Huffman encoding lengths
ascii_length = total_chars * 8
huffman_length = calculate_lengths(frequencies, huffman_codes)

# Step 6: Calculate average bits per character using Huffman coding
avg_bits_per_char = calculate_avg_bits_per_char(huffman_length, total_chars)

# Step 7: Calculate compression percentage
compression_percentage = calculate_compression(ascii_length, huffman_length)

# Display results
print("\nResults:")
print("Entropy (bits per character):", entropy)
print("ASCII Encoding Length (bits):", ascii_length)
print("Huffman Encoding Length (bits):", huffman_length)
print("Average Bits per Character (Huffman):", avg_bits_per_char)
print("Compression Percentage:", compression_percentage)

# Display full table of character frequencies and codes
table = [(char, freq, f"{freq / total_chars:.6f}", huffman_codes[char], len(huffman_codes[char])) for char, freq in
         frequencies.items()]
print("\nCharacter Frequencies and Codes:")
print("Char | Frequency | Probability | Huffman Code | Code Length")
for row in table:
    print(f"{repr(row[0])}    | {row[1]}        | {row[2]}       | {row[3]}         | {row[4]}")
