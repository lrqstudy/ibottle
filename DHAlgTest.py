# Diffie-Hellman key exchange implementation

def power(base, exponent, modulus):
    result = 1
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exponent //= 2
    return result


def diffie_hellman(p, g, alice_private, bob_private):
    A = power(g, alice_private, p)
    B = power(g, bob_private, p)
    secret_key_A = power(B, alice_private, p)
    secret_key_B = power(A, bob_private, p)
    return secret_key_A, secret_key_B

# 1 准备一个素数p和它的一个原根g
p = 104729  # A prime number, known to both parties
g = 2  # 104729的原根之一2


# 2. alice用自己的私钥，计算出DH算法的公钥alice_pub 并共享出去
private_key_alice = 0x1234abcd
alice_pub = power(g, private_key_alice, p)


# 3. bob用自己的私钥，计算出DH算法的公钥bob_pub 并共享出去
private_key_bob = 0xabcd1234
bob_pub = power(g, private_key_bob, p)

# 4. alice用自己的私钥，和bob提供的DH算法公钥bob_pub，计算出共享密钥alice_share_key
alice_share_key = power(bob_pub, private_key_alice, p)


#5. bob用自己的私钥，和alice提供的DH算法公钥alice_pub，计算出共享密钥bob_share_key
bob_share_key = power(alice_pub, private_key_bob, p)

print("Shared secret key for Alice:", alice_share_key)
print("Shared secret key for Bob:", bob_share_key)

# 6. alice和bob计算出来的共享密钥是一样的，说明算法正确

# 下面这个是把整个步骤进行聚合Calculate shared secret keys
shared_secret_alice, shared_secret_bob = diffie_hellman(p, g, private_key_alice, private_key_bob)
print("Shared secret key for Alice:", shared_secret_alice)
print("Shared secret key for Bob:", shared_secret_bob)

# 7. 正确做法，使用opssl的DH算法库

