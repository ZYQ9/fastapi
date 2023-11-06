from pandas import DataFrame
import pandas as pd 

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
    },
    {
        "labname": "fortigate",
        "status": "dev"
    },
    {
        "labname": "pan",
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
    },
    {
        "Title": "Cisco",
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

# def compare_lists2(list1: list,list2: list) -> bool: 

#     df1 = pd.DataFrame(list1)
#     df2 = pd.DataFrame(list2)
#     diff = dataframe_difference(df1,df2)
#     result = len(diff) == 0
#     if not result:
#         print(f'There are {len(diff)} differences: \n {diff.head()}')
#     return result

# def dataframe_difference(df1: DataFrame, df2: DataFrame) -> DataFrame:
    
#     comparison_df = df1.merge(df2, indicator=True, how='outer')
#     diff_df = comparison_df[comparison_df['merge'] != 'both']
#     return diff_df

# print(compare_lists2(list1,list2))

df1 = pd.DataFrame(list1)
df2 = pd.DataFrame(list2)
# df2.rename(columns={'Title':'labname','asgclod':'status'},inplace=True)

print(df1)
print('\n')
print(df2)
print('\n')

missing_in_df2 = df1.loc[~df1['labname'].isin(df2['Title'])]
missing_in_df1 = df2.loc[~df2['Title'].isin(df1['labname'])]

print(missing_in_df2)
print('\n')
print(missing_in_df1)

print(missing_in_df1['labname'])