#from math import *;u=lambda a,b,r:acos(sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)/r/2);circleintersection=lambda a,b,r:(2*u(a,b,r)-sin(2*u(a,b,r)))*r**2

#from math import *;u=lambda a,b,r:acos(sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)/r/2);circleintersection=lambda a,b,r: (lambda:(l) )()

#print (circleintersection([0,0],[10,10],1) )
#from math import *;circleintersection=lambda a,b,r:(lambda l=(sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)/r/2):(l<1)and int((2*acos(l)-sin(2*acos(l)))*r**2))()
#print (  circleintersection([0,0],[10,10],10) )

#l=abs(a[0]-b[0]+j*([1]-b[1]))
from math import *;circleintersection=lambda a,b,r:(lambda l=abs(a[0]-b[0]+1j*(a[1]-b[1]))/r/2:(l<1)and int((2*acos(l)-sin(2*acos(l)))*r**2))()
print (  circleintersection([0,0],[10,10],10) )
