import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv(r"d:/BITK9/Python/Chuong 3/diem.csv")

diem_tb = {
    "Toan": df["Toan"].mean(),
    "Ly": df["Ly"].mean(),
    "Hoa": df["Hoa"].mean(),
}

plt.bar(diem_tb.keys(), diem_tb.values())
plt.xlabel("Mon hoc")
plt.xlabel("Diem trung binh")

plt.title("Diem trung binh cac mon hoc")
plt.ylim(0, 10)

plt.show()
