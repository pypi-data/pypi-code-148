import socket
import time
from imutils.video import VideoStream
import imagezmq
import cv2
import traceback
import sys

ip_addr='tcp://192.168.1.3'
input_image=''
output_image=''

image_hub0_0 = imagezmq.ImageHub(open_port=ip_addr+':5560', REQ_REP=False)
image_hub0_1 = imagezmq.ImageHub(open_port=ip_addr+':5561', REQ_REP=False)
image_hub0_2 = imagezmq.ImageHub(open_port=ip_addr+':5562', REQ_REP=False)
image_hub0_3 = imagezmq.ImageHub(open_port=ip_addr+':5563', REQ_REP=False)

image_hub1 = imagezmq.ImageHub(open_port=ip_addr+':5570', REQ_REP=False)
image_hub2 = imagezmq.ImageHub(open_port=ip_addr+':5580', REQ_REP=False)
image_hub3 = imagezmq.ImageHub(open_port=ip_addr+':5590', REQ_REP=False)



sender0_0 = imagezmq.ImageSender(connect_to=ip_addr+':5660')
sender0_1 = imagezmq.ImageSender(connect_to=ip_addr+':5661')
sender0_2 = imagezmq.ImageSender(connect_to=ip_addr+':5662')
sender0_3 = imagezmq.ImageSender(connect_to=ip_addr+':5663')

sender1 = imagezmq.ImageSender(connect_to=ip_addr+':5670')
sender2 = imagezmq.ImageSender(connect_to=ip_addr+':5680')
sender3 = imagezmq.ImageSender(connect_to=ip_addr+':5690')

rpi_name = "shit"#socket.gethostname() # send RPi hostname with each image
 
picam = cv2.VideoCapture(input_image) #0) #VideoStream(usePiCamera=True).start()

videoFileName = output_image#'All_detectingIMG_1500.avi'
w = round(picam.get(cv2.CAP_PROP_FRAME_WIDTH)) # width
h = round(picam.get(cv2.CAP_PROP_FRAME_HEIGHT)) #height
fps = picam.get(cv2.CAP_PROP_FPS) #frame per second
fourcc = cv2.VideoWriter_fourcc(*'DIVX') #fourcc
delay = round(1000/fps)		

out = cv2.VideoWriter(videoFileName, fourcc, fps, (w,h))
if not (out.isOpened()):
	print("File isn't opend!!")
	picam.release()
	sys.exit()


#time.sleep(2.0)  # allow camera sensor to warm up
try:
    while True:  # send images as stream until Ctrl-C
        ret,image_orign = picam.read(0)
        print("image_orign.shap: ",image_orign.shape, len(image_orign),len(image_orign[0]))
        if ret:
            image_orign0=image_orign[0:int(len(image_orign)/2)-1,0:int(len(image_orign[0])/2)-1]
            image_orign1=image_orign[0:int(len(image_orign)/2)-1,int(len(image_orign[0])/2):] 
            image_orign2=image_orign[int(len(image_orign)/2):,0:int(len(image_orign[0])/2)-1]
            image_orign3=image_orign[int(len(image_orign)/2):,int(len(image_orign[0])/2):]
            
            image_orign0_0=image_orign0[0:int(len(image_orign0)/2)-1,0:int(len(image_orign0[0])/2)-1]
            image_orign0_1=image_orign0[0:int(len(image_orign0)/2)-1,int(len(image_orign0[0])/2):] 
            image_orign0_2=image_orign0[int(len(image_orign0)/2):,0:int(len(image_orign0[0])/2)-1]
            image_orign0_3=image_orign0[int(len(image_orign0)/2):,int(len(image_orign0[0])/2):]
            
            sender0_0.send_image("1/4_0", image_orign0_0)
            sender0_1.send_image("1/4_1", image_orign0_1)
            sender0_2.send_image("1/4_2", image_orign0_2)
            sender0_3.send_image("1/4_3", image_orign0_3)
            
            sender1.send_image("2/4", image_orign1)
            sender2.send_image("3/4", image_orign2)
            sender3.send_image("4/4", image_orign3)
            #image_orign=cv2.resize(image_orign, None,None,5,5,cv2.INTER_CUBIC)
            
            image_name0_0, image0_0 = image_hub0_0.recv_image()
            out.write(image0_0)
            print(image0_0.shape)
            cv2.imshow("1/4_0", image0_0)
            
            image_name0_1, image0_1 = image_hub0_1.recv_image()
            out.write(image0_1)
            print(image0_1.shape)
            cv2.imshow("1/4_1", image0_1)
            
            image_name0_2, image0_2 = image_hub0_2.recv_image()
            out.write(image0_2)
            print(image0_2.shape)
            cv2.imshow("1/4_2", image0_2)
            
            image_name0_3, image0_3 = image_hub0_3.recv_image()
            out.write(image0_3)
            print(image0_3.shape)
            cv2.imshow("1/4_3", image0_3)
    
            image_name1, image1 = image_hub1.recv_image()
            print(image1.shape)
            cv2.imshow("2/4", image1)
        
            image_name2, image2 = image_hub2.recv_image()
            print(image2.shape)
            cv2.imshow("3/4", image2)
            
            image_name3, image3 = image_hub3.recv_image()
            print(image3.shape)
            cv2.imshow("4/4", image3)
            
            cv2.waitKey(delay)  # wait until a key is pressed
            if cv2.waitKey(delay) == 27:
                break
        else:
            print("ret is false")
            break
except(KeyboardInterrupt, SystemExit):
    print('Exit dut to keyboard interrupt')
except Exception as ex:
    print('Traceback error:',ex)
    traceback.print_exc()
finally:
	picam.release()
	out.release()
	cv2.destroyAllWindows()