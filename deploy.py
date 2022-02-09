from brownie import accounts, config, ERC20tokens

def deploy_ERC20TOKENS():
    pass

def main():
    #account = accounts.load("dumebi-account")
    #print(account)
    account = accounts.add(config["wallets"]["from_key"])
    #account = get_account
    ERC_TOKENS = ERC20tokens.deploy({"from": account})
    print(ERC_TOKENS)
