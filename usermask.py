import cv2
import numpy as np



def mask(point,i,image):
	img = cv2.imread(image)

	# convert image to grayscale
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	# define polygon points
	points = np.array( point, dtype=np.int32 )

	# draw polygon on input to visualize
	img_poly = img.copy()
	cv2.polylines(img_poly, [points], True, (0,0,255), 1)

	# create mask for polygon
	mask = np.zeros_like(gray)
	cv2.fillPoly(mask,[points],(255))

	# get color values in gray image corresponding to where mask is white
	values = gray[np.where(mask == 255)]

	# count number of white values
	count = 0
	for value in values:
		if value == 255:
			count = count + 1
	print("count =",count)

	if count > 5:
		result = img.copy()
		result[mask==255] = (0,0,0)
	else:
		result = img


	# save results
	cv2.imwrite('C:/Users/gunas/Music/Flask/figures/tmp/mask'+str(i+1)+'.png', mask)
	#cv2.imshow('barn_poly', img_poly)
	#cv2.imshow('barn_mask', mask)
	#cv2.imshow('barn_result', result)
	return 

# mouse call back function

		


def process_content(points):	
	cont_img='C:/Users/gunas/Music/Flask/figures/content/content.png'
	for i in range(0,len(points)):
		point=points[i][0:-1]
		mask(point,i,cont_img)
	

