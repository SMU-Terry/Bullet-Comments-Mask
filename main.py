#====================================================
# Author: Terry
# Address: ShanghaiTech University, Shanghai, China
# Date: 2022.5.4
#====================================================

import cv2 as cv
from cv2 import VideoWriter
import numpy as np
from PIL import Image
from CommentsTrackLayer import CommentsLayers
import os

class VideoProcess:
    def __init__(self, video_file_path):
        """
        构造方法
        @param  video_file_path  mp4格式视频
        """
        self.video_file_path = video_file_path

    def layers_composite(self):
        """
        合成视频与弹幕
        1.读取视频第X帧画面
        2.获取第X帧弹幕层画面，并用蒙版处理
        3.合成弹幕成与视频层
        4.保存为视频文件
        """
        cap = cv.VideoCapture(self.video_file_path)
        # 获取视频宽度与高度
        frame_w = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
        frame_h = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        # 获取帧率
        fps = int(cap.get(cv.CAP_PROP_FPS))
        # 构建视频写入器
        video_name = './comments_block/out_video/output.mp4'
        fourcc = cv.VideoWriter_fourcc(*'MP4V')
        video_writer = cv.VideoWriter(video_name,fourcc,fps,(frame_w,frame_h))

        # 实例化弹幕层
        text_path = './comments_block/danmu_real.txt'
        comments_layers = CommentsLayers(text_path, frame_w, frame_h, track_num=5)  

        frame_index = 0

        while True:
            ret,frame = cap.read()
            frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            if not ret:
                print('视频处理完毕')
                break
            
            # 对弹幕层进行蒙版处理
            frame_comments_layers = comments_layers.manage_multi_layers(frame_index)
            # frame_comments_layers.show()
            # frame_comments_layers_np = np.array(frame_comments_layers)
            # 读取蒙版
            masks_path = './comments_block/masks_img/'+str(frame_index)+'.jpg'
            # 只有背景有人时才会生成蒙版 所以会有些帧率没有蒙版图片 os.path判断一下
            if os.path.exists(masks_path):
                mask = cv.imread(masks_path)
                mask_gray = cv.cvtColor(mask, cv.COLOR_BGR2GRAY)
                # 对弹幕层转为numpy数组
                frame_comments_layers_np = np.asarray(frame_comments_layers)
                # 对弹幕层alpha通道进行处理
                frame_comments_layers_np[:,:,3] = np.where(mask_gray==255, 0, frame_comments_layers_np[:,:,3])
                # 转为image
                frame_comments_layers = Image.fromarray(frame_comments_layers_np)

            # 将视频层转化为RGBA格式
            frame_video_layer = cv.cvtColor(frame, cv.COLOR_BGR2RGBA)
            frame_video_layer_PIL = Image.fromarray(frame_video_layer)

            # 将视频层和弹幕层合成
            output = Image.alpha_composite(frame_video_layer_PIL,frame_comments_layers)
            # 转化为numpy格式
            output_np = np.asarray(output)
            # 转为RGB格式
            output = cv.cvtColor(output_np,cv.COLOR_RGBA2RGB)
            # output = cv.cvtColor(frame_comments_layers_np,cv.COLOR_RGBA2BGR)

            cv.imshow('Demo', output)
            video_writer.write(output)
            frame_index += 1
            if cv.waitKey(10) & 0xff==27:
                break
        
        video_writer.release()
        cap.release()
        cv.destroyAllWindows()


if __name__ == '__main__':
    vp = VideoProcess('./comments_block/videos/video.mp4')
    vp.layers_composite()

                




