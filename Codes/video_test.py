import tensorflow as tf
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np
import cv2
import time

# loading the stored model from file
interpreter = tf.lite.Interpreter(model_path='../Raspi_codes/lite_model.tflite')
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details= interpreter.get_output_details()
interpreter.resize_tensor_input(input_details[0]['index'],(1,64,64,3))
interpreter.resize_tensor_input(output_details[0]['index'], [1,3])
interpreter.allocate_tensors()

#opencv for capturing video
cap = cv2.VideoCapture('./video_test.mp4')
time.sleep(2)
if cap.isOpened():
    rval, frame = cap.read()
else:
    rval = False
IMG_SIZE = 64
alert = 0
flag = 0
while(1):

    rval, image = cap.read()
    if rval==True:
        orig = image.copy()
        
        # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.resize(image, (IMG_SIZE, IMG_SIZE))  
        image = image.astype("float") / 255.0
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)
        
        tic = time.time()
        interpreter.set_tensor(input_details[0]['index'], image)
        interpreter.invoke()
        tflite_results = interpreter.get_tensor(output_details[0]['index'])
        toc = time.time()
        
        fire_prob = tflite_results[0][1] * 100
        smoke_prob = tflite_results[0][2] * 100
        print("Time taken = ", toc - tic)
        print("FPS: ", 1 / np.float64(toc - tic))
        print("Fire Probability: ", fire_prob)
        print("Smoke Probability: ", smoke_prob)
        print(image.shape)
        
        label = "Fire Probability: " + str(fire_prob)
        cv2.putText(orig, label, (10, 25),  cv2.FONT_HERSHEY_SIMPLEX,0.7, (0, 255, 0), 2)
        label = "Smoke Probability: " + str(smoke_prob)
        cv2.putText(orig, label, (10, 60),  cv2.FONT_HERSHEY_SIMPLEX,0.7, (0, 255, 0), 2)

        cv2.imshow("Output", orig)
        
        key = cv2.waitKey(10)
        if key == 27: # exit on ESC
            break
    elif rval==False:
            break
end = time.time()
cap.release()
cv2.destroyAllWindows()