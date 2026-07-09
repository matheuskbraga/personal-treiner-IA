import cv2
import mediapipe as mp
import numpy as np

from mediapipe.tasks import python
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2


file_name = "video/video.mp4"

def draw_landmarks_on_image(rgb_image, detection_result):
  pose_landmarks_list = detection_result.pose_landmarks
  annotated_image = np.copy(rgb_image)

  pose_landmark_style = drawing_styles.get_default_pose_landmarks_style()
  pose_connection_style = drawing_utils.DrawingSpec(color=(0, 255, 0), thickness=2)

  for pose_landmarks in pose_landmarks_list:
    drawing_utils.draw_landmarks(
        image=annotated_image,
        landmark_list=pose_landmarks,
        connections=vision.PoseLandmarksConnections.POSE_LANDMARKS,
        landmark_drawing_spec=pose_landmark_style,
        connection_drawing_spec=pose_connection_style)

  return annotated_image

cap = cv2.VideoCapture(file_name)
scale = 0.5
model_path = 'pose_landmarker_full.task'

options = python.vision.PoseLandmarkerOptions(
    base_options=python.BaseOptions(model_asset_path=model_path),
    running_mode=python.vision.RunningMode.VIDEO,
)

print()

with python.vision.PoseLandmarker.create_from_options(options) as landmarker:
    while (cap.isOpened()):
        retorno, frame = cap.read()
        fps = cap.get(cv2.CAP_PROP_FPS)
        calc_ts = [0.0]

        width = int(frame.shape[1] * scale)
        height = int(frame.shape[0] * scale)
        dim = (width, height)
            
        # redimensionando o vídeo
        resized_frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
        
        if retorno == True:
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=resized_frame)
            calc_ts.append(int(calc_ts[-1] + 1 / fps))

            detection_result = landmarker.detect_for_video(mp_image, calc_ts[-1])
            cv2.imshow("Video", resized_frame)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break

cap.release()
cv2.destroyAllWindows()