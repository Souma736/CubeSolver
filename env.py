"""
@author:majiabo
@e-mail:majiabo@hust.edu.cn

此文件用来模拟魔方。
"""
import tkinter as tk
import numpy as np
from random import shuffle
import time



#################
#GUI_env 以及颜色定义
################
class GUI_env():
    def __init__(self):
        ## config 
        self.Color_bar = {0:'yellow',1:'white',2:'green',
                    3:'blue',4:'orange',5:'red'}
        self.cubelet_width = 80
        self.col_number = 12
        self.row_number = 9
        self.surface_order = [4,2,0,3,1,5]   # 魔方块在平面图形上的表示
        #坐标修正
        self.surface_coors = [(0,3*self.cubelet_width),(3*self.cubelet_width,0),
                        (3*self.cubelet_width,3*self.cubelet_width),(3*self.cubelet_width,6*self.cubelet_width),
                        (3*self.cubelet_width,9*self.cubelet_width),(6*self.cubelet_width,3*self.cubelet_width)]
        self.GUI = tk.Tk()
        self.GUI.title("CubeSolver_V1.0")
        self.board = tk.Canvas(self.GUI,width=self.col_number*self.cubelet_width,height = self.row_number*self.cubelet_width)
        self.cube = self.construct_cube(random=False)
        #初始化魔方
        self.GUI_init()
    def Draw_color(self,surface,data):
        """
        为某一面绘制图形，返回board
        surface 为网格左上角坐标(row,col)
        """
        (row,col) = surface
        for i in range(3):
            for j in range(3):
                color = self.Color_bar[np.argmax(data[i,j,:])]
                self.board.create_rectangle(j*self.cubelet_width+col,i*self.cubelet_width+row,
                                        (j+1)*self.cubelet_width+col,(i+1)*self.cubelet_width+row,fill = color,width = 10)

    def construct_cube(self,random):
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
    def GUI_init(self,radnom = False):
        """
        初始化魔方
        """
        cube = self.construct_cube(random=radnom)
        for index,s in enumerate(self.surface_order):
            data = self.cube[s,:,:,:]
            surface_refine = self.surface_coors[index]
            self.Draw_color(surface_refine,data)
        self.board.pack()
        return cube

    def click_scramble(self,scramble_func,dire):
        tk.Button(self.GUI,text = 'Down_CK',command = lambda:scramble_func(self.cube,dire)).pack()
        self.update_GUI()
    def update_GUI(self):
        """
        移动后用来重新绘制图形
        """
        for index,s in enumerate(self.surface_order):
            data = self.cube[s,:,:,:]
            surface_refine = self.surface_coors[index]
            self.Draw_color(surface_refine,data)
    def show(self):
        self.GUI.mainloop()


