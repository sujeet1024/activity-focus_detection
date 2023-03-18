import subprocess
import cv2
import numpy as np


class Engine():
    def __init__(self, *videos):
        self.videos = videos
        self.keys = ["Hotspot", "Focus"]
        self.hotspot_txts = {0: "deadzone", 1: "activity", 2: "hotspot"}
        self.hotspot_colors = {0: (0, 0, 255), 1: (255, 50, 50), 2: (50, 255, 50)}
        
        self.moving_averages = {k: None for k in self.keys}
        self.thresholds = {"Hotspot": (0.2, 0.8), "Focus": 150}
    
    def get_avg_meta_data(self, meta_data):
        alpha = 0.15
        for k in self.keys:
            if self.moving_averages[k] is None:
                self.moving_averages[k] = meta_data[k]
            else:
                self.moving_averages[k] = self.moving_averages[k] * alpha + meta_data[k] * (1 - alpha)
        return self.moving_averages
    
    def apply_thresholds(self, meta_data):
        if meta_data["Hotspot"] < self.thresholds["Hotspot"][0]:
            meta_data["Hotspot"] = 0
        elif meta_data["Hotspot"] < self.thresholds["Hotspot"][1]:
            meta_data["Hotspot"] = 1
        else:
            meta_data["Hotspot"] = 2
            
        meta_data["Focus"] = meta_data["Focus"] < self.thresholds["Focus"]
        
        return meta_data
    
    def check_if_focussed(self, frame):
        var = cv2.Laplacian(frame, cv2.CV_64F).var()
#         return var < 30
        return var # < self.thresholds["Focus"]
    
    def display_meta_data(self, frame, meta_data):
        hotspot_id = meta_data["Hotspot"]
        hotspot_txt = self.hotspot_txts[hotspot_id]
        hotspot_color =  self.hotspot_colors[hotspot_id]
        frame = cv2.putText(frame, hotspot_txt, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, hotspot_color, 3)
        
        focus = meta_data["Focus"]
        if focus:
            focus = "Blur"
            focus_color = (0, 0, 240)
        else:
            focus = "Focused"
            focus_color = (255, 50, 50)
        focus = str(focus)
        frame = cv2.putText(frame, focus, (200, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, focus_color, 3)
        
        return frame
    
    def check_if_moving(self, prev_fram, cur_frame):
        if prev_fram is None:
            return 0
        prev_gray = cv2.cvtColor(prev_fram, cv2.COLOR_BGR2GRAY) 
        cur_gray = cv2.cvtColor(cur_frame, cv2.COLOR_BGR2GRAY) 
        flow = cv2.calcOpticalFlowFarneback(prev_gray, cur_gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)

        norm =  20 * np.linalg.norm(flow) / np.linalg.norm(cur_frame)
        return norm
        
        
    def process(self, video_id):
        # self.video = cv2.VideoCapture(self.videos[video_id], 'API','FFMPEG')
        subprocess.Popen(f'ffmpeg -i {self.videos[video_id]} -vcodec copy -an -f mp4 toprocess.mp4')
        self.video = cv2.VideoCapture('toprocess.mp4')
        prev_frame = None
        
        while True:
            ret, frame = self.video.read()
            if ret:
                meta_data = {
                    "Hotspot": self.check_if_moving(prev_frame, frame),
                    "Focus": self.check_if_focussed(frame)
                }
                meta_data = self.get_avg_meta_data(meta_data)
                meta_data = self.apply_thresholds(meta_data)
                
                prev_frame = frame

                cv2.imshow("video", self.display_meta_data(frame, meta_data))
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            else:
                break
        
        
# engine = Engine("video1.mp4", "video2.mp4")
engine = Engine('Copy of 00099.MTS')
engine.process(0)
