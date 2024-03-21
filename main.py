import pandas as pd


class Scheduler:
    def __init__(self, file_path):
        self.ER_df = pd.read_excel(file_path)
        self.display_cols = [
            "Patient ID",
            "Patient Name",
            "Age",
            "Sex",
            "Admission Date",
            "Admission Type"
        ]
        self.display_df = self.ER_df.reindex(columns=self.display_cols)

        self.pri_cols = [
            "Patient ID",
            "Patient Name",
            "Age",
            "Sex",
            "Priority"
        ]
        self.pri_df = self.ER_df.reindex(columns=self.pri_cols)

        self.comTime_cols = [
            "Patient ID",
            "Patient Name",
            "Age",
            "Sex",
            "Operation Completion Time(hrs)"
        ]
        self.comTime_df = self.ER_df.reindex(columns=self.comTime_cols)

    def comtime_sort_ascending(self, df):
        com_time = df['Operation Completion Time(hrs)'].values.tolist()
        for i in range(len(com_time) - 1):
            min_index = i
            for j in range(i + 1, len(com_time)):
                if com_time[j] < com_time[min_index]:
                    min_index = j
            if min_index != i:
                df.iloc[i], df.iloc[min_index] = df.iloc[min_index].copy(), df.iloc[i].copy()
                com_time[i], com_time[min_index] = com_time[min_index], com_time[i]
        return df

    def comtime_sort_descending(self, df):
        com_time = df['Operation Completion Time(hrs)'].values.tolist()
        for i in range(len(com_time) - 1):
            min_index = i
            for j in range(i + 1, len(com_time)):
                if com_time[j] > com_time[min_index]:
                    min_index = j
            if min_index != i:
                df.iloc[i], df.iloc[min_index] = df.iloc[min_index].copy(), df.iloc[i].copy()
                com_time[i], com_time[min_index] = com_time[min_index], com_time[i]
        return df

    def get_priority_array(self):
        priority = self.ER_df['Priority'].values.tolist()
        pri_ranks = []
        for pri in priority:
            if pri == "High":
                pri_ranks.append(3)
            elif pri == "Medium":
                pri_ranks.append(2)
            elif pri == "Low":
                pri_ranks.append(1)
        return pri_ranks

    def priority_sort(self, df):
        pri = self.get_priority_array()
        for i in range(len(pri) - 1):
            min_index = i
            for j in range(i + 1, len(pri)):
                if pri[j] > pri[min_index]:
                    min_index = j
            if min_index != i:
                df.iloc[i], df.iloc[min_index] = df.iloc[min_index].copy(), df.iloc[i].copy()
                pri[i], pri[min_index] = pri[min_index], pri[i]
        return df

    def save_prompt(self, df):
        save = input("Do you wish to save this order[y/n]: ")
        if save.lower() == "y":
            save_name = input("Save as: ")
            df.to_excel(f"{save_name}.xlsx")
        elif save.lower() == "n":
            print("Exiting...")

    def com_time_sort_prompt(self):
        order = int(input("[1]-Shortest finishing time first: \n"
                          "[2]-Longest finishing time first: "))

        if order == 1:
            self.comtime_sort_ascending(self.comTime_df)
            print(self.comTime_df)
            self.save_prompt(self.comTime_df)

        elif order == 2:
            self.comtime_sort_descending(self.comTime_df)
            print(self.comTime_df)
            self.save_prompt(self.comTime_df)

        else:
            print("Invalid input")

    def priority_sort_prompt(self):
        self.priority_sort(self.pri_df)
        print(self.pri_df)
        self.save_prompt(self.pri_df)

    def user_interface(self):

        view_df_prompt = input("View patients list[y/n]: ")
        if view_df_prompt.lower() == "y":
            print(self.display_df)

            print("Sort list")
            sort_prompt = int(input("[1]-Optimization based on Priority: \n"
                                    "[2]-Optimize based on Completion Time: "))

            if sort_prompt == 1:
                self.priority_sort_prompt()
            elif sort_prompt == 2:
                self.com_time_sort_prompt()

        elif view_df_prompt.lower() == "n":
            view_sorted_list = input("View sorted list[y/n]: ")
            if view_sorted_list.lower() == "y":
                sort_prompt = int(input("[1]-Optimization based on Priority: \n"
                                        "[2]-Optimize based on Completion Time: "))

                if sort_prompt == 1:
                    self.priority_sort_prompt()
                elif sort_prompt == 2:
                    self.com_time_sort_prompt()
            elif view_sorted_list.lower() == "n":
                print("Exiting...")
            else:
                print("Invalid input!")


class Patients:
    def __init__(self, file_path):
        self.df = pd.read_excel(file_path)

    def generate_next_id(self):
        if len(self.df) == 0:
            return 1
        else:
            return self.df['Patient ID'].max() + 1

    def patient_data(self):
        ID = self.generate_next_id()
        name = input("Name: ")
        age = int(input("Age: "))
        sex = input("Sex: ")
        op_time = input("Operation Time: ")
        priority = input("Priority: ")
        admission_date = input("Admission Date: ")
        admission_type = input("Admission Type: ")

        data = {
            'Patient ID': [ID],
            'Patient Name': [name],
            'Age': [age],
            'Sex': [sex],
            'Operation Completion Time(hrs)': [op_time],
            'Priority': [priority],
            'Admission Date': [admission_date],
            'Admission Type': [admission_type]
        }

        return data

    def add_patients(self):
        i = 0
        rows = []
        while i < 100:
            data = self.patient_data()
            rows.append(data)
            prompt = int(input("Save [1]: Add Patient[2]: "))
            if prompt == 1:
                # Append all rows from store_rows to DataFrame
                for row in rows:
                    new_row = pd.DataFrame(row, index=[0])
                    self.df = self.df.append(new_row, ignore_index=True)

                # Save the updated DataFrame
                self.df.to_excel("Hospital ER.xlsx", index=False)
                print("Saved")
                break
            elif prompt == 2:
                continue
            i += 1


def main():
    prompt = int(input("[1] Add patient [2] Create Schedule: "))

    if prompt == 1:
        patients = Patients("Hospital ER.xlsx")
        patients.add_patients()
    elif prompt == 2:
        scheduler = Scheduler("Hospital ER.xlsx")
        scheduler.user_interface()
    else:
        print("Invalid input")


if __name__ == "__main__":
    print("WELCOME TO THE ER DEPARTMENT")
    main()
