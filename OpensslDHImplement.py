import datetime
from cryptography.hazmat.primitives.asymmetric import dh

print(datetime.datetime.now())
# 测试钱包 A 的私钥
private_key_wallet_a = 0x111
# 测试钱包 B 的私钥
private_key_wallet_b = 0x222
# 使用 OpenSSL 的 DH 参数
parameters = dh.generate_parameters(generator=2, key_size=2048)

# 使用钱包 A 的私钥创建 DH 私钥对象
private_key_dh_wallet_a = parameters.generate_private_key(
)

# 使用钱包 B 的私钥创建 DH 私钥对象
private_key_dh_wallet_b = parameters.generate_private_key(
)

# 生成钱包 A 和钱包 B 的 DH 公钥
public_key_dh_wallet_a = private_key_dh_wallet_a.public_key()
public_key_dh_wallet_b = private_key_dh_wallet_b.public_key()

# 执行 Diffie-Hellman 密钥交换，生成共享密钥 C
shared_key_wallet_a = private_key_dh_wallet_a.exchange(public_key_dh_wallet_b)
shared_key_wallet_b = private_key_dh_wallet_b.exchange(public_key_dh_wallet_a)

# 打印生成的密钥
print("Wallet A's Shared Key:")
print(shared_key_wallet_a.hex())
print("\nWallet B's Shared Key:")
print(shared_key_wallet_b.hex())
print(datetime.datetime.now())


# 使用共享密钥 C 对消息进行加密解密 TODO
