# ibottle

去中心化漂流瓶ibottle

一、项目思路逻辑及Solidity版本

https://github.com/lrqstudy/learn-smart-contract/blob/main/DriftBottleV7BaseChain.sol

这个项目是我自己初学solidity写的一个example，交友类dapp，跟我们通常玩的漂流瓶类似。

1. 首先用户需要注册，购买NFT，作为赠送我们给用户token（LFT lifetogo），注册信息中包括基本的用户名，年龄，性别等信息，注册一次获得100point积分（参数可设置）

2. 用户注册完成后，获得NFT和对应的LFT token，刚开始玩必须先丢瓶子，每丢一次花费5LFT（参数可设置），该部分token归平台所有，瓶子里存放的是打招呼用语及本人的社交id，如wechat。，丢瓶子消费多少获得相应的积分。

3. 用户还可以捡瓶子，捡瓶子一次花50LFT，其中95%给丢瓶子的人，5%作为平台手续费（比例参数可设置），捡瓶子也类似，消费多少获得多少积分。
   捡瓶子的逻辑是，只有捡的人才能看到瓶子中的内容，其它人无权限看到瓶子中的内容。

4. 用户的token不够了，可以用ETH进行购买。

存在的问题：关键信息链上泄漏，因为漂流瓶的数据是直接存放在链上的storage中的，同时可以在区块链浏览器中找到信息，无法做到只让付钱的人看。

这是大概的业务逻辑，在第一个版本中，这个漂流瓶的数据是直接存放在链上的storage中的，同时可以在区块链浏览器中找到信息，只要用户懂区块链，就不需要去捡瓶子，直接去链上捞获取wechat就好了。

二、Solidity+中心化服务器信息加密版本

由于第一个版本的逻辑bug，因此我设计了一个中心化服务器，将核心关键信息在服务端加密后，再写入storage中，取到时候，先从链上获取，然后再通过服务器后端解密，供前端展示。

中心化服务器对于信息的加密解密，解决了基本的业务逻辑问题，程序可以实现基本的功能，但是还是类似web2.5的style


存在的问题：需要依赖中心化服务器提供加解密服务。很不web3


三、Cairo版本实现及DH密钥共享算法-链上信息加密

而新的版本，我想用Cairo合约完成，去掉服务端加解密的代码，其实我们的需求就是这个，如何安全的对链上数据进行隐藏加密解密，只有对应的付钱捡起瓶子的人才能看到瓶子中的内容。合约基本逻辑部分用Cairo进行实现。 而链上信息加密的功能，使用DH密钥共享算法。

我这个项目借鉴了 这个项目https://www.privatemarket.dev/whatisthis 
privatemarket 这个网站是卖地址的私钥的，核心就是用了DH密钥互换和zk凭证算法。

1. 介绍DH密钥交换算法： https://zh.wikipedia.org/zh-sg/%E8%BF%AA%E8%8F%B2-%E8%B5%AB%E7%88%BE%E6%9B%BC%E5%AF%86%E9%91%B0%E4%BA%A4%E6%8F%9B

2. 密钥互换算法python代码演示及openssl库实现



3. ibottle项目业务流程处理思路

3.1 Alice丢瓶子，用DH算法计算出的public key，随机的素数，和他的原根值， 和他要放入的漂流瓶的信息的（我是Alice，我的微信号lrqstudy）hash值写入区块链中。此时瓶子的状态为1

	write(alice_public_key,prime_number,primitive_root_number, bottlt_message_hash)
	write(bottle_status,1)


3.2 Bob去区块链上捡到了Alice的瓶子，得到了Alice的public key ，用自己的私钥计算出Alice的共享key，并将共享key的hash和 自己用DH算法计算出的public key写入到区块链中，同时支付捡瓶子的费用到合约中。此时瓶子的状态从1变成了2
   
   read(alice_public_key,prime_number,primitive_root_number)
   share_key = calculate_share_key(bob_private_key,prime_number,primitive_root_number,alice_public_key)
   write(share_key_hash,bob_public_key) 
   pay_fee(50LFT)
   write(bottle_status,2)

3.3 Alice接收到bob捡它瓶子的需求
   获取到Bob提供的DH算法public key，计算两人的共享key的hash，跟Bob提交到链上的共享key 的哈希值进行比对，共享key比对一致后（防止Bob传错了共享key），将自己想放入的瓶子的内容（我是Alice，我的微信号是lrqstudy）用两者的共享key进行加密后放到区块链中。 此时瓶子的状态从2变成了3
	
	read(bob_public_key,share_key_hash)
	share_key = calculate_share_key(bob_public_key)
	check_share_key_hash(share_key,share_key_hash)
	encode_bottle_message(bottle_message,share_key)
	write(bottle_encode_message)
	write(bottle_status,3)

3.4 第四步，Bob看到Alice接受了请求，Bob获取链上用共享key加密的漂流瓶内容，并用共享key对获取的漂流瓶内容进行解密，获得原始漂流瓶内容，对漂流瓶内容数据取hash，跟alice 在第一步中提交的漂流瓶内容的hash进行比对，防止alice在第三步中作恶。如果一致，则确认交易完成了。
	
   read(bottle_encode_message,bottle_message_hash)
   decode_bottle_message(bottle_encode,message,share_key)
   check()
   confirm_pay()
   write(bottle_status,4)

注意：DH算法生产环境建议使用openssl的dh实现库。

总结核心就在于如何确保链上信息存储的安全性，又能实现信息交换的需求，类似的需求还有很多，其实这也属于隐私一类。 

这是整体的思路，剩下的就是用cairo语言去实现上面的代码，部分还需要结合前端进行实现。












