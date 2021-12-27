import cv2

imageFile = '/home/minsu/MST/서구청역지도.PNG'
img  = cv2.imread(imageFile)    # cv2.IMREAD_COLOR

#cv2.imshow('Map',img)

#meter per minute
man = 91.8
woman = 86.4
kid = 40

#중심좌표
x = 459
y = 418
# area 1
x1 = 419
y1 = 158
#area 2
x2 = 710
y2 = 445
#area 3
x3 = 406
y3 = 684
#area 4
x4 = 199
y4 = 441

time = int(input('시간을 입력하시오(분) : ')) #min
area = int(input('구역을 입력하시오 : ')) #1,2,3,4
Distinction = input('man, woman, kid 중 고르시오 : ') #man, woman, kid
print(type(Distinction)) #str

# time = 15
# area = 1
# Distinction = kid
print(type(Distinction))    #str

imageCircle = img.copy()
#d = kid*time #반경


if Distinction == man and area ==1 :
    distance = man * time
    print('distance :',distance)
    cv2.circle(imageCircle,(int(x1+distance/2),int(y1+distance/2)),int(distance/2), (255,0,0),thickness=2, lineType=cv2.LINE_AA)

elif  Distinction == man and area ==2 :
    distance = man * time
    print('distance :',distance)
    cv2.circle(imageCircle,(int(x2+distance/2),int(y2+distance/2)),int(distance/2), (255,0,0),thickness=2, lineType=cv2.LINE_AA)

elif  Distinction == man and area ==3 :
    distance = man * time
    print('distance :',distance)
    cv2.circle(imageCircle,(int(x3+distance/2),int(y3+distance/2)),int(distance/2), (255,0,0),thickness=2, lineType=cv2.LINE_AA)

elif Distinction == man and area ==4 :
    distance = man * time
    print('distance :',distance)
    cv2.circle(imageCircle,(int(x4+distance/2),int(y4+distance/2)),int(distance/2), (255,0,0),thickness=2, lineType=cv2.LINE_AA)

elif Distinction == woman and area ==1 :
    distance = woman * time
    print('distance :',distance)
    cv2.circle(imageCircle,(int(x1+distance/2),int(y1+distance/2)),int(distance/2), (255,0,0),thickness=2, lineType=cv2.LINE_AA)

elif  Distinction == woman and area ==2 :
    distance = woman * time
    print('distance :',distance)
    cv2.circle(imageCircle,(int(x2+distance/2),int(y2+distance/2)),int(distance/2), (255,0,0),thickness=2, lineType=cv2.LINE_AA)

elif  Distinction == woman and area ==3 :
    distance = woman * time
    print('distance :',distance)
    cv2.circle(imageCircle,(int(x3+distance/2),int(y3+distance/2)),int(distance/2), (255,0,0),thickness=2, lineType=cv2.LINE_AA)

elif Distinction == woman and area ==4 :
    distance = woman * time
    print('distance :',distance)
    cv2.circle(imageCircle,(int(x4+distance/2),int(y4+distance/2)),int(distance/2), (255,0,0),thickness=2, lineType=cv2.LINE_AA)

elif Distinction == kid and area ==1 :
    distance = kid * time
    print('distance :',distance)
    cv2.circle(imageCircle,(int(x1+distance/2),int(y1+distance/2)),int(distance/2), (255,0,0),thickness=2, lineType=cv2.LINE_AA)

elif  Distinction == kid and area ==2 :
    distance = kid * time
    print('distance :',distance)
    cv2.circle(imageCircle,(int(x2+distance/2),int(y2+distance/2)),int(distance/2), (255,0,0),thickness=2, lineType=cv2.LINE_AA)

elif  Distinction == kid and area ==3 :
    distance = kid * time
    print('distance :',distance)
    cv2.circle(imageCircle,(int(x3+distance/2),int(y3+distance/2)),int(distance/2), (255,0,0),thickness=2, lineType=cv2.LINE_AA)

elif Distinction == kid and area ==4 :
    distance = kid * time
    print('distance :',distance)
    cv2.circle(imageCircle,(int(x4+distance/2),int(y4+distance/2)),int(distance/2), (255,0,0),thickness=2, lineType=cv2.LINE_AA)


#cv2.circle(imageCircle,(x,y),d, (255,0,0),thickness=2, lineType=cv2.LINE_AA)
#원의 중심, 반지름, 선의 색, 굵기, 선 표현법


cv2.imshow("image circle", imageCircle)

cv2.waitKey()
cv2.destroyAllWindows()