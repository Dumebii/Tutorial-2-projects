from brownie import accounts, config, PropertyAllocation

def deploy():
    pass

def main():
    #account = accounts.load("dumebi-account")
    #print(account)
    account = accounts.add(config["wallets"]["from_key"])
    #account = get_account
    Property_Allocation = PropertyAllocation.deploy({"from": account})
    print(Property_Allocation)
