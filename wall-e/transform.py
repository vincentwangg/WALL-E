#!/usr/bin/python
import numpy as np


x=np.array([65,75,76,77,78,190])
y=np.array([0,75,76,77,78,255])

a=70.0
b=185.0
c=0.0
d=255.0



#for i in range(115):
#	x=i+70
#	#Linear Transform moves range of values
#	y=(x-a)/(b-a)*(d-c)+c
#	y=int(round(y))
#	print x,y


x=(x-a)/(b-a)*(d-c)+c
x=np.rint(x)

print x
