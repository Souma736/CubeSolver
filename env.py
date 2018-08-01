"""
@author:majiabo
@e-mail:majiabo@hust.edu.cn

此文件用来模拟魔方。
"""
import tkinter as tk
import numpy as np

###################
# 
###################

def construct_cube(order = 3):
    """
    创建魔方的数据结构，使用正方体魔方，即共有六面。
    用含有六个键的字典表示一个魔方，每个键值对表示一面。
    采用one-hot 编码：
                [1,0,0,0,0,0] ,white
                [0,1,0,0,0,0] ,blue
                [0,0,1,0,0,0] ,red
                [0,0,0,1,0,0] ,green
                [0,0,0,0,1,0] ,yellow
                [0,0,0,0,0,1] ,orange
    每一面是一个[3,3,6]的numpyarra
    Note!!!!
        1.无论如何变幻，对应面中间的颜色对应不变
        2.每种颜色有order*2个,若是三阶魔方，即有九个
    实现：
        ##以下指中间色块
        让黄色与白色对应，黄色为forward，白色为backward
        让绿色与蓝色对应，绿色为left，蓝色为right
    """
    color_bar = np.eye(6)
    Forward = np.array
     
