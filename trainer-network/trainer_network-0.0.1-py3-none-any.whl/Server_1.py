import cv2
import imagezmq
import numpy as np
import time
import timeit
from PIL import Image
import traceback

ip_addr='tcp://192.168.1.3'

cfg='cfg/yolov4.cfg'
weights='cfg/yolov4.weights'
names='cfg/coco.names'

image_hub0_0 = imagezmq.ImageHub(open_port='tcp://*:5660')
image_hub0_1 = imagezmq.ImageHub(open_port='tcp://*:5661')
image_hub0_2 = imagezmq.ImageHub(open_port='tcp://*:5662')
image_hub0_3 = imagezmq.ImageHub(open_port='tcp://*:5663')

image_hub1 = imagezmq.ImageHub(open_port='tcp://*:5670')
image_hub2 = imagezmq.ImageHub(open_port='tcp://*:5680')
image_hub3 = imagezmq.ImageHub(open_port='tcp://*:5690')

sender0_0 = imagezmq.ImageSender(connect_to=ip_addr+':5560', REQ_REP=False)
sender0_1 = imagezmq.ImageSender(connect_to=ip_addr+':5561', REQ_REP=False)
sender0_2 = imagezmq.ImageSender(connect_to=ip_addr+':5562', REQ_REP=False)
sender0_3 = imagezmq.ImageSender(connect_to=ip_addr+':5563', REQ_REP=False)

sender1 = imagezmq.ImageSender(connect_to=ip_addr+':5570', REQ_REP=False)
sender2 = imagezmq.ImageSender(connect_to=ip_addr+':5580', REQ_REP=False)
sender3 = imagezmq.ImageSender(connect_to=ip_addr+':5590', REQ_REP=False)

# sender_pic=imagezmq.ImageSender(connect_to='tcp://*:5557',REQ_REP=False)
# sender_face=imagezmq.ImageSender(connect_to='tcp://*:5558',REQ_REP=False)
# sender_face_detect=imagezmq.ImageSender(connect_to='tcp://*:5559',REQ_REP=False)
# sender_jpg=imagezmq.ImageSender(connect_to='tcp://*:5560',REQ_REP=False)
# for i in range(100):
#     port=i+9000
#     globals()[f'sender_picked_arr{port}']=imagezmq.ImageSender(connect_to=f'tcp://*:{port}',REQ_REP=False)

YOLO_net = cv2.dnn.readNet(cfg,weights)
classes = []
with open(names, "r") as f:
    classes = [line.strip() for line in f.readlines()]

YOLO_net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
YOLO_net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

kk=YOLO_net.getUnconnectedOutLayers()
#print(YOLO_net.getUnconnectedOutLayers())
k1=YOLO_net.getLayerNames()
#print("k1 : ",k1[300],"\nkk: ",kk)
kkk=kk.reshape(-1)

