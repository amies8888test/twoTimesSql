#!/usr/bin/python
# -*- coding:utf8 -*-

import os
import re
import sys
import types

init_path = sys.argv[1]
all_file = []
regex_select = "select (.*) from (.*) where"
regex_update = "update (.*) set (.*) where"
regex_insert = "insert into (.*) \((.*)\) values"
table = "user"

def get_file_inpath(init_path):
    listfile=os.listdir(init_path)
    return listfile
#匹配字符串是否满足正则,source代表源字符串，regex代表匹配正则表达式,优先找正则表达式中的第num1个匹配值，如果为空，则返回第num2个返回值
def match(source,regex,num1,num2):
    patt = re.compile(regex,re.I)
    patt_arr = patt.findall(source)
    if(len(patt_arr) == 1):
        if(type(patt_arr[0]) == types.TupleType):
            if str(patt_arr[0][num1]) == "":
                return clean(str(patt_arr[0][num2]))
            else:
                return clean(str(patt_arr[0][num1]))
        return clean(str(patt_arr[0]))
    return
#匹配出查询字符串，返回表名
def match_select(source, regex, table_num, colmun_num):
    patt = re.compile(regex,re.I)
    patt_arr = patt.findall(source)
    if(len(patt_arr) == 1):
        if(type(patt_arr[0]) == types.TupleType):
            return clean(str(patt_arr[0][table_num]))
        return clean(str(patt_arr[0]))
    return
#匹配出update语句，返回表名和update的字段
def match_update(source, regex, table_num, column_num):
    rnt = {}
    patt = re.compile(regex,re.I)
    patt_arr = patt.findall(source)
    if(len(patt_arr) == 1):
        if(type(patt_arr[0]) == types.TupleType):
            table = clean(str(patt_arr[0][table_num]))
            rnt['table'] = table

            cols=[]
            columns = clean(str(patt_arr[0][column_num]))
            for column in columns.split(","):
                column = clean(column)
                cols.append(clean(column.split("=")[0].strip("`")))
            rnt['column'] = cols
    return rnt
#匹配insert语句，返回表名和insert的字段
def match_insert(source, regex, table_num, column_num=0):
    rnt={}
    patt = re.compile(regex,re.I)
    patt_arr = patt.findall(source)
    if(len(patt_arr) == 1):
        if(type(patt_arr[0]) == types.TupleType):
            table = clean(str(patt_arr[0][table_num]))
            rnt['table'] = table

            cols=[]
            columns = clean(str(patt_arr[0][column_num]))
            for column in columns.split(","):
                cols.append(clean(column.strip("`")))
            rnt['column'] = cols
    return rnt

#检测输出出来的变量是否进行了二次数据库操作
def twoSqlCheck(file_path,first_line,second_line,cols):
    rnt = False
    varia = second_line.split("=")[0].strip()
    file_object = open(file_path)
    temp_content = ""
    try:
        file_content = file_object.read()
        content_arr = file_content.split("function")
        if len(content_arr) == 1:
            temp_content = file_content
        else:
            for content in content_arr:
                if content.find(second_line) != -1:
                    temp_content = content
        file_object.close()
    except:
        file_object.close()
    file_object = open("temp.txt","w")
    file_object.write(temp_content)
    file_object.close()
    for line in open("temp.txt","r"):
        if line != second_line and line != first_line:
            if line.lower().find('delete ') != -1 or line.lower().find('update ') != -1 or line.lower().find('select ') != -1 or line.lower().find('insert ') != -1:
               
                for col in cols:
                    if (line.find(varia + "[" + col + "]") != -1 or line.find(varia + "['" + col + "']") != -1 or line.find(varia + "[\"" + col + "\"]") != -1) :
                        rnt = line
    # print rnt
    # exit()
    return rnt
#对匹配出来的表名进行清理
def clean(data):
    data = data.strip()
    data_arr = data.split("(")
    return data_arr[0].strip()
#读取一个文件夹下面所有的.php后缀的文件
def get_all_file(init_path):
    current_file = get_file_inpath(init_path)
    for one_file in current_file:
        fulldirfile = os.path.join(init_path,one_file)
        if one_file[0] == '.':
            pass
        if os.path.isdir(fulldirfile):
            get_all_file(fulldirfile)
        else:
            #如果不需要去掉后台地址，去掉fulldirfile.find("admin") == -1
            if fulldirfile.split(".")[-1] == "php" and fulldirfile.find("admin") == -1:
                all_file.append(fulldirfile)

get_all_file(init_path)
#逐行读取每个文件下面的每一行
match_num = 0
for first_file in all_file:
    for first_line in open(first_file,"r"):
        #这里的num需要根据正则表达式进行确定，这里是指定table的测试方式
        # if match(first_line, regex_in, 1, 4) == table:
        #     table = match(first_line, regex_in, 1, 4)
        #     for second_file in all_file:
        #         for second_line in open(second_file,"r"):
        #             if match(second_line, regex_out, 1, 4) == table:
        #                 if twoSqlCheck(second_file, second_line):
        #                     match_num = match_num + 1
        #                     handler = open('out_put.txt','a+')
        #                     handler.write("成功匹配到第" + str(match_num) + "条记录\n");
        #                     handler.write("INSERT或者UPDATE语句为"+ first_file +"：\n" + first_line +"\n")
        #                     handler.write("SELECT语句为"+ second_file +"：\n" + second_line +"\n")
        #                     handler.write("二次数据库操作为"+ second_file + ":\n" + twoSqlCheck(second_file, second_line) + "\n\n")
        #                     handler.close()
        #这里是不指定table，自动遍历所有table
        if match_update(first_line, regex_update, 0, 1):
            rnt = match_update(first_line, regex_update, 0, 1)
            table = rnt['table']
            cols = rnt['column']
            for second_file in all_file:
                for second_line in open(second_file,"r"):
                    if match_select(second_line, regex_select, 1, 1) == table:
                        if twoSqlCheck(second_file,first_file, second_line, cols):
                            match_num = match_num + 1
                            handler = open('out_put.txt','a+')
                            handler.write("成功匹配到第" + str(match_num) + "条记录\n");
                            handler.write("INSERT或者UPDATE语句为"+ first_file +"：\n" + first_line +"\n")
                            handler.write("SELECT语句为"+ second_file +"：\n" + second_line +"\n")
                            handler.write("二次数据库操作为"+ second_file + ":\n" + twoSqlCheck(second_file,first_file, second_line, cols) + "\n\n")
                            handler.close()
        elif match_insert(first_file, regex_insert, 0, 1):
            rnt = match_update(first_line, regex_insert, 0, 1)
            table = rnt['table']
            cols = rnt['column']
            for second_file in all_file:
                for second_line in open(second_file,"r"):
                    if match_select(second_line, regex_select, 1, 1) == table:
                        if twoSqlCheck(second_file, first_file, second_line, cols):
                            match_num = match_num + 1
                            handler = open('out_put.txt','a+')
                            handler.write("成功匹配到第" + str(match_num) + "条记录\n");
                            handler.write("INSERT或者UPDATE语句为"+ first_file +"：\n" + first_line +"\n")
                            handler.write("SELECT语句为"+ second_file +"：\n" + second_line +"\n")
                            handler.write("二次数据库操作为"+ second_file + ":\n" + twoSqlCheck(second_file,first_file, second_line, cols) + "\n\n")
                            handler.close()
        else:
            pass
