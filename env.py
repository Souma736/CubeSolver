"""
@author:majiabo
@e-mail:majiabo@hust.edu.cn

此文件用来模拟魔方。
"""
import tkinter as tk
import numpy as np
from random import shuffle
def construct_cube(random = False):
    """
    创建魔方的数据结构，使用正方体魔方，即共有六面。
    用含有六个键的字典表示一个魔方，每个键值对表示一面。
    采用one-hot 编码：
                [1,0,0,0,0,0] ,yellow
                [0,1,0,0,0,0] ,white
                [0,0,1,0,0,0] ,green
                [0,0,0,1,0,0] ,blue
                [0,0,0,0,1,0] ,orange
                [0,0,0,0,0,1] ,red
    每一面是一个[3,3,6]的numpyarra
    Note!!!!
        1.无论如何变幻，对应面中间的颜色对应不变
        2.每种颜色有order*2个,若是三阶魔方，即有九个
    实现：
        ##以下指中间色块
        让黄色与白色对应，黄色为forward，白色为backward
        让绿色与蓝色对应，绿色为left，蓝色为right
        让橙色与红色对应，橙色为up，红色为down
    """

    cube = np.zeros([6,3,3,6])
    color_bar = np.eye(6)
    
    if random:
        all_squres = [color_bar[j,:] for j in range(6) for i in range(8)]   #得到所有非中间色块
        shuffle(all_squres)     #打乱列表

        # 0-->forward, 1-->backward, 2--->left,
        # 3-->right,   4-->up,       5--->down,

        #随机初始化cube
        counter = 0
        for s in range(6):
            for i in range(3):
                for j in range(3):
                    if i!=1 or j!=1:
                        cube[s,i,j,:] = all_squres[counter]
                        counter += 1
            cube[s,1,1,:] = color_bar[s,:]
    else:
        for s in range(6):
            for i in range(3):
                for j in range(3):
                    cube[s,i,j,:] = color_bar[s,:]
    return cube

#cube = construct_cube()

####################
#魔方旋转函数
####################
def Forward(cube,clockwise):
    """
    转动正面的魔方块，
    cube:需要转动的魔方
    若clockwise = True,则顺时针转动
    若clockwise = Flase,则逆时针转动
    """
    
    # 得到所要移动面的所有数据。
    #  4
    # 2031 >> 0是目标
    #  5
    scramble_cubelets = {}

    scramble_cubelets['L'] = cube[2,:,2,:].copy()
    scramble_cubelets['R'] = cube[3,:,0,:].copy()
    scramble_cubelets['U'] = cube[4,2,:,:].copy()
    scramble_cubelets['D'] = cube[5,0,:,:].copy()
    scramble_cubelets['LF'] = cube[0,:,0,:].copy()
    scramble_cubelets['RF'] = cube[0,:,2,:].copy()
    scramble_cubelets['UF'] = cube[0,0,:,:].copy()
    scramble_cubelets['DF'] = cube[0,2,:,:].copy()
    # 逆时针
    if not clockwise:
        cube[2,:,2,:] = scramble_cubelets['U']
        cube[5,0,:,:] = scramble_cubelets['L']
        cube[3,:,0,:] = scramble_cubelets['D']
        cube[4,2,:,:] = scramble_cubelets['R']
        cube[0,:,0,:] = scramble_cubelets['UF']
        cube[0,2,:,:] = scramble_cubelets['LF']
        cube[0,:,2,:] = scramble_cubelets['DF']
        cube[0,0,:,:] = scramble_cubelets['RF']
    else:
        cube[2,:,2,:] = scramble_cubelets['D']
        cube[5,0,:,:] = scramble_cubelets['R']
        cube[3,:,0,:] = scramble_cubelets['U']
        cube[4,2,:,:] = scramble_cubelets['L']
        cube[0,:,0,:] = scramble_cubelets['DF']
        cube[0,2,:,:] = scramble_cubelets['RF']
        cube[0,:,2,:] = scramble_cubelets['UF']
        cube[0,0,:,:] = scramble_cubelets['LF']
    return cube
    
