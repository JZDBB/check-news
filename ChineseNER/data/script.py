# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 10:34:14 2018

@author: wtb
"""

file_src = "sk.test"
file_dst = "sk.test"

def read(file):
    with open(file, "r", encoding="utf8") as f:
        get = f.read()
        result = get.splitlines()
    return result

def process(result):
    result_new = []
    for line in result:
        line_new = line
#        temp = line.split(' ')[1].split('-')
        temp = line.split(' ')
        if len(temp) == 2:
            temp = temp[1].split('-')
            if len(temp) == 2:
                if temp[0] in ['M', 'E']:
                    line_temp = list(line)
                    line_temp[2] = 'I'
                    line_new = ''.join(line_temp)
                if temp[0] == 'S':
                    line_temp = list(line)
                    line_temp[2] = 'B'
                    line_new = ''.join(line_temp)
        result_new.append(line_new)
    return result_new
    
def write(file, result_new):
    with open(file, "w", encoding="utf8") as f:
        for line in result_new:
            f.write(line+'\n')
            
if __name__ == "__main__":
    result = read(file_src)
    result_new = process(result)
    write(file_dst, result_new)
