#====================================================
# Author: Terry
# Address: ShanghaiTech University, Shanghai, China
# Date: 2022.5.4
#====================================================

import numpy as np
import random
import math
from PIL import Image,ImageDraw,ImageFont


class CommentsTrack:
    def __init__(self,text_list,w=800,h=100,color=(0,255,0),font_size=40,speed=50):
        """
        构造方法
        @param text_list list 本泳道文字列表
        @param w,h int 泳道宽度和高度
        @param color tuple 泳道文字颜色
        @param font_size int 文字大小
        @param speed int 文字速度（像素/帧）
        """
        self.text_list = text_list
        self.w = w
        self.h = h
        self.color = color
        self.font_size = font_size
        self.speed = speed

    def text_list_str(self,blank_num):
        """
        将每段弹幕文字整合到一个泳道
        @param blank_num int 空白格数目
        """
        text_str = ''
        for text in self.text_list:
            text_str += (text + ' '*blank_num)
        return text_str

    def create_track(self,frame_index):
        """
        构建弹幕泳道
        @param frame_index int 第几帧画面的索引
        """
        # 创建透明背景
        transparent_bg = Image.new('RGBA', (self.w,self.h), (255,0,255,0))
        d = ImageDraw.Draw(transparent_bg)
        font = ImageFont.truetype('./comments_block/fonts/MSYH.ttc', self.font_size, encoding='utf-8')
        offset = 100 - frame_index*self.speed 
        d.text((offset,10), self.text_list_str(5), font=font, fill=self.color)
        # transparent_bg.show()
        return transparent_bg

class CommentsLayers:
    """
    输出第X帧的弹幕画面
    """
    def __init__(self,text_path,layer_w, layer_h, track_h=100,track_num=3):
        """
        构造方法
        @param text_path str 弹幕文本的路径
        @param track_num int 弹幕泳道行数
        @param track_w,track_h int 每条泳道高度(没有宽度是因为宽度与弹幕层宽度一样)
        @param layer_w,layer_h int 弹幕层背景宽度和高度
        """
        self.text_path = text_path
        self.track_num = track_num
        self.track_w = layer_w
        self.track_h = track_h
        self.layer_w = layer_w
        self.layer_h = layer_h

        # 创建颜色库、速度库
        speed_list = [6,8,9,10]
        color_list = [(0,0,255,255),(255,0,0,255),(255,0,255,255),(0,255,0,255)]
        # 实例化track_num个CommentsTrack类
        self.track_obj_list = []
        text_list = self.create_comments_layer()
        for track_index in range(self.track_num):
            speed = random.choice(speed_list)
            color = random.choice(color_list)
            track_obj = CommentsTrack(text_list[track_index], w=self.track_w, 
                                    h=self.track_h, color=color, speed=speed)
            self.track_obj_list.append(track_obj)        
        
    def text_to_list(self):
        """
        读取弹幕文本，转换成列表
        @return text_list list 弹幕列表
        """
        text_list = []
        with open(self.text_path, 'r', encoding='utf-8') as f:
            text_list = [f.strip() for f in f.readlines()]
        # print(text_list)
        return text_list

    def create_comments_layer(self):
        """
        将弹幕列表中的文本添加到弹幕泳道中
        @return final_list list 返回排列好的弹幕列表
        """
        text_list = self.text_to_list()
        text_len = len(text_list)
        # track_column为转置后的array列数
        track_column = math.ceil(text_len/self.track_num)
        text_array = np.arange(track_column*self.track_num)

        # 此处的track_num是指转置后的行数
        text_array = np.reshape(text_array, (track_column,self.track_num))
        # 进行转置操作
        text_array = text_array.T
        # 弹幕列表填不满text_array  用“ ”来代替填满text_array
        blank_list = []
        for i in range(text_array.size - text_len):
            blank_list.append(' ')
        # 将弹幕列表与空白格列表合并
        final_list = []
        final_list = np.concatenate((text_list,blank_list))

        return final_list[text_array]

    def manage_multi_layers(self, frame_index):
        """
        生成多个弹幕泳道
        @frame_index int 第X帧的弹幕画面
        @return multi_layers_bg list 返回生成的多个弹幕泳道
        """
        multi_layers_bg = Image.new('RGBA', (self.layer_w, self.layer_h), (255,0,255,0))

        for track_id, track_obj in enumerate(self.track_obj_list):
            comments_track = track_obj.create_track(frame_index)
            multi_layers_bg.paste(comments_track,(0,self.track_h*track_id))
        # multi_layers_bg.show()
        # multi_layers_bg_np = np.array(multi_layers_bg)
        # print('multi_layers_bg\'s shape: ',multi_layers_bg_np.shape)
        return multi_layers_bg


if __name__ == '__main__':
    # vp = VideoProcess('./comments_block/videos/video.mp4')
    # vp.video2mask()
    # text_list = ['111','222', '333']
    # ct = CommentsTrack(text_list)
    # bg = ct.create_track(1)
    # ct.text_list_str(5)

    # text_path = './comments_block/danmu_real.txt'
    # cl = CommentsLayers(text_path, 3)
    # # text = cl.text_to_list()
    # x = cl.manage_multi_layers(100)
    pass






