from f5.bigip import ManagementRoot

# Connect to the BigIP
mgmt = ManagementRoot("ngf5p7.ngdata.no", "admin", "password")

# Get a list of all pools on the BigIP and print their names and their
# members' names
pools = mgmt.tm.ltm.pools.get_collection()
for pool in pools:
    print(pool.name)
    for member in pool.members_s.get_collection():     
        print(member.name)