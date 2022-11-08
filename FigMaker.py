def maikingFig(x, y, xlim, ylim, asp, savePath, data_Path):
  import numpy as np
  import matplotlib.pyplot as plt
  import os
  
  plt.rcParams['font.family'] ='sans-serif' #使用するフォント
  plt.rcParams['xtick.direction'] = 'in'  #x軸の目盛線が内向き('in')か外向き('out')か双方向か('inout')
  plt.rcParams['ytick.direction'] = 'in'  #y軸の目盛線が内向き('in')か外向き('out')か双方向か('inout')
  plt.rcParams['xtick.major.width'] = 1.0 #x軸主目盛り線の線幅
  plt.rcParams['ytick.major.width'] = 1.0 #y軸主目盛り線の線幅
  plt.rcParams['font.size'] = 8 #フォントの大きさ
  plt.rcParams['axes.linewidth'] = 1.0  #軸の線幅edge linewidth。囲みの太さ
  #plt.xlim(0, xlim)
  #plt.ylim(0, ylim)
  if asp == 0:
    fig = plt.figure()
  else:
    fig = plt.figure(figsize=(3.14 *asp,3.14)) #図のサイズの設定, 図のサイズはインチで指定され、変数は(幅, 高さ)です。

  ax = fig.add_subplot(111)
  ax.plot(x, y)
  #label
  ax.set_xlabel('Sliding Time [sec]')
  ax.set_ylabel('Friction Coefficient')
  ax.set_xlim(0, xlim)
  ax.set_ylim(0, ylim)
  #plt.show()

  fileName = savePath + os.sep + os.path.splitext(os.path.basename(data_Path))[0] + ".png"
  fig.savefig(fileName, bbox_inches="tight", pad_inches=0.05)  # 画像を保存
  print("saved[" + fileName + "]")
  

  #ref https://qiita.com/qsnsr123/items/325d21621cfe9e553c17




import sys
import glob
import os
import tkinter as tk
import tkinter.filedialog
from tkinter import messagebox


#fileList取得
# ルートウィンドウ作成
root = tk.Tk()
# ルートウィンドウの非表示
root.withdraw()

target_Path = tkinter.filedialog.askdirectory(title="データの参照をフォルダを指定してください。", mustexist=True)
target_Path_csv = target_Path + os.sep + "*.csv"
target_Path_xlsx = target_Path + os.sep + "*.xlsx"
fileList_csv = glob.glob(target_Path_csv)
fileList_xlsx = glob.glob(target_Path_xlsx)
if (len(fileList_csv) != 0) and (len(fileList_xlsx) != 0):
  messagebox.showerror("error01", "選択したフォルダにデータがありません。システムを終了します。")
  sys.exit()
savePath = tkinter.filedialog.askdirectory(title="データの保存先を指定してください。", mustexist=True)
xlim = float(input("作成するグラフのx軸の最大値を入力してください。\n>>"))
ylim = float(input("作成するグラフのy軸の最大値を入力してください。\n>>"))
asp = float(input('アスペクト比を入力してください。\n論文用途であれば1, 指定なしの場合は0を入力してください。\n>>'))
type_macine = int(input('旧型なら0、新型なら1を入力してください。\n>>'))
if type_macine == 0:
  step = 20
else:
  step = 1


if len(fileList_csv) != 0:
  import csv
  for count_fL in range(len(fileList_csv)):     #count_fL = count_fileList
    print(str(count_fL+1) + "/" + str(len(fileList_csv)))

    DB_Outcome = []
    #DB取得
    data_Path = fileList_csv[count_fL]
    with open(data_Path, encoding="shift-jis") as f:
    #DB→計算用一次元配列に置き換え
      csvreader = csv.reader(f)
      DB = [row for row in csvreader] 
    SlidingTime = []
    FrictionCoefficient = []
    for i in range(len(DB)-step):
      SlidingTime.append(float(DB[i+step][0]))
      FrictionCoefficient.append(float(DB[i+step][2]))
    maikingFig(SlidingTime, FrictionCoefficient, xlim, ylim, asp, savePath, data_Path)

if len(fileList_xlsx) != 0:
  import pandas
  #Body
  for count_fL in range(len(fileList_xlsx)):     #count_fL = count_fileList
    print(str(count_fL+1) + "/" + str(len(fileList_xlsx)))

    #DB取得
    data_Path = fileList_xlsx[count_fL]
    DB = pandas.read_excel(data_Path, sheet_name = "Sheet1")

    #DB→計算用一次元配列に置き換え
    SlidingTime = []
    FrictionCoefficient = []
    for i in range(len(DB)-step):
      SlidingTime.append(DB.values[i+step][0])
      FrictionCoefficient.append(DB.values[i+step][2])
    maikingFig(SlidingTime, FrictionCoefficient, xlim, ylim, asp, savePath, data_Path)
print("All Process is Done\nstop Running\nSee you my Boss")

#error01:選択したフォルダにデータがありません。

#ver1.0.0
#基本的なアルゴリズムの作成
#ver1.1.0
#新型ボールオンディスクに対応