def Backward(cube,clockwise):
    """
    转背面，道理同上
     O
    OOO*        --->中间是Forward,背面是最后一个Backward
     O
    """
    scramble_cubelets = {}

    scramble_cubelets['L'] = cube[3,:,2,:].copy()
    scramble_cubelets['R'] = cube[2,:,0,:].copy()
    scramble_cubelets['U'] = cube[4,0,:,:].copy()
    scramble_cubelets['D'] = cube[5,2,:,:].copy()
    scramble_cubelets['LB'] = cube[1,:,0,:].copy()
    scramble_cubelets['RB'] = cube[1,:,2,:].copy()
    scramble_cubelets['UB'] = cube[1,0,:,:].copy()
    scramble_cubelets['DB'] = cube[1,2,:,:].copy()
    if clockwise:
        cube[3,:,2,:] = scramble_cubelets['D']
        cube[5,2,:,:] = scramble_cubelets['R']
        cube[2,:,0,:] = scramble_cubelets['U']
        cube[4,0,:,:] = scramble_cubelets['L']
        cube[1,:,0,:] = scramble_cubelets['DB']
        cube[1,2,:,:] = scramble_cubelets['RB']
        cube[1,:,2,:] = scramble_cubelets['UB']
        cube[1,0,:,:] = scramble_cubelets['LB']
    else:
        cube[3,:,2,:] = scramble_cubelets['U']
        cube[5,2,:,:] = scramble_cubelets['L']
        cube[2,:,0,:] = scramble_cubelets['D']
        cube[4,0,:,:] = scramble_cubelets['R']
        cube[1,:,0,:] = scramble_cubelets['UB']
        cube[1,2,:,:] = scramble_cubelets['LB']
        cube[1,:,2,:] = scramble_cubelets['DB']
        cube[1,0,:,:] = scramble_cubelets['RB']
    return cube

def Left(cube,clockwise):
    """
    旋转左面
     O
    *OOO        >>> * 旋转面
     O
    """
    scramble_cubelets = {}

    scramble_cubelets['L'] = cube[1,:,2,:].copy()
    scramble_cubelets['R'] = cube[0,:,0,:].copy()
    scramble_cubelets['U'] = cube[4,:,0,:].copy()
    scramble_cubelets['D'] = cube[5,:,0,:].copy()
    scramble_cubelets['LL'] = cube[2,:,0,:].copy()
    scramble_cubelets['RL'] = cube[2,:,2,:].copy()
    scramble_cubelets['UL'] = cube[2,0,:,:].copy()
    scramble_cubelets['DL'] = cube[2,2,:,:].copy()
    if clockwise:
        cube[1,:,2,:] = scramble_cubelets['D']
        cube[5,:,0,:] = scramble_cubelets['R']
        cube[0,:,0,:] = scramble_cubelets['U']
        cube[4,:,0,:] = scramble_cubelets['L']
        cube[2,:,0,:] = scramble_cubelets['DL']
        cube[2,2,:,:] = scramble_cubelets['RL']
        cube[2,:,2,:] = scramble_cubelets['UL']
        cube[2,0,:,:] = scramble_cubelets['LL']
    else:
        cube[1,:,2,:] = scramble_cubelets['U']
        cube[5,:,0,:] = scramble_cubelets['L']
        cube[0,:,0,:] = scramble_cubelets['D']
        cube[4,:,0,:] = scramble_cubelets['R']
        cube[2,:,0,:] = scramble_cubelets['UL']
        cube[2,2,:,:] = scramble_cubelets['LL']
        cube[2,:,2,:] = scramble_cubelets['DL']
        cube[2,0,:,:] = scramble_cubelets['RL']
    return cube

