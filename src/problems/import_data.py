#Script che mi serve per importare i dati contenuti nei csv files
import pandas as pd
import numpy as np
import os

def import_csv_files():
    t = pd.read_csv("problems/t.csv", header = None)
    t = t.to_numpy()
    x = pd.read_csv("problems/x.csv", header = None)
    x = x.to_numpy()
    u = pd.read_csv("problems/u.csv", header= None)
    u = u.to_numpy()
    du_dx = pd.read_csv("problems/du_dx.csv", header= None)
    du_dx = du_dx.to_numpy()
    du2_dx = pd.read_csv("problems/du2_dx.csv", header=None)
    du2_dx = du2_dx.to_numpy()
    du3_dx = pd.read_csv("problems/du3_dx.csv", header=None)
    du3_dx = du3_dx.to_numpy()
    u1 = pd.read_csv("problems/u1.csv", header=None)
    u1=u1.to_numpy()
    u2 = pd.read_csv("problems/u2.csv", header=None)
    u2 = u2.to_numpy()
    u3 = pd.read_csv("problems/u3.csv", header=None)
    u3 = u3.to_numpy()
    u4 = pd.read_csv("problems/u4.csv", header=None)
    u4 = u4.to_numpy()
    u5 = pd.read_csv("problems/u5.csv", header=None)
    u5 = u5.to_numpy()
    u6 = pd.read_csv("problems/u6.csv", header=None)
    u6 = u6.to_numpy()
    u7 = pd.read_csv("problems/u7.csv", header=None)
    u7 = u7.to_numpy()
    u8 = pd.read_csv("problems/u8.csv", header=None)
    u8 = u8.to_numpy()
    u9 = pd.read_csv("problems/u9.csv", header=None)
    u9 = u9.to_numpy()
    u10 = pd.read_csv("problems/u10.csv", header=None)
    u10 = u10.to_numpy()
    du_dt = pd.read_csv("problems/du_dt.csv", header=None)
    du_dt = du_dt.to_numpy()
    return [t,x,u,du_dx, du2_dx, du3_dx, u1, u2, u3, u4, u5, u6, u7, u8, u9, u10, du_dt]


def import_analytic_csv_files():
    t = pd.read_csv("problems/t.csv", header = None)
    t = t.to_numpy()
    x = pd.read_csv("problems/x.csv", header = None)
    x = x.to_numpy()
    u = pd.read_csv("problems/u_analy.csv", header= None)
    u = u.to_numpy()
    du_dx = pd.read_csv("problems/du_dx_analy.csv", header= None)
    du_dx = du_dx.to_numpy()
    du2_dx = pd.read_csv("problems/du2_dx_analy.csv", header=None)
    du2_dx = du2_dx.to_numpy()
    du3_dx = pd.read_csv("problems/du3_dx_analy.csv", header=None)
    du3_dx = du3_dx.to_numpy()
    u1 = pd.read_csv("problems/u1_analy.csv", header=None)
    u1=u1.to_numpy()
    u2 = pd.read_csv("problems/u2_analy.csv", header=None)
    u2 = u2.to_numpy()
    u3 = pd.read_csv("problems/u3_analy.csv", header=None)
    u3 = u3.to_numpy()
    u4 = pd.read_csv("problems/u4_analy.csv", header=None)
    u4 = u4.to_numpy()
    u5 = pd.read_csv("problems/u5_analy.csv", header=None)
    u5 = u5.to_numpy()
    u6 = pd.read_csv("problems/u6_analy.csv", header=None)
    u6 = u6.to_numpy()
    u7 = pd.read_csv("problems/u7_analy.csv", header=None)
    u7 = u7.to_numpy()
    u8 = pd.read_csv("problems/u8_analy.csv", header=None)
    u8 = u8.to_numpy()
    u9 = pd.read_csv("problems/u9_analy.csv", header=None)
    u9 = u9.to_numpy()
    u10 = pd.read_csv("problems/u10_analy.csv", header=None)
    u10 = u10.to_numpy()
    du_dt = pd.read_csv("problems/du_dt_analy.csv", header=None)
    du_dt = du_dt.to_numpy()
    return [t,x,u,du_dx, du2_dx, du3_dx, u1, u2, u3, u4, u5, u6, u7, u8, u9, u10, du_dt]



def import_csv_data(data_directory):
    files = os.listdir(data_directory)
    files.sort()
    data = []
    for file in files:
        print("file", file)
        d = pd.read_csv(data_directory + "/" + file, header=None)
        d = d.to_numpy()
        data.append(d)
    return data
