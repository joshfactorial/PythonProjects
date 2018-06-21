import pandas as pd
import numpy as np


def read_table(filename):
    with open(filename, "r") as file:
        array = []
        flag = 0
        temp = ""
        for line in file:
            temp = line.rstrip('\n')
            if flag == 1:
                if temp != "#":
                    if temp[0] == "#":
                        array.append(temp.split()[1:])
                    else:
                        array.append(temp.split())
            if temp == "# VARIABLE ORDER":
                flag = 1

        array = pd.DataFrame(data=array[1:], columns=array[0], index=None)
        array_clean = array.loc[~(array['qcflag'].str.startswith("*"))]
        array_clean["year"] = array_clean["year"].astype(int)
        array_clean["month"] = array_clean["month"].astype(int)
        array_clean["day"] = array_clean["day"].astype(int)
        array_clean["hour"] = array_clean["hour"].astype(int)
        array_clean["minute"] = array_clean["minute"].astype(int)
        array_clean["second"] = array_clean["second"].astype(int)
        array_clean["value"] = array_clean["value"].astype(float)
        del array_clean["value_unc"]
        del array_clean["nvalue"]
        del array_clean["latitude"]
        del array_clean['longitude']
        del array_clean['altitude']
        del array_clean['elevation']
        del array_clean['intake_height']
        del array_clean['instrument']
        return array_clean

co2_alaska_clean = read_table("C:/Users/Joshua/Google Drive/_grad school/Summer 2018/Programming/co2_alaska.txt")
co2_alaska_clean = co2_alaska_clean.loc[co2_alaska_clean['year'] != 1973]
co2_hawaii_clean = read_table("C:/Users/Joshua/Google Drive/_grad school/Summer 2018/Programming/co2_hawaii.txt")


index = list(co2_alaska_clean.groupby("year").mean()['value'].round(2).index.values)
data = []
data.append(list(co2_alaska_clean.groupby("year").max()['value'].round(2)))
change_alaska = ["--"]
means_alaska = list(co2_alaska_clean.groupby("year").mean()['value'].round(2))
data.append(means_alaska)
for i in range(1, len(index)):
    change_alaska.append(round(((means_alaska[i]-means_alaska[i-1])/means_alaska[i-1])*100, 2))
data.append(change_alaska)
data.append(list(co2_hawaii_clean.groupby("year").max()['value'].round(2)))
change_hawaii = ["--"]
means_hawaii = list(co2_hawaii_clean.groupby("year").mean()['value'].round(2))
data.append(means_hawaii)
for i in range(1, len(index)):
    change_hawaii.append(round(((means_hawaii[i]-means_hawaii[i-1])/means_hawaii[i-1])*100, 2))
data.append(change_hawaii)
data = np.array(data)
data = data.T
df = pd.DataFrame(data, index=index, columns = pd.MultiIndex.from_product([["ALASKA", "HAWAII"], ["MAX_LEVEL", "MEAN_LEVEL", "%CHANGE"]]))
print(df.to_string())
with open("C:/Users/Joshua/Google Drive/_grad school/Summer 2018/Programming/output.txt", "w") as outfile:
    df.to_string(outfile)