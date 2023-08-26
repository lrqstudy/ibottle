def is_primitive_root(g, p):
    residues = set()
    for i in range(1, p):
        residue = (g ** i) % p
        if residue in residues:
            return False
        residues.add(residue)
    return len(residues) == p - 1

def find_primitive_roots(p):
    primitive_roots = []
    for g in range(2, p):
        if is_primitive_root(g, p):
            primitive_roots.append(g)
    return primitive_roots

#prime_number = int(input("Enter a prime number: "))
prime_number = 137

primitive_roots = find_primitive_roots(prime_number)
print(f"Primitive roots of {prime_number}: {primitive_roots}")