def Right(cube,clockwise):
    """
    旋转右边方块
     4
    2031        >>> 目标是3
     5
    """
    scramble_cubelets = {}

    scramble_cubelets['L'] = cube[0,:,2,:].copy() 
    scramble_cubelets['R'] = cube[1,:,0,:].copy()
    scramble_cubelets['U'] = cube[4,:,2,:].copy()
    scramble_cubelets['D'] = cube[5,:,2,:].copy()
    scramble_cubelets['LR'] = cube[3,:,0,:].copy()
    scramble_cubelets['RR'] = cube[3,:,2,:].copy()
    scramble_cubelets['UR'] = cube[3,0,:,:].copy()
    scramble_cubelets['DR'] = cube[3,2,:,:].copy()
    if clockwise:
        cube[0,:,2,:] = scramble_cubelets['D']
        cube[5,:,2,:] = scramble_cubelets['R']
        cube[1,:,0,:] = scramble_cubelets['U']
        cube[4,:,2,:] = scramble_cubelets['L']
        cube[3,:,0,:] = scramble_cubelets['DR']
        cube[3,2,:,:] = scramble_cubelets['RR']
        cube[3,:,2,:] = scramble_cubelets['UR']
        cube[3,0,:,:] = scramble_cubelets['LR']
    else:
        cube[0,:,2,:] = scramble_cubelets['U']
        cube[5,:,2,:] = scramble_cubelets['L']
        cube[1,:,0,:] = scramble_cubelets['D']
        cube[4,:,2,:] = scramble_cubelets['R']
        cube[3,:,0,:] = scramble_cubelets['UR']
        cube[3,2,:,:] = scramble_cubelets['LR']
        cube[3,:,2,:] = scramble_cubelets['DR']
        cube[3,0,:,:] = scramble_cubelets['RR']
    return cube

def Up(cube,clockwise):
    """
    转动上方
     4
    2031        >>> 4 为目标
     5
    """
    scramble_cubelets = {}

    scramble_cubelets['L'] = cube[2,0,:,:].copy() 
    scramble_cubelets['R'] = cube[3,0,:,:].copy()
    scramble_cubelets['U'] = cube[1,0,:,:].copy()
    scramble_cubelets['D'] = cube[0,0,:,:].copy()
    scramble_cubelets['LU'] = cube[4,:,0,:].copy()
    scramble_cubelets['RU'] = cube[4,:,2,:].copy()
    scramble_cubelets['UU'] = cube[4,0,:,:].copy()
    scramble_cubelets['DU'] = cube[4,2,:,:].copy()
    if clockwise:
        cube[2,0,:,:] = scramble_cubelets['D']
        cube[0,0,:,:] = scramble_cubelets['R']
        cube[3,0,:,:] = scramble_cubelets['U']
        cube[1,0,:,:] = scramble_cubelets['L']
        cube[4,:,0,:] = scramble_cubelets['DU']
        cube[4,2,:,:] = scramble_cubelets['RU']
        cube[4,:,2,:] = scramble_cubelets['UU']
        cube[4,0,:,:] = scramble_cubelets['LU']
    else:
        cube[2,0,:,:] = scramble_cubelets['U']
        cube[0,0,:,:] = scramble_cubelets['L']
        cube[3,0,:,:] = scramble_cubelets['D']
        cube[1,0,:,:] = scramble_cubelets['R']
        cube[4,:,0,:] = scramble_cubelets['UU']
        cube[4,2,:,:] = scramble_cubelets['LU']
        cube[4,:,2,:] = scramble_cubelets['DU']
        cube[4,0,:,:] = scramble_cubelets['RU']
    return cube

def Down(cube,clockwise):
    """
    旋转下面的方块
     4
    2031        >> 5 目标
     5
    """
    scramble_cubelets = {}

    scramble_cubelets['L'] = cube[2,2,:,:].copy() 
    scramble_cubelets['R'] = cube[3,2,:,:].copy()
    scramble_cubelets['U'] = cube[0,2,:,:].copy()
    scramble_cubelets['D'] = cube[1,2,:,:].copy()
    scramble_cubelets['LD'] = cube[5,:,0,:].copy()
    scramble_cubelets['RD'] = cube[5,:,2,:].copy()
    scramble_cubelets['UD'] = cube[5,0,:,:].copy()
    scramble_cubelets['DD'] = cube[5,2,:,:].copy()
    if clockwise:        
        cube[2,2,:,:] = scramble_cubelets['D']
        cube[1,2,:,:] = scramble_cubelets['R']
        cube[3,2,:,:] = scramble_cubelets['U']
        cube[0,2,:,:] = scramble_cubelets['L']
        cube[5,:,0,:] = scramble_cubelets['DD']
        cube[5,2,:,:] = scramble_cubelets['RD']
        cube[5,:,2,:] = scramble_cubelets['UD']
        cube[5,0,:,:] = scramble_cubelets['LD']
    else:
        cube[2,2,:,:] = scramble_cubelets['U']
        cube[1,2,:,:] = scramble_cubelets['L']
        cube[3,2,:,:] = scramble_cubelets['D']
        cube[0,2,:,:] = scramble_cubelets['R']
        cube[5,:,0,:] = scramble_cubelets['UD']
        cube[5,2,:,:] = scramble_cubelets['LD']
        cube[5,:,2,:] = scramble_cubelets['DD']
        cube[5,0,:,:] = scramble_cubelets['RD']
    return cube

