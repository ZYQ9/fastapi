list1 = [
    {
        "labname": "sentinelOne",
        "status": "both"
    },
    {
        "labname": "crowdstrike",
        "status": "dev"
    },
    {
        "labname": "ngfw",
        "status": "dev"
    }
]
 
list2 = [
    {
        "Title": "sentinelOne",
        "asgsclod": "both"
    },
    {
        "Title": "crowdstrike",
        "asgsclod": "dev"
    },
    {
        "Title": "ngfw",
        "asgsclod": "dev"
    }
]

def compare_lists(list1,list2):
    for item1 in list1:
        if not any(item2["Title"] == item1["labname"] for item2 in list2):
            print(f"{item1['labname']} needs to be deleted")
        else:
            print(f"check {item1['labname']} status")

    for item2 in list2:
        if not any(item1["labname"] == item2["Title"] for item1 in list1):
            print(f"{item2['Title']} needs to be added")

compare_lists(list1,list2)