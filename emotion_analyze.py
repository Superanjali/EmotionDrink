import requests
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib import patches
from io import BytesIO
import os
import cv2
from timeit import default_timer as timer

# Parameters #########################################################

cv_blue = (255,0,0)
last_event = timer() - 20
param_windowname = 'EmotionDrink'

# If you are using a Jupyter notebook, uncomment the following line.
#%matplotlib inline

# Replace <Subscription Key> with your valid subscription key.
subscription_key = "4dbd5770efe843119b3e3281bd2efdeb" #DSFace API

# Set image path from local file.
image_path = os.path.join('Aishwariya_Rai_(face).jpg')

assert subscription_key

# You must use the same region in your REST call as you used to get your
# subscription keys. For example, if you got your subscription keys from
# westus, replace "westcentralus" in the URI below with "westus".
#
# Free trial subscription keys are generated in the westcentralus region.
# If you use a free trial subscription key, you shouldn't need to change
# this region.
face_api_url = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect'

image_data = open(image_path, "rb")

headers = {'Content-Type': 'application/octet-stream',
           'Ocp-Apim-Subscription-Key': subscription_key}
'''
params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,' +
    'emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'
}
'''
params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,emotion'
}

emotion_multi = {
        'anger': 4., 
        'contempt': 0, 
        'disgust': 0, 
        'fear': 0, 
        'happiness': 1., 
        'neutral': 0, 
        'sadness': 2., 
        'surprise': 1.        
        }
# %%

# Methods ############################################################

def get_top_emotion(face):
    emotions = face["faceAttributes"]['emotion']
    inverse = [(emotions[key]*emotion_multi[key], key) for key in emotions]
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    print(emotions)
    print(inverse)
    return max(inverse)

def get_emotion(image_data):  
    response = requests.post(face_api_url, params=params, headers=headers, data=image_data)
    response.raise_for_status()
    faces = response.json()
    rez = []
    for face in faces:
        fr = face["faceRectangle"]
        top_emo = get_top_emotion(face)
        rez.append((fr,top_emo))
    return rez
        
def put_text(img, x, y, text, color):
    '''Write text on the image
    Modifies the paramter image. No return necessary
    '''
    fontFace = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 1
    thickness = 2 #change thickness
    boxsize, baseline = cv2.getTextSize(text, fontFace, fontScale, thickness)
    cv2.putText(img, text, (x,y + boxsize[1]), fontFace, fontScale, color, thickness)
    
# %%    


if False:
    response = requests.post(face_api_url, params=params, headers=headers, data=image_data)
    response.raise_for_status()
    faces = response.json()
    
    # Display the original image and overlay it with the face information.
    image_read = open(image_path, "rb").read()
    image = Image.open(BytesIO(image_read))
    
    plt.figure(figsize=(8, 8))
    ax = plt.imshow(image, alpha=1)
    for face in faces:
        fr = face["faceRectangle"]
        fa = face["faceAttributes"]
        origin = (fr["left"], fr["top"])
        p = patches.Rectangle(
            origin, fr["width"], fr["height"], fill=False, linewidth=2, color='b')
        ax.axes.add_patch(p)
        top_emo = get_top_emotion(face)
        #print(top_emo)
        #plt.text(origin[0], origin[1], "%s, %d"%(fa["gender"].capitalize(), fa["age"]),fontsize=20, weight="bold", va="bottom")
        plt.text(origin[0], origin[1], "%.3f, %s"%(top_emo[0],top_emo[1]),fontsize=20, weight="bold", va="bottom")
        
    _ = plt.axis("off")
    plt.show()


#%%

# Main code ##########################################################
cam = cv2.VideoCapture(0)
cv2.namedWindow(param_windowname, cv2.WINDOW_NORMAL)
cv2.resizeWindow(param_windowname, 640, 480)

while True:
    # 1 Read frame, break if no frame available
    ret, frame = cam.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)

    # 2 Check user input
    k = cv2.waitKey(1)
    if k>0:
       print(k, chr(k))
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    
    if k ==  32:
        #space pressed turn on classifier
        last_event = timer()
        img_str = cv2.imencode('.jpg', frame)[1].tostring()
        emo = get_emotion(img_str)
        #print(emo)
    
    #print results for limited amount of time:
    time_passed = timer() - last_event
    if time_passed < 5:
        for elem in emo:
            text = elem[1][1]
            x,y = elem[0]['left'],elem[0]['top']
            w,h = elem[0]['width'],elem[0]['height']
            put_text(frame,x,y-30,text,cv_blue)
            cv2.rectangle(frame,(x,y),(x+w,y+h),cv_blue, 1)
    
    cv2.imshow(param_windowname,frame)
    
cam.release()
cv2.destroyAllWindows()

# %%
