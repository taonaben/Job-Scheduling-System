import pandas as pd

ER_df = pd.read_excel('Hospital ER.xlsx')


def comtime_sort_ascending(df):
    # SELECTION SORT ALGORITHM
    com_time = df['Completion Time(hrs)'].values.tolist()
    for i in range(len(com_time) - 1):
        min_index = i
        for j in range(i + 1, len(com_time)):
            if com_time[j] > com_time[min_index]:
                min_index = j
        if min_index != i:
            # Swap rows in DataFrame
            df.iloc[i], df.iloc[min_index] = df.iloc[min_index].copy(), df.iloc[i].copy()
            com_time[i], com_time[min_index] = com_time[min_index], com_time[i]

    return df


def comtime_sort_descending(df):
    # SELECTION SORT ALGORITHM
    com_time = df['Completion Time(hrs)'].values.tolist()
    for i in range(len(com_time) - 1):
        min_index = i
        for j in range(i + 1, len(com_time)):
            if com_time[j] > com_time[min_index]:
                min_index = j
        if min_index != i:
            # Swap rows in DataFrame
            df.iloc[i], df.iloc[min_index] = df.iloc[min_index].copy(), df.iloc[i].copy()
            com_time[i], com_time[min_index] = com_time[min_index], com_time[i]

    return df


def get_priority_array():
    # CONVERTS PRIORITY STRINGS TO INT, SO AS TO CREATE A MANIPULATABLE ARRAY
    priority = ER_df['Priority'].values.tolist()
    pri_ranks = []
    for pri in priority:
        if pri == "High":
            pri_ranks.append(3)
        elif pri == "Medium":
            pri_ranks.append(2)
        elif pri == "Low":
            pri_ranks.append(1)
    return pri_ranks


def priority_sort(df):
    # IMPLIMENTED SELECTION SORT ALGORITHM
    pri = get_priority_array()
    for i in range(len(pri) - 1):
        min_index = i
        for j in range(i + 1, len(pri)):
            if pri[j] > pri[min_index]:
                min_index = j
        if min_index != i:
            # Swap rows in DataFrame
            df.iloc[i], df.iloc[min_index] = df.iloc[min_index].copy(), df.iloc[i].copy()
            pri[i], pri[min_index] = pri[min_index], pri[i]

    return df


def save_prompt():
    save = input("Do you wish to save this order[y/n]: ")
    if save.lower() == "y":
        save_name = input("Save as: ")
        ER_df.to_excel(f"{save_name}.xlsx")
    elif save.lower() == "n":
        print("Exiting...")


def user_interface():
    print("WELCOME TO THE ER DEPARTMENT")

    view_df_prompt = input("View patients list[y/n]: ")
    if view_df_prompt.lower() == "y":
        print(ER_df)

        print("Sort list")
        sort_prompt = int(input("[1]-Optimization based on Priority: \n"
                                "[2]-Optimize based on Completion Time: "))

        if sort_prompt == 1:
            print(priority_sort(ER_df))
            save_prompt()
        elif sort_prompt == 2:
            order = int(input("[1]-Shortest finishing time first: \n"
                              "[2]-Longest finishing time first: "))

            if order == 1:
                print(comtime_sort_ascending(ER_df))
                save_prompt()

            elif order == 2:
                print(comtime_sort_descending(ER_df))
                save_prompt()
        else:
            print("Invalid input")
    elif view_df_prompt.lower() == "n":
        view_sorted_list = input("View sorted list[y/n]: ")
        if view_sorted_list.lower() == "y":
            sort_prompt = int(input("[1]-Optimization based on Priority: \n"
                                    "[2]-Optimize based on Completion Time: "))

            if sort_prompt == 1:
                print(priority_sort(ER_df))
                save_prompt()
            elif sort_prompt == 2:
                order = int(input("[1]-Shortest finishing time first: \n"
                                  "[2]-Longest finishing time first: "))

                if order == 1:
                    print(comtime_sort_ascending(ER_df))
                    save_prompt()
                elif order == 2:
                    print(comtime_sort_descending(ER_df))
                    save_prompt()
            else:
                print("Invalid input")
        elif view_sorted_list.lower() == "n":
            print("Exiting...")
        else:
            print("Invalid input!\nExiting...")

    else:
        print("Invalid input!")


if __name__ == "__main__":
    user_interface()
