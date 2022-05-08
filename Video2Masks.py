#====================================================
# Author: Terry
# Address: ShanghaiTech University, Shanghai, China
# Date: 2022.5.4
#====================================================

import cv2 as cv
import numpy as np
from pixellib.instance import instance_segmentation


class Video2Masks:
    def __init__(self, video_file_path) -> None:
        """
        构造方法
        @param  video_file_path  mp4格式视频
        """
        self.video_file_path = video_file_path

    def create_mask(self):
        """
        将视频文件处理成一帧帧蒙版图片
        """
        # 实例化 实例分割
        instance = instance_segmentation()
        instance.load_model("./comments_block/weights/mask_rcnn_coco.h5")     

        cap = cv.VideoCapture(self.video_file_path)
        
        # 记录帧数
        frame_index = 0
        while True:
            ret, frame = cap.read()
            frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            if not ret:
                print('视频处理完毕')
                break

            # 对人进行实例分割
            target_class = instance.select_target_classes(person=True)
            result,output = instance.segmentFrame(frame, segment_target_classes=target_class)
            
            # 如果该帧图片有人就进行处理
            person_num = len(result['class_ids'])
            if person_num > 0:
                # mask为识别出人的蒙版 shape=[h,w,p_index] 
                mask = result['masks']
                # 创建黑色底图
                mask_layer = np.zeros((output.shape[:2]))
                for p_index in range(person_num):
                    mask_layer = np.where(mask[:,:,p_index]==True, 255, mask_layer)

                # 将处理好的黑色底图保存
                mask_file = './masks_img'+str(frame_index)+'.jpg'
                cv.imwrite(mask_file, mask_layer)

                print('第%d帧处理完毕'%(frame_index))
            else:
                print('第%d帧无人'%(frame_index))

            frame_index += 1

            cv.imshow('Demo', mask_layer)
            if cv.waitKey(10) & 0xff==27:
                break
        
        cap.release()
        cv.destroyAllWindows()