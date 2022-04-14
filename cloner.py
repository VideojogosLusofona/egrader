from git import Repo

group_repo = {}
with open("repos.txt") as grfile:
    for line in grfile:
        data = line.split()
        group_repo[data[0]] = data[1]

for key in group_repo.keys():
    print(f"{key}: {group_repo[key]}")
    repo = Repo.clone_from(group_repo[key], f"entregas/{key}")
    
for key in group_repo.keys():
    print(f"{key}_MIRROR: {group_repo[key]}")
    repo = Repo.clone_from(group_repo[key], f"entregas/{key}_MIRROR", multi_options=['--mirror'])
    
    
    
    
