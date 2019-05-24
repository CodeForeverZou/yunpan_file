#!/usr/bin/env python3
# -*- coding:utf-8 -*-
 
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter.ttk import *
import sqlite3
 
def select_db_file():
    db_file = askopenfilename(title="请选择BaiduYunCacheFileV0.db文件",filetypes=[('db', '*.db')])
    db.set(db_file)
 
def select_save_file():
    save_file = asksaveasfilename(filetypes=[('文件', '*.txt')])
    f.set(save_file+".txt")
 
def write_file2(file_dict,f,item,gap=""):
    if item=="/":
        f.write("━" + "/" + "\n")
        for i in file_dict["/"]:
            j=i['name']
            #加个file_size
            f.write("┣" + "━" + j + ' ' + str(i['size']) + "\n")
            j = item + j + "/"
            if j in file_dict:
                write_file2(file_dict,f,j, gap="┣━")
    else:
        gap = "┃  " + gap
        for i in file_dict[item]:
            #加个size
            j=i['name']
            f.write(gap + j + ' ' + str(i['size']) + "\n")
            j = item + j + "/"
            if j in file_dict:
                  write_file2(file_dict,f,j,gap)
                  
                  
def select_bigf(file_dict,f,item,gap=""):
    #筛选大文件
    if item=="/":
        f.write("━" + "/" + "\n")
        for i in file_dict["/"]:
            j=i['name']
            #加个file_size
            if i['size']>1073741824 or i['size']==0:               
                f.write("┣" + "━" + j + ' ' + str(i['size']) + '------'+ item +"\n")
            j = item + j + "/"
            if j in file_dict:
                select_bigf(file_dict,f,j, gap="┣━")
    else:
        gap = "┃  " + gap
        for i in file_dict[item]:
            #加个size
            j=i['name']
            if i['size']>1073741824 :
                f.write(gap + j + ' ' + str(i['size']) + '------'+ item +"\n")
            j = item + j + "/"
            if j in file_dict:
                  select_bigf(file_dict,f,j,gap)

def init():
    #创建一个复杂的数据结构：file_dict
    #其本质为字典，键为路径，值为列表（列表内容是字典，键为文件名，值为文件大小）
    file_dict = {}
    conn = sqlite3.connect(db.get())
    cursor = conn.cursor()
    cursor.execute("select * from cache_file")
    while True:
        value = cursor.fetchone()
        if not value:
            break
        path = value[2]
        name = value[3]
        size = value[4]
        isdir = value[6]
        dict={'name':"",'size':''}
        dict['name']=name
        dict['size']=size
        
        if path not in file_dict:
            file_dict[path] = []
            file_dict[path].append(dict)
        else:
            file_dict[path].append(dict)

    return file_dict

def create_baiduyun_filelist():
    file_dict = {}
    file_dict = init()          
    with open(f.get(),"w",encoding='utf-8') as fp:
        write_file2(file_dict,fp,"/")

def create_bbaiduyun_filelist():
    file_dict = {}
    file_dict = init()          
    with open(f.get(),"w",encoding='utf-8') as fp:
        select_bigf(file_dict,fp,"/")
 
root = Tk()
root.title('百度云文件列表生成工具')
#创建“选择DB文件”按钮、文本框
db_select = Button(root, text=' 选择DB文件 ',command=select_db_file)
db_select.grid(row=1,column=1,sticky=W,padx=(2,0),pady=(2,0))
db = StringVar()
db_path = Entry(root,width=80,textvariable = db)
db_path['state'] = 'readonly'
db_path.grid(row=1,column=2,padx=3,pady=3,sticky=W+E)
#创建“选择保存位置”按钮、文本框
save_path = Button(root, text='选择保存地址',command=select_save_file)
save_path.grid(row=2,column=1,sticky=W,padx=(2,0),pady=(2,0))
f = StringVar()
file_path = Entry(root,width=80,textvariable = f)
file_path['state'] = 'readonly'
file_path.grid(row=2, column=2,padx=3,pady=3,sticky=W+E)
#创建事件按钮
create_btn = Button(root, text='生成文件列表',command=create_baiduyun_filelist)
create_btn.grid(row=3,column=1,columnspan=2,pady=(0,2))
create_btn = Button(root, text='生成大文件列表',command=create_bbaiduyun_filelist)
create_btn.grid(row=4,column=1,columnspan=2,pady=(0,2))

root.columnconfigure(2, weight=1)
root.mainloop()