def Random_scramble(N,cube):
    """
    对当前状态的魔方随机旋转N次
    """
    action_ids = np.random.randint(0,high=6,size=N)
    direction_ids =np.random.randint(0,high =2, size = N)
    action_func = [Forward,Backward,Left,Right,Up,Down]
    direction = [True,False]
    for ac_id,direc_id in zip(action_ids,direction_ids):
        cube = action_func[ac_id](cube,direction[direc_id])
        print(ac_id,direc_id)
    return cube
#################
#GUI 以及颜色定义
################
Color_bar = {0:'yellow',1:'white',2:'green',
             3:'blue',4:'orange',5:'red'}
cubelet_width = 80
col_number = 12
row_number = 9
surface_order = [4,2,0,3,1,5]   # 魔方块在平面图形上的表示
#坐标修正
surface_coors = [(0,3*cubelet_width),(3*cubelet_width,0),
                 (3*cubelet_width,3*cubelet_width),(3*cubelet_width,6*cubelet_width),
                 (3*cubelet_width,9*cubelet_width),(6*cubelet_width,3*cubelet_width)]

def Draw_color(board,surface,data):
    """
    为某一面绘制图形，返回board
    surface 为网格左上角坐标(row,col)
    """
    global Color_bar,cubelet_width
    (row,col) = surface
    for i in range(3):
        for j in range(3):
            color = Color_bar[np.argmax(data[i,j,:])]
            board.create_rectangle(j*cubelet_width+col,i*cubelet_width+row,
                                    (j+1)*cubelet_width+col,(i+1)*cubelet_width+row,fill = color,width = 10)

def GUI_init(cube):

    global col_number,row_number,surface_coors,surface_order,cubelet_width
    GUI = tk.Tk()
    GUI.title("CubeSolver_V1.0")
    board = tk.Canvas(GUI,width=col_number*cubelet_width,height = row_number*cubelet_width)
    for index,s in enumerate(surface_order):
        data = cube[s,:,:,:]
        surface_refine = surface_coors[index]
        Draw_color(board,surface_refine,data)
    """
    for i in [3,4,5]:
        for j in [0,1,2]:
            color = Color_bar[np.argmax(cube[4,j,i-3,:])]
            board.create_rectangle(i*cubelet_width,j*cubelet_width,
                                    (i+1)*cubelet_width,(j+1)*cubelet_width,fill = color,width = 10)
    for i in range(12):
        for j in [3,4,5]:
            board.create_rectangle(i*cubelet_width,j*cubelet_width,
                                    (i+1)*cubelet_width,(j+1)*cubelet_width,fill ="",width = 10)
    for i in [3,4,5]:
        for j in [6,7,8]:
            color = Color_bar[np.argmax(cube[5,j-6,i-3,:])]
            board.create_rectangle(i*cubelet_width,j*cubelet_width,
                                    (i+1)*cubelet_width,(j+1)*cubelet_width,fill =color,width = 10)
    """
    board.pack()
    return [GUI,board]

def update_GUI(cube,board):
    for index,s in enumerate(surface_order):
        data = cube[s,:,:,:]
        surface_refine = surface_coors[index]
        Draw_color(board,surface_refine,data)
    
cube = construct_cube(random=False)
[GUI,board] = GUI_init(cube)
cube = Random_scramble(2,cube)
update_GUI(cube,board)
GUI.mainloop()
## 多次旋转有问题，