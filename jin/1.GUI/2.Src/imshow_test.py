import cv2

cap = cv2.VideoCapture(0)
	
while True:
	ret, fram = cap.read()
	
	if ret:
		gray = cv2.cvtColor(fram, cv2.COLOR_BGR2GRAY)
		cv2.imshow('video', gray)
		
	else:
		print('error')

cap.release()
cv2.destroyAllWindows()