layer_names = YOLO_net.getLayerNames()
#print("layer_names = ",layer_names)
output_layers = [layer_names[i - 1] for i in kkk]#YOLO_net.getUnconnectedOutLayers()]
print(output_layers)
def Set_yolo(rpi_name, images):
    frame=images

    #ret, frame = VideoSignal.read()
    h, w, c = frame.shape
    print(f'init_set :{h}x{w}x{c}')
    x=0;y=0
    picked_img=frame[y:y+h,x:x+w]
    #cv2.imshow("frame",images)
    
    # blob = cv2.dnn.blobFromImage(frame, 1, (320, 320), (0, 0, 0),True, crop=True)
    blob = cv2.dnn.blobFromImage(frame, 1/255, (412, 412), (0, 0, 0),True, crop=True)
    # blob_test=cv2.dnn.imagesFromBlob(blob)#,1,(832,832),(0,0,0),True,crop=False)
    # blob_test=np.array(blob_test)
    
    # blob_test=np.reshape(blob_test[0],3)
    #blob = cv2.cvtColor(blob, cv2.COLOR_BGR2RGB)
    # print("====================",type(blob_test),blob_test.shape)
    
    # blob_img = Image.fromarray(blob_test.reshape(-1))
    # print("blob_img: ",type(blob_img), blob_img.size)
    # blob_img.show()#cv2.imshow("aa",blob_test[0])
    
    #cv2.imshow("blob",blob_test)
    # blob = cv2.dnn.blobFromImage(frame, 1/256, (720, 1280), (0, 0, 0),True, crop=False)
    #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0),thickness=1)
    YOLO_net.setInput(blob)
    outs = YOLO_net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []

    for out in outs:

        for detection in out:

            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.0001:
                # Object detected
                center_x = int(detection[0] * w)
                center_y = int(detection[1] * h)
                dw = int(detection[2] * w)
                dh = int(detection[3] * h)
                # Rectangle coordinate
                x = int(center_x - dw / 2)
                y = int(center_y - dh / 2)
                boxes.append([x, y, dw, dh])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    conf_threshold=0.5
    nms_threshold=0.4
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold,nms_threshold)
    jpg_buffer=b''
    property_={}
    #for h in range(len(indexes)):
    #    sub_dic={}
    #    index=int(indexes[h])
    #    con=round(confidences[index],3)
    #    sub_dic[f'{classes[class_ids[index]]}']=f'{boxes[h]}'
        #property_[h]=f"{classes[class_ids[index]]}({con})"
    #    property_[h]=sub_dic#f"{sub_dic}"
        #property_[f'{classes[class_ids[index]]}']=f'{boxes[h]}'
        #property_[f'{classes[class_ids[index]]}']=f'{boxes[h]}'
    #if h==0 or w==0:

    #picked_img=frame[y:y+h,x:x+w]
    #cv2.imshow('test',picked_img)
    picked_arr=[]
    #print('-------',indexes)
    #print('---boxes--',boxes)
    for i, box in enumerate(boxes):
        if i in indexes:
            tmp=[]
            for k in box:
                if k <0:
                    tmp.append(k*0)
                else:
                    tmp.append(k)

            x, y, w, h = tmp#boxes[i]
            label = str(classes[class_ids[i]])
            sub_dic={}
            #sub_dic[f'{label}']=f'{tmp}'
            #property_[h]=sub_dic
            #if label=='person':
            print(label)
            sub_dic[f'{label}']=f'{tmp}'
            property_[h]=sub_dic
            score = confidences[i]
            picked_img=frame[y:y+h,x:x+w]
            
            
            #gau_picked_img = cv2.GaussianBlur(picked_img, (99, 99), 10)
            #picked_arr.append(picked_img)
            
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0),thickness=1)
            #frame[y:y+h,x:x+w]=gau_picked_img
            
            
            
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0, 255), 1)
            print(f'{x},{y},{x+w},{y+h} \n confidence {score}')
            #picked_img=cv2.flip(picked_img, -1)
            #ret_code, jpg_buffer = cv2.imencode(
            #        ".jpg", picked_img, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
            
    return rpi_name, frame, picked_img,property_,picked_arr

images=b''
jpg_buffer=b''
face_image=b''
def Pub(name, images, flip_image,detect_data,cnt,picked_arr,sender):
    name_dic={}
    name_dic['name']=name
    detect_data[len(detect_data)]=name_dic
    detect_d=str(detect_data)

    sender.send_image(detect_data, images)
    #if jpg_buffer is not None:
        #sender_pic.send_jpg(name,jpg_buffer)
    # sender_pic.send_image(name,flip_image)
    # sender_face.send_image(name,face_image)
    # sender_face_detect.send_image(name,face_de)
    # if face_image is not None:
    #     jpeg_quality=95
    #     ret_code, jpg_buffer =cv2.imencode(
    #             '.jpg',face_image, [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality])
    #     sender_jpg.send_jpg(detect_d, jpg_buffer)
    print('===========================',len(picked_arr))
#     for i in range(th):
#         port_arr=list(map(int, detect_data.keys()))

#         port=i+9000
#         print('-----prot---',port)
#         #globals()[f'sender_picked_arr{port}']=imagezmq.ImageSender(connect_to=f'tcp://*:{port}',REQ_REP=False)
# #        globals()[f'sender_picked_arr{i}']=imagezmq.ImageSender(connect_to=f'tcp://*:{port}',REQ_REP=False)
# #        if i < th:#picked_arr[i]:# is not None:
#         picked_img=picked_arr[i]
#         if picked_img is not None:
#             jpeg_quality=95
#             ret_code, jpg_buffer =cv2.imencode(
#                     '.jpg',picked_img, [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality])
#             #sender_jpg.send_jpg(detect_d, jpg_buffer)
#         globals()[f'sender_picked_arr{port}'].send_jpg(name,jpg_buffer)
#        else:
#            w,h,c=images.shape
#            picked_img=np.zeros((w,h,3), np.uint8)
#            globals()[f'sender_picked_arr{port}'].send_image(name,picked_img)


#    for i,picked_img in enumerate(picked_arr):
#        globals()[f'sender_picked_arr{i}'].send_image(name,picked_img)

