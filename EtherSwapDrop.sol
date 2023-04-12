// SPDX-License-Identifier: MIT
pragma solidity 0.8.17;

/*

需求分析，首先启动的时候，将eth打入当前合约中。
然后调用swap, 将token按照一定的比例换成eth，转给调用方。
(success, ) = payable(msg.sender).call{value: amount}("");
*/

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract EtherSwapDrop{
    
    address public immutable owner;
    ERC20 public immutable supportingToken;
    uint16 public swapRate =1000;

    modifier onlyOwner(){
        require(msg.sender==owner,"only owner can operation");
        _;
    }

    event Swap(address indexed operator,uint256 amount);

    event BuyBackAndBurn(address indexed operator,uint256 amount);

    event WithdrawETH(address indexed operator,uint256 amount);

    event WithdrawToken(address indexed operator,uint256 amount);

    event Receive(address indexed operator,uint256 amount);

    constructor(address _supportingToken){
        supportingToken = ERC20(_supportingToken);
        owner = msg.sender;
    }

    function buyBackAndBurn(uint256 amount)external returns(bool success){
        require(amount>0,"can't be zero");
        uint256 ethAmount = amount/swapRate;
        require(supportingToken.balanceOf(msg.sender)>=amount,"token not enough");
        require(address(this).balance>=ethAmount,"eth not enough");
        //token直接转到0地址进行销毁. 前端ethers 调用报错
        supportingToken.transfer(address(0),amount);
        (success, ) = payable(msg.sender).call{value: ethAmount}("");
        emit BuyBackAndBurn(msg.sender,amount);
        return success;
    }

    /*
    回购LFT,将LFT转到当前合约中，并将eth转给发送方，安装固定的兑换比例
    */
    function buyBack(uint256 amount) external returns(bool success){
        require(amount>0,"can't be zero");
        uint256 ethAmount = amount/swapRate;
        require(supportingToken.balanceOf(msg.sender)>=amount,"token not enough");
        require(address(this).balance>=ethAmount,"eth not enough");
        //将用户的token转到合约中
        supportingToken.transferFrom(msg.sender,address(this),amount);
        //将合约中对应数量的eth返还给
        (success, ) = payable(msg.sender).call{value: ethAmount}("");
        emit Swap(msg.sender,amount);
        return success;
    }

    /*
    燃烧token
    */
    function burn(uint256 amount) external returns(bool){
        require(supportingToken.balanceOf(msg.sender)>=amount,"token not enough");
        //将币转到0地址
        supportingToken.transfer(address(0),amount);
        return true;
    }

    /*
    提现ETH
    */
    function withdrawETH(uint256 amount) external onlyOwner returns(bool success){
        require(address(this).balance>=amount,"eth not enough");
        (success, ) = payable(msg.sender).call{value: amount}("");
        emit WithdrawETH(msg.sender,amount);
        return success;
    }

    /*
    提现token
    */
    function withdrawToken(uint256 amount) external onlyOwner returns (bool){
        require(supportingToken.balanceOf(msg.sender)>=amount,"token not enough");
        supportingToken.transfer(msg.sender,amount);
        emit WithdrawToken(msg.sender,amount);
        return true;
    }


     /*
    接收eth 并且在offertoken余额充足的情况下, 把offeringtoken 转给调用方.  这里就直接相当于是ICO了
    */
    receive() external payable {
        //接收到eth,就给对方转 swapRate倍的 supportToken
        uint256 getTokenAmount = msg.value * swapRate;
        require(supportingToken.balanceOf(address(this)) >= getTokenAmount); //校验余额充足
        // 如果余额充足就给对方转接收到eth,就给对方转 1000倍的 supportToken
        supportingToken.transfer(msg.sender, getTokenAmount); //将合约中的offeringtoken转给调用方,也就是打eth进来的人
        emit Receive(msg.sender,msg.value);
    }
}
