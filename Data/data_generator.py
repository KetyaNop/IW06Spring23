import random

protein_alphabet = [
    "A",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "K",
    "L",
    "M",
    "N",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "V",
    "W",
    "Y",
]
print("Creating Random Protein Sequence")
protein = ""
for i in range(1280000):
    protein = protein + random.choice(protein_alphabet)

with open("Protein.txt", "w") as text_file:
    print(protein, file=text_file)

print("Creating Random Bit String")
bit_string_alphabet = ["0", "1"]
bit_string = ""
for i in range(1280000):
    bit_string = bit_string + random.choice(bit_string_alphabet)

with open("BitString.txt", "w") as text_file:
    print(bit_string, file=text_file)
