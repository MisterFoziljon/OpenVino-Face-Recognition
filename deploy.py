from openvino.runtime import Core, get_version
from time import perf_counter
from pathlib import Path
import streamlit as st
import numpy as np
import cv2
import sys
import os

sys.path.append('common/python')
sys.path.append('common/python/openvino/model_zoo')

from utils import crop
from landmarks_detector import LandmarksDetector
from face_detector import FaceDetector
from faces_database import FacesDatabase
from face_identifier import FaceIdentifier

import monitors
from helpers import resolution
from images_capture import open_images_capture

from model_api.models import OutputTransform
from model_api.performance_metrics import PerformanceMetrics

st.title("Face Recognition")

class Frame_Processor():
    
    QUEUE_SIZE = 16
    face_detection_model = "models\\face-detection-retail-0004\FP32\\face-detection-retail-0004.xml"
    face_landmarks_model = "models\\landmarks-regression-retail-0009\\FP32\\landmarks-regression-retail-0009.xml"
    face_recognition_model = "models\\face-reidentification-retail-0095\FP32\\face-reidentification-retail-0095.xml"

    def __init__(self):
        core = Core()
        self.face_detector = FaceDetector(core, self.face_detection_model, (0,0), confidence_threshold=0.6, roi_scale_factor=1.15)
        self.landmarks_detector = LandmarksDetector(core, self.face_landmarks_model)
        self.face_identifier = FaceIdentifier(core, self.face_recognition_model, match_threshold=0.3, match_algo='HUNGARIAN')
        self.face_detector.deploy('CPU') # 'CPU', 'GPU', 'HETERO'
        self.landmarks_detector.deploy('CPU', self.QUEUE_SIZE)
        self.face_identifier.deploy('CPU', self.QUEUE_SIZE)
        self.faces_database = FacesDatabase("data", self.face_identifier, self.landmarks_detector, None, False)
        self.face_identifier.set_faces_database(self.faces_database)
    
    def process(self, frame):
        orig_image = frame.copy()
        rois = self.face_detector.infer((frame,))

        if self.QUEUE_SIZE < len(rois):
            rois = rois[:self.QUEUE_SIZE]

        landmarks = self.landmarks_detector.infer((frame, rois))
        face_identities, unknowns = self.face_identifier.infer((frame, rois, landmarks))

        
        if False and len(unknowns) > 0:
            for i in unknowns:
                if rois[i].position[0] == 0.0 or rois[i].position[1] == 0.0 or \
                    (rois[i].position[0] + rois[i].size[0] > orig_image.shape[1]) or \
                    (rois[i].position[1] + rois[i].size[1] > orig_image.shape[0]):
                    continue

                crop_image = crop(orig_image, rois[i])
                name = self.faces_database.ask_to_save(crop_image)
                
                if name:
                    id = self.faces_database.dump_faces(crop_image, face_identities[i].descriptor, name)
                    face_identities[i].id = id

        return [rois, landmarks, face_identities]


class Recognition:
    def __init__(self):
        pass

    def draw_detections(self, frame, frame_processor, detections, output_transform):
        size = frame.shape[:2]
        frame = output_transform.resize(frame)
        
        for roi, landmarks, identity in zip(*detections):
            text = frame_processor.face_identifier.get_identity_label(identity.id)
            if identity.id != FaceIdentifier.UNKNOWN_ID:
                text += ' %.2f%%' % (100.0 * (1 - identity.distance))

            xmin = max(int(roi.position[0]), 0)
            ymin = max(int(roi.position[1]), 0)
            xmax = min(int(roi.position[0] + roi.size[0]), size[1])
            ymax = min(int(roi.position[1] + roi.size[1]), size[0])
            
            xmin, ymin, xmax, ymax = output_transform.scale([xmin, ymin, xmax, ymax])
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 220, 0), 2)

            textsize = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 1)[0]
            cv2.rectangle(frame, (xmin, ymin), (xmin + textsize[0], ymin - textsize[1]), (255, 255, 255), cv2.FILLED)
            cv2.putText(frame, text, (xmin, ymin), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 1)

        return frame

    def use_camera(self, api):
        cap = open_images_capture(api, False)
        frame_processor = Frame_Processor()
        FRAME_WINDOW = st.image([])

        metrics = PerformanceMetrics()
        presenter = None
        output_transform = None
        input_crop = None
            
        while True:
            start_time = perf_counter()
            frame = cap.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            output_resolution = (3*frame.shape[1]/4, 3*frame.shape[0]/4)
            output_transform = OutputTransform(frame.shape[:2], output_resolution)
            output_resolution = output_transform.new_resolution
                
            presenter = monitors.Presenter("", 55, (round(output_resolution[0] / 4), round(output_resolution[1] / 8)))

            detections = frame_processor.process(frame)
                
            presenter.drawGraphs(frame)

            frame = self.draw_detections(frame, frame_processor, detections, output_transform)

            metrics.update(start_time, frame)
                
            FRAME_WINDOW.image(frame)                
            
        metrics.log_total()


def main():
    recognition = Recognition()
    api = None
    with st.sidebar:
        st.title("Camera Properties")
        user = st.text_input("user: ", placeholder="admin")
        password = st.text_input("password: ", placeholder="AEZAKMI12")
        ip = st.text_input("ip: ", placeholder="192.168.0.102")
        rtsp = st.text_input("port: ",placeholder="554")

        if st.button("start"):
            api = f"rtsp://admin:AEZAKMI12@192.168.0.102:554/h264/ch1/main/av_stream"
            #api = f"rtsp://{user}:{password}@{ip}:{rtsp}/h264/ch1/main/av_stream"

    if api:
        recognition.use_camera(api)
        
if __name__ == "__main__":
    main()
