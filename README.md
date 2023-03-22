# txtAwards

A decentralised system that allows educational institutions to issue micro-credentials signed by students and later verified by potential employers. The system is designed with the core principle of operating in a decentralised environment without the need for a central authority. The system can be accessed by institutions, students, and employers globally, without registration or reliance on third-party servers, leading to reduced costs and an uptime guarantee. The system makes use of the Polygon Blockchain.

[Tutorial video](https://youtu.be/HtQByfBWKdA)

[Whitepaper]()

## Release
The release makes use of the Polygon Blockchain (Mainnet). You don't need to install anything since the project is compiled into a portable application. Educational institutions need some MATIC tokens to award students. For this application, MATIC is only used for gas (transaction) fees which is determined by the supply and demand of the Polygon network. MATIC can be purchased from a cryptocurrency exchange such as coinbase.com. 

System makes use of the following endpoints:
 - Infura https://www.infura.io/
 - Polygon Gas Station https://wiki.polygon.technology/docs/develop/tools/polygon-gas-station/

## Development
The project comes with two folders: *app* and *contracts*. The *app* folder contains all the python code for this application. The *contracts* folder has all the smart contracts in solidity. 

### Installation
To run this project you are required to install the following:

 - Python 3.8.0 https://www.python.org/downloads/release/python-380/
 - Hardhat https://hardhat.org/
 - VS Code https://code.visualstudio.com/

The application comes with multiple packages which needs to be installed. Inside the terminal, open the *app* folder and create a virtual environment for our python application.

**Create a virtual environment**

    python -m venv venv

**Activate environment**

    venv\Scripts\activate.bat

**Install packages**

    python -m pip install -r requirements.txt

**ENV File**

Inside the root of the *app* folder we need to create a `.env` file. In our case, we are going to connect locally to Hardhat, so it is suggested to add the below variables. You can easily replace the web3 provider to your preference. 

    WEB3_HTTPProvider=HTTP://127.0.0.1:8545
    POLYGON_GAS_STATION=https://gasstation-mainnet.matic.network/v2

**Compiling contracts**
 
For our case, we are going to compile the solidity contracts using Hardhat. To do this open the *contracts* folder inside the terminal and install the OpenZeppelin libraries as described here: https://docs.openzeppelin.com/upgrades-plugins/1.x/hardhat-upgrades

Then run the following command:

    npx hardhat compile

To test the contracts you can simply run:

    npx hardhat test

### Running Application

To run the application, open the *contracts* folder inside the terminal and run the following command:

    npx hardhat node

Once the node is up and running,  open the *app* folder in the terminal and run the following command:

    python main.py

Your application should start and you should see the welcome screen.

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)