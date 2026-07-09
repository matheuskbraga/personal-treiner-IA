import cv2

file_name = "video.mp4"

cap = cv2.VideoCapture(file_name)
scale = 0.5

while (cap.isOpened()):
    retorno, frame = cap.read()

    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dim = (width, height)
        
    # redimensionando o vídeo
    resized_frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
    
    if retorno == True:
        cv2.imshow("Video", resized_frame)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()