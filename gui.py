
import tkinter as tk
from tkinter.filedialog import askopenfilename
# from MMR import mmr
import codecs 
window = tk.Tk()
window.title('text summarization')
window.geometry('400x400')

'''
def openfile():
    filename = path
    try:
        with open(filename) as f:
            for each_line in f:
                t1.insert(INSERT,each_line)                
    except OSError as reason:
        print('文件不存在！\n请重新输入文件名'+str(reason)
'''

def selectPath():
	path_1= askopenfilename()
	print(path_1)
# 	path.set(path_1)
# #	f = open(path)
# 	filename = str(path)
	f=codecs.open(path_1)
	t1.insert(f)                

	
path = tk.StringVar()

# b1 = tk.Button(window, text='提取摘要', width=15,
#               height=2,command=mmr).grid(row=2, column=2, padx=10, pady=10)
#b1.pack()

b2 = tk.Button(window, text='选择新闻', width=15,
              height=2,command=selectPath).grid(row=1, column=2, padx=10, pady=10)
#b2.pack()

t1 = tk.Text(window, width=20,height=10).grid(row=1, column=1, padx=10, pady=10)
#t1.pack()

t2 = tk.Text(window, width=20, height=10).grid(row=2, column=1, padx=10, pady=10)
#t2.pack()



window.mainloop()