cnt=0
# def Face_detector(face_image, cascade):
#     x=0;y=0
#     h, w, c = face_image.shape
#     send_face_img=face_image[y:y+h,x:x+w]
#     #start_t=timeit.default_timer()
#     text='test'
#     face_image = cv2.resize(face_image,dsize=None,fx=1.0,fy=1.0)
#     gray = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
#     results = cascade.detectMultiScale(gray,
#             scaleFactor= 1.1,
#             minNeighbors=5,
#             minSize=(20,20)
#             )

#     for box in results:
#         x, y, w, h = box
#         test_box=[x,y,w,h]
#         print(f'boxes : {box}')
#         if test_box:
#             cv2.rectangle(face_image, (x,y), (x+w, y+h), (255,255,255), thickness=1)
#             cv2.putText(face_image,text,(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1)
#             send_face_img=face_image[y:y+h,x:x+w]
#             #terminate_t = timeit.default_timer()
#             #FPS = 'fps' + str(int(1./(terminate_t - start_t )))
#     return text, send_face_img, face_image
    #cv2.imshow('facenet',img)
    #if cv2.waitKey(1) > 0:
    #    break
th=0
try:
    while True:
        # cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_alt.xml')
        # text, face_image,face_de = Face_detector(picked_image,cascade)
        # images = cv2.rotate(images, cv2.ROTATE_90_COUNTERCLOCKWISE)#_CLOCKWISE)
        start = time.time()
        
        rpi_name0_0, images0_0 = image_hub0_0.recv_image()
        send_name0_0, send_image0_0,picked_image0_0,detect_data0_0,picked_arr0_0 = Set_yolo(rpi_name0_0,images0_0)
        image_hub0_0.send_reply(b'OK')
        Pub(send_name0_0, send_image0_0,picked_image0_0,detect_data0_0,cnt,picked_arr0_0,sender0_0)
        
        rpi_name0_1, images0_1 = image_hub0_1.recv_image()
        send_name0_1, send_image0_1,picked_image0_1,detect_data0_1,picked_arr0_1 = Set_yolo(rpi_name0_1,images0_1)
        image_hub0_1.send_reply(b'OK')
        Pub(send_name0_1, send_image0_1,picked_image0_1,detect_data0_1,cnt,picked_arr0_1,sender0_1)
        
        rpi_name0_2, images0_2 = image_hub0_2.recv_image()
        send_name0_2, send_image0_2,picked_image0_2,detect_data0_2,picked_arr0_2 = Set_yolo(rpi_name0_2,images0_2)
        image_hub0_2.send_reply(b'OK')
        Pub(send_name0_2, send_image0_2,picked_image0_2,detect_data0_2,cnt,picked_arr0_2,sender0_2)
        
        rpi_name0_3, images0_3 = image_hub0_3.recv_image()
        send_name0_3, send_image0_3,picked_image0_3,detect_data0_3,picked_arr0_3 = Set_yolo(rpi_name0_3,images0_3)
        image_hub0_3.send_reply(b'OK')
        Pub(send_name0_3, send_image0_3,picked_image0_3,detect_data0_3,cnt,picked_arr0_3,sender0_3)
        
        
        
        
                
        rpi_name1, images1 = image_hub1.recv_image()
        send_name1, send_image1,picked_image1,detect_data1,picked_arr1 = Set_yolo(rpi_name1,images1)
        image_hub1.send_reply(b'OK')
        Pub(send_name1, send_image1,picked_image1,detect_data1,cnt,picked_arr1,sender1)
        
        rpi_name2, images2 = image_hub2.recv_image()
        send_name2, send_image2,picked_image2,detect_data2,picked_arr2 = Set_yolo(rpi_name2,images2)
        image_hub2.send_reply(b'OK')
        Pub(send_name2, send_image2,picked_image2,detect_data2,cnt,picked_arr2,sender2)
        
        rpi_name3, images3 = image_hub3.recv_image()
        send_name3, send_image3,picked_image3,detect_data3,picked_arr3 = Set_yolo(rpi_name3,images3)
        image_hub3.send_reply(b'OK')
        Pub(send_name3, send_image3,picked_image3,detect_data3,cnt,picked_arr3,sender3)
        
        end = round(time.time()-start,3)
        second_start=time.time()
        cnt+=1
        second_end=round(time.time()-second_start,4)
        print(f'{cnt}: Time for recevied a image: {end}sec, Time for aired a image: {second_end}sec')
except(KeyboardInterrupt, SystemExit):
    print('Exit dut to keyboard interrupt')
except Exception as ex:
    print('Traceback error:',ex)
    traceback.print_exc()
finally:
    image_hub0_0.close()
    sender0_0.close()
    # sender_pic.close()
    # sender_face.close()
    # sender_face_detect.close()
    # sender_jpg.close()
    # for i in range(10):
    #     port=i+10000
    #     globals()[f'sender_picked_arr{port}'].close()
