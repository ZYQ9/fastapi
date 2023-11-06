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
    set_list1 = set(tuple(d.items()) for d in list1)
    set_list2 = set(tuple(d.items()) for d in list2)

    set_diff = set_list1.symmetric_difference(set_list2)

    return set_diff

print(compare_lists(list1,list2))