class Agent(GUI_env):
    """
    所有均采用顺时针
    垃圾数据结构，，，，
    """
    def Forward(self,clockwise):
        """
        转动正面的魔方块，
        cube:需要转动的魔方
        若clockwise = True,则顺时针转动
        若clockwise = Flase,则逆时针转动
        """
        # checked --------> 
        # 得到所要移动面的所有数据。
        #  4
        # 2031 >> 0是目标
        #  5
        scramble_cubelets = {}
        rc = [2,1,0]
        scramble_cubelets['L'] = self.cube[2,:,2,:].copy()
        scramble_cubelets['R'] = self.cube[3,:,0,:].copy()
        scramble_cubelets['U'] = self.cube[4,2,:,:].copy()
        scramble_cubelets['D'] = self.cube[5,0,:,:].copy()
        scramble_cubelets['LF'] = self.cube[0,:,0,:].copy()
        scramble_cubelets['RF'] = self.cube[0,:,2,:].copy()
        scramble_cubelets['UF'] = self.cube[0,0,:,:].copy()
        scramble_cubelets['DF'] = self.cube[0,2,:,:].copy()
        if clockwise:
            self.cube[2,:,2,:] = scramble_cubelets['D']
            self.cube[5,0,:,:] = scramble_cubelets['R'][rc,:]
            self.cube[3,:,0,:] = scramble_cubelets['U']
            self.cube[4,2,:,:] = scramble_cubelets['L'][rc,:]
            self.cube[0,:,0,:] = scramble_cubelets['DF']
            self.cube[0,2,:,:] = scramble_cubelets['RF'][rc,:]
            self.cube[0,:,2,:] = scramble_cubelets['UF']
            self.cube[0,0,:,:] = scramble_cubelets['LF'][rc,:]
        else:
            self.cube[2,:,2,:] = scramble_cubelets['U'][rc,:]
            self.cube[5,0,:,:] = scramble_cubelets['L']
            self.cube[3,:,0,:] = scramble_cubelets['D'][rc,:]
            self.cube[4,2,:,:] = scramble_cubelets['R']
            self.cube[0,:,0,:] = scramble_cubelets['UF'][rc,:]
            self.cube[0,2,:,:] = scramble_cubelets['LF']
            self.cube[0,:,2,:] = scramble_cubelets['DF'][rc,:]
            self.cube[0,0,:,:] = scramble_cubelets['RF']
    def Backward(self,clockwise):
        """
        转背面，道理同上
         4
        2031        --->1 目标
         5
        """
        scramble_cubelets = {}
        rc = [2,1,0]
        scramble_cubelets['L'] = self.cube[3,:,2,:].copy()
        scramble_cubelets['R'] = self.cube[2,:,0,:].copy()
        scramble_cubelets['U'] = self.cube[4,0,rc,:].copy() #反序，纸巾方块演示
        scramble_cubelets['D'] = self.cube[5,2,rc,:].copy()
        scramble_cubelets['LB'] = self.cube[1,:,0,:].copy()
        scramble_cubelets['RB'] = self.cube[1,:,2,:].copy()
        scramble_cubelets['UB'] = self.cube[1,0,:,:].copy()
        scramble_cubelets['DB'] = self.cube[1,2,:,:].copy()
        if clockwise:
            self.cube[3,:,2,:] = scramble_cubelets['D']
            self.cube[5,2,:,:] = scramble_cubelets['R'] #无需反序
            self.cube[2,:,0,:] = scramble_cubelets['U']
            self.cube[4,0,:,:] = scramble_cubelets['L']
            self.cube[1,:,0,:] = scramble_cubelets['DB']
            self.cube[1,2,:,:] = scramble_cubelets['RB'][rc,:]
            self.cube[1,:,2,:] = scramble_cubelets['UB']
            self.cube[1,0,:,:] = scramble_cubelets['LB'][rc,:]
        else:
            self.cube[3,:,2,:] = scramble_cubelets['U'][rc,:]
            self.cube[5,2,:,:] = scramble_cubelets['L'][rc,:]
            self.cube[2,:,0,:] = scramble_cubelets['D'][rc,:]
            self.cube[4,0,:,:] = scramble_cubelets['R'][rc,:]
            self.cube[1,:,0,:] = scramble_cubelets['UB'][rc,:]
            self.cube[1,2,:,:] = scramble_cubelets['LB']
            self.cube[1,:,2,:] = scramble_cubelets['DB'][rc,:]
            self.cube[1,0,:,:] = scramble_cubelets['RB']
        #checked ---->

    def Left(self,clockwise):
        """
        旋转左面
         4
        2031       >>> 2 旋转面
         5
        """
        scramble_cubelets = {}
        rc = [2,1,0]
        scramble_cubelets['L'] = self.cube[1,:,2,:].copy()
        scramble_cubelets['R'] = self.cube[0,:,0,:].copy()
        scramble_cubelets['U'] = self.cube[4,:,0,:].copy()
        scramble_cubelets['D'] = self.cube[5,rc,0,:].copy()
        scramble_cubelets['LL'] = self.cube[2,:,0,:].copy()
        scramble_cubelets['RL'] = self.cube[2,:,2,:].copy()
        scramble_cubelets['UL'] = self.cube[2,0,:,:].copy()
        scramble_cubelets['DL'] = self.cube[2,2,:,:].copy()
        if clockwise:
            self.cube[1,:,2,:] = scramble_cubelets['D']
            self.cube[5,:,0,:] = scramble_cubelets['R'] #无需反序
            self.cube[0,:,0,:] = scramble_cubelets['U']
            self.cube[4,:,0,:] = scramble_cubelets['L'][rc,:]
            self.cube[2,:,0,:] = scramble_cubelets['DL']
            self.cube[2,2,:,:] = scramble_cubelets['RL'][rc,:]
            self.cube[2,:,2,:] = scramble_cubelets['UL']
            self.cube[2,0,:,:] = scramble_cubelets['LL'][rc,:]
        else:
            self.cube[1,:,2,:] = scramble_cubelets['U'][rc,:]
            self.cube[5,:,0,:] = scramble_cubelets['L'][rc,:]
            self.cube[0,:,0,:] = scramble_cubelets['D'][rc,:]
            self.cube[4,:,0,:] = scramble_cubelets['R']
            self.cube[2,:,0,:] = scramble_cubelets['UL'][rc,:]
            self.cube[2,2,:,:] = scramble_cubelets['LL']
            self.cube[2,:,2,:] = scramble_cubelets['DL'][rc,:]
            self.cube[2,0,:,:] = scramble_cubelets['RL']
            #checked

    def Right(self,clockwise):
        """
        旋转右边方块
         4
        2031        >>> 目标是3
         5
        """
        scramble_cubelets = {}
        rc = [2,1,0]

        scramble_cubelets['L'] = self.cube[0,:,2,:].copy() 
        scramble_cubelets['R'] = self.cube[1,:,0,:].copy()
        scramble_cubelets['U'] = self.cube[4,rc,2,:].copy()
        scramble_cubelets['D'] = self.cube[5,:,2,:].copy()
        scramble_cubelets['LR'] = self.cube[3,:,0,:].copy()
        scramble_cubelets['RR'] = self.cube[3,:,2,:].copy()
        scramble_cubelets['UR'] = self.cube[3,0,:,:].copy()
        scramble_cubelets['DR'] = self.cube[3,2,:,:].copy()
        if clockwise:
            self.cube[0,:,2,:] = scramble_cubelets['D']
            self.cube[5,:,2,:] = scramble_cubelets['R'][rc,:]
            self.cube[1,:,0,:] = scramble_cubelets['U']
            self.cube[4,:,2,:] = scramble_cubelets['L']
            self.cube[3,:,0,:] = scramble_cubelets['DR']
            self.cube[3,2,:,:] = scramble_cubelets['RR'][rc,:]
            self.cube[3,:,2,:] = scramble_cubelets['UR']
            self.cube[3,0,:,:] = scramble_cubelets['LR'][rc,:]
        else:
            self.cube[0,:,2,:] = scramble_cubelets['U'][rc,:]
            self.cube[5,:,2,:] = scramble_cubelets['L']
            self.cube[1,:,0,:] = scramble_cubelets['D'][rc,:]
            self.cube[4,:,2,:] = scramble_cubelets['R'][rc,:]
            self.cube[3,:,0,:] = scramble_cubelets['UR'][rc,:]
            self.cube[3,2,:,:] = scramble_cubelets['LR']
            self.cube[3,:,2,:] = scramble_cubelets['DR'][rc,:]
            self.cube[3,0,:,:] = scramble_cubelets['RR']
            #checked --->
    def Up(self,clockwise):
        """
        转动上方
         4
        2031        >>> 4 为目标
         5
        """
        scramble_cubelets = {}
        rc = [2,1,0]
        scramble_cubelets['L'] = self.cube[2,0,:,:].copy() 
        scramble_cubelets['R'] = self.cube[3,0,rc,:].copy()
        scramble_cubelets['U'] = self.cube[1,0,rc,:].copy()
        scramble_cubelets['D'] = self.cube[0,0,:,:].copy()
        scramble_cubelets['LU'] = self.cube[4,:,0,:].copy()
        scramble_cubelets['RU'] = self.cube[4,:,2,:].copy()
        scramble_cubelets['UU'] = self.cube[4,0,:,:].copy()
        scramble_cubelets['DU'] = self.cube[4,2,:,:].copy()
        if clockwise:
            self.cube[2,0,:,:] = scramble_cubelets['D']
            self.cube[0,0,:,:] = scramble_cubelets['R'][rc,:]
            self.cube[3,0,:,:] = scramble_cubelets['U'][rc,:]
            self.cube[1,0,:,:] = scramble_cubelets['L']
            self.cube[4,:,0,:] = scramble_cubelets['DU']
            self.cube[4,2,:,:] = scramble_cubelets['RU'][rc,:]
            self.cube[4,:,2,:] = scramble_cubelets['UU']
            self.cube[4,0,:,:] = scramble_cubelets['LU'][rc,:]
        else:
            self.cube[2,0,:,:] = scramble_cubelets['U'][rc,:]
            self.cube[0,0,:,:] = scramble_cubelets['L']
            self.cube[3,0,:,:] = scramble_cubelets['D']
            self.cube[1,0,:,:] = scramble_cubelets['R'][rc,:]
            self.cube[4,:,0,:] = scramble_cubelets['UU'][rc,:]
            self.cube[4,2,:,:] = scramble_cubelets['LU']
            self.cube[4,:,2,:] = scramble_cubelets['DU'][rc,:]
            self.cube[4,0,:,:] = scramble_cubelets['RU']
            #checked --->
    def Down(self,clockwise):
        """
        旋转下面的方块
         4
        2031        >> 5 目标
         5
        """
        scramble_cubelets = {}
        rc = [2,1,0]
        scramble_cubelets['L'] = self.cube[2,2,rc,:].copy() 
        scramble_cubelets['R'] = self.cube[3,2,:,:].copy()
        scramble_cubelets['U'] = self.cube[0,2,:,:].copy()
        scramble_cubelets['D'] = self.cube[1,2,rc,:].copy()
        scramble_cubelets['LD'] = self.cube[5,:,0,:].copy()
        scramble_cubelets['RD'] = self.cube[5,:,2,:].copy()
        scramble_cubelets['UD'] = self.cube[5,0,:,:].copy()
        scramble_cubelets['DD'] = self.cube[5,2,:,:].copy()
        if clockwise:        
            self.cube[2,2,:,:] = scramble_cubelets['D'][rc,:]
            self.cube[1,2,:,:] = scramble_cubelets['R']
            self.cube[3,2,:,:] = scramble_cubelets['U']
            self.cube[0,2,:,:] = scramble_cubelets['L'][rc,:]
            self.cube[5,:,0,:] = scramble_cubelets['DD']
            self.cube[5,2,:,:] = scramble_cubelets['RD'][rc,:]
            self.cube[5,:,2,:] = scramble_cubelets['UD']
            self.cube[5,0,:,:] = scramble_cubelets['LD'][rc,:]
        else:
            self.cube[2,2,:,:] = scramble_cubelets['U']
            self.cube[1,2,:,:] = scramble_cubelets['L'][rc,:]
            self.cube[3,2,:,:] = scramble_cubelets['D'][rc,:]
            self.cube[0,2,:,:] = scramble_cubelets['R']
            self.cube[5,:,0,:] = scramble_cubelets['UD'][rc,:]
            self.cube[5,2,:,:] = scramble_cubelets['LD']
            self.cube[5,:,2,:] = scramble_cubelets['DD'][rc,:]
            self.cube[5,0,:,:] = scramble_cubelets['RD']

    def Random_scramble(self,N):
        """
        对当前状态的魔方随机旋转N次
        """
        action_ids = np.random.randint(0,high=6,size=N)
        direction_ids =np.random.randint(0,high =2, size = N)
        action_func = [self.Forward,self.Backward,self.Left,self.Right,self.Up,self.Down]
        direction = [True,False]
        for ac_id,direc_id in zip(action_ids,direction_ids):
            action_func[ac_id](direction[direc_id])
            print(ac_id,direc_id)

agent = Agent()
agent.Random_scramble(120)
agent.update_GUI()
agent.show()