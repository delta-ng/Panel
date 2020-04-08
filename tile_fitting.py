# Given the roof <x1,y1> <x2,y2> <x3,y3> <x4,y4>
# Title <0,0> <C,0> <0,D> <C,D>
import math 
from PIL import Image, ImageDraw,ImageChops
# C=50
# D=50
class Polygon:
    def __init__(self):
        self.point=[]
    def addpoint(self,x,y=None):
        if not y:
            self.point.extend(x)
        else:
            self.point.extend([x,y])
    def normalize(self):
        x=min(self.point[::2])
        y=min(self.point[1::2])
        for i in range(0,len(self.point),2):
            self.point[i]-=x
            self.point[i+1]-=y
    def poly_order(self,arr=None):
        if arr==None:
            arr=self.point.copy()
        '''Since our Polygon is convex object'''
        if len(arr)<=6:
            return arr
        ele=[]
        x=[arr[i] for i in range(0,len(arr),2)]
        y=[arr[i] for i in range(1,len(arr),2)]
        centroid_x=sum(x)/len(x)
        centroid_y=sum(y)/len(y)
        slope=[]
        for i in range(len(x)):
            temp=(y[i]-centroid_y)/(x[i]-centroid_x) if x[i]!=centroid_x else math.inf
            tan=math.atan(temp)
            if (y[i]-centroid_y>0 and x[i]-centroid_x<0):
                tan=math.atan(temp)+180
            elif (y[i]-centroid_y<0 and x[i]-centroid_x<0):
                tan=math.atan(temp)-180
            slope.append([tan,i])
        slope.sort(reverse=True)
        # print(slope)
        for i in slope:
            ele.extend([x[i[1]],y[i[1]]])
        # print(ele)
        if arr==self.point:
            self.point=ele
        return ele
    def edge_intersect(self,i,xt=None,yt=None):
        # self.poly_order()
        # for i in range(0,len(self.point),2):
        x1,y1,x2,y2=self.point[i:i+4] if i!=len(self.point)-2 else self.point[i:i+2]+self.point[:2]
        if xt==None:
            return ((yt-y1)*(x2-x1)/(y2-y1))+x1 if y2<=yt<=y1 or y1<=yt<=y2 else math.inf
        elif yt==None:
            return ((y2-y1)*(xt-x1)/(x2-x1))+y1 if x2<=xt<=x1 or x1<=xt<=x2  else math.inf
        # print(eq(xt=0))
        # self.edge_func.append(eq)
    def point_check(self,x,y):
        x_pos=[]
        for i in range(1,len(self.point),2):
            if self.point[i]==y:
                if self.point[i-1]==x:
                    return True
                x_pos.append(self.point[i-1])
            elif i==len(self.point)-1:
                if (self.point[i]-y)*(self.point[1]-y)<0:
                    t=self.edge_intersect(i-1,yt=y)
                    if t!=math.inf:
                        x_pos.append(t)
            elif (self.point[i]-y)*(self.point[i+2]-y)<0:
                t=self.edge_intersect(i-1,yt=y)
                if t!=math.inf:
                    x_pos.append(t)
                # print(i,t,self.point[i],self.point[i+2],y)
        if len(x_pos)==0 or len(x_pos)==1:
            return False
        # print(x_pos)
        assert len(x_pos)==2,"Non Convex Polygon"
        x_pos.sort()
        if x_pos[0]<=x<=x_pos[1]:
            return True
        return False
    def poly_interest(self,x,y):
        points=[]
        if self.point_check(x,y):
            points.extend([x,y])
        if self.point_check(x+C,y):
            points.extend([x+C,y])
        if self.point_check(x,y+D):
            points.extend([x,y+D])
        if self.point_check(x+C,y+D):
            points.extend([x+C,y+D])
        if len(points)==8:
            return True
        if len(points)==0:
            return []
        for i in [x,x+C]:
            for j in range(0,len(self.point),2):
                t=self.edge_intersect(j,xt=i)
                if y<t<y+D:
                    if self.point_check(i,t):
                        points.extend([i,t])
            # if y<eq4(xt=i)<y+D:
            #     if point_check(i,eq4(xt=i)):
            #         points.extend([i,eq4(xt=i)])
            # if y<eq1(xt=i)<y+D:
            #     if point_check(i,eq1(xt=i)):
            #         points.extend([i,eq1(xt=i)])
            # if y<eq3(xt=i)<y+D:
            #     if point_check(i,eq3(xt=i)):
            #         points.extend([i,eq3(xt=i)])
        for i in [y,y+D]:
            for j in range(0,len(self.point),2):
                t=self.edge_intersect(j,yt=i)
                if x<t<x+C:
                    if self.point_check(t,i):
                        points.extend([t,i])
            #     # print("Yo1",eq2(yt=y))
            # if x<eq4(yt=i)<x+C:
            #     if point_check(eq4(yt=i),i):
            #         points.extend([eq4(yt=i),i])
            # if x<eq1(yt=i)<x+C:
            #     if point_check(eq1(yt=i),i):
            #         points.extend([eq1(yt=i),i])
            # if x<eq3(yt=i)<x+C:
            #     if point_check(eq3(yt=i),i):
            #         points.extend([eq3(yt=i),i])
        for i in range(0,len(self.point),2):
            if x<self.point[i]<x+C and y<self.point[i+1]<y+D:
                points.extend([self.point[i],self.point[i+1]])
        if len(points)>4:
            return self.poly_order(points)
        return []
        

a=Polygon()
# a.addpoint(0,800)
# a.addpoint(1000,1000)
# a.addpoint(800,100)
# a.addpoint(0,0)
# a.addpoint(980,990)
# a.poly_order()
# print(a.poly_interest(970,980))
# t,b,c,d=a.addedge_func()
# print(t(xt=0),b(xt=0),c(xt=0),d(xt=0))
    # ele=[]
    # if len(arr)==8:
    #     x=[[arr[i],i] for i in range(0,8,2)]
    #     x=sorted(x)
    #     # print(x)
    #     if arr[x[1][1]+1]>arr[x[0][1]+1]:
    #         p1=arr[x[1][1]:x[1][1]+2]
    #         p4=arr[x[0][1]:x[0][1]+2]
    #     else:
    #         p1=arr[x[0][1]:x[0][1]+2]
    #         p4=arr[x[1][1]:x[1][1]+2]
    #     x.pop(0)
    #     x.pop(0)
    #     # print(x)
    #     if arr[x[1][1]+1]>arr[x[0][1]+1]:
    #         p2=arr[x[1][1]:x[1][1]+2]
    #         p3=arr[x[0][1]:x[0][1]+2]
    #     else:
    #         p2=arr[x[0][1]:x[0][1]+2]
    #         p3=arr[x[1][1]:x[1][1]+2]
    # else:
    #     return arr
    # ele.extend(p1)
    # ele.extend(p2)
    # ele.extend(p3)
    # ele.extend(p4)
    # return ele
# print(poly_order([750, 920, 750, 960, 770.0, 920, 760.0, 960]))
# def eq1(xt=None,yt=None):
#     if xt==None:
#         return ((yt-y1)*(x2-x1)/(y2-y1))+x1 if y2!=y1 else math.inf
#     elif yt==None:
#         return ((y2-y1)*(xt-x1)/(x2-x1))+y1 if x2!=x1 else math.inf
# def eq2(xt=None,yt=None):
#     if xt==None:
#         return ((yt-y2)*(x3-x2)/(y3-y2))+x2 if y3!=y2 else math.inf
#     elif yt==None:
#         return ((y3-y2)*(xt-x2)/(x3-x2))+y2 if x3!=x2 else math.inf
#     # elif ((y2-y1)*(xt-x1)/(x2-x1))+y1>=yt:
#     #     return True
#     # return False
# def eq3(xt=None,yt=None):
#     if xt==None:
#         return ((yt-y3)*(x4-x3)/(y4-y3))+x3 if y4!=y3 else math.inf
#     elif yt==None:
#         return ((y4-y3)*(xt-x3)/(x4-x3))+y3 if x4!=x3 else math.inf
# def eq4(xt=None,yt=None):
#     if xt==None:
#         return ((yt-y4)*(x1-x4)/(y1-y4))+x4 if y1!=y4 else math.inf
#     elif yt==None:
#         return ((y1-y4)*(xt-x4)/(x1-x4))+y4 if x1!=x4 else math.inf
# def point_check(x,y):
#     '''Jordon Curve Theorm'''
#     temp1=eq1(xt=x)
#     temp3=eq3(xt=x)
#     temp2=eq2(yt=y)
#     temp4=eq4(yt=y)
#     if temp3<=y<=temp1 and temp4<=x<=temp2:
#         return True 
#     return False
# def poly(x,y):
#     points=[]
#     if point_check(x,y):
#         points.extend([x,y])
#     if point_check(x+C,y):
#         points.extend([x+C,y])
#     if point_check(x,y+D):
#         points.extend([x,y+D])
#     if point_check(x+C,y+D):
#         points.extend([x+C,y+D])
#     if len(points)==8:
#         return True
#     if len(points)==0:
#         return []
#     for i in [x,x+C]:
#         if y<eq2(xt=i)<y+D:
#             if point_check(i,eq2(xt=i)):
#                 points.extend([i,eq2(xt=i)])
#         if y<eq4(xt=i)<y+D:
#             if point_check(i,eq4(xt=i)):
#                 points.extend([i,eq4(xt=i)])
#         if y<eq1(xt=i)<y+D:
#             if point_check(i,eq1(xt=i)):
#                 points.extend([i,eq1(xt=i)])
#         if y<eq3(xt=i)<y+D:
#             if point_check(i,eq3(xt=i)):
#                 points.extend([i,eq3(xt=i)])
#     for i in [y,y+D]:
#         if x<eq2(yt=i)<x+C:
#             if point_check(eq2(yt=i),i):
#                 points.extend([eq2(yt=i),i])
#             # print("Yo1",eq2(yt=y))
#         if x<eq4(yt=i)<x+C:
#             if point_check(eq4(yt=i),i):
#                 points.extend([eq4(yt=i),i])
#         if x<eq1(yt=i)<x+C:
#             if point_check(eq1(yt=i),i):
#                 points.extend([eq1(yt=i),i])
#         if x<eq3(yt=i)<x+C:
#             if point_check(eq3(yt=i),i):
#                 points.extend([eq3(yt=i),i])
#     for i,j in zip([x1,x2,x3,x4],[y1,y2,y3,y4]):
#         if x<i<x+C and y<j<y+D:
#             points.extend([i,j])
#     if len(points)>4:
#         # print(points)
#         return poly_order(points)
#     return []
# a,b=list(map(int,input().split()))
# while(a>=0 and b>=0):
#     print(point_check(a,b))
#     a,b=list(map(int,input().split()))
print("All inputs are separated by space.")
print("Order of the vertic doesn't matter as the programmer is smart enough to figure out the order.")
C,D = list(map(int,input("Size of Title (C D):").split()))
n=int(input("Number of vertics of wall:"))
for i in range(n):
    a.addpoint(list(map(float,input("x"+str(i+1)+" y"+str(i+1)+":").split())))
a.normalize()
a.poly_order()
# x2,y2=list(map(float,input("x2 y2:").split()))
# x3,y3=list(map(float,input("x3 y3:").split()))
# x4,y4=list(map(float,input("x4 y4:").split()))
# min_=min(x1,x2,x3,x4)
# x1-=min_
# x2-=min_
# x3-=min_
# x4-=min_
# min_=min(y1,y2,y3,y4)
# y1-=min_
# y2-=min_
# y3-=min_
# y4-=min_
# # Input should be given in clockwise direction starting from top left corner point
# x1,y1,x2,y2,x3,y3,x4,y4=poly_order([x1,y1,x2,y2,x3,y3,x4,y4])
# A = max(x1,x2,x3,x4)
# B = max(y1,y2,y3,y4)
# C,D = list(map(int,input("Size of Title (C D):").split()))
# if( A%C + B%D > A%D + B%C):
#     temp=C
#     C=D
#     D=temp
# # rect(C,D,A,B)
x=C
y=D
A=math.ceil(max(a.point[::2]))
B=math.ceil(max(a.point[1::2]))
img = Image.new("RGB", (A, B))
imgo = Image.new("RGB", (A, B))
img_mask = Image.new("RGB", (A, B))
img_temp = ImageDraw.Draw(img_mask) 
img1_temp = ImageDraw.Draw(imgo) 
img_temp.polygon(a.point,fill="white")
count_full=0
count_edge=0
edge=[]
for j in range(0,B,y):
    for i in range(0,A,x):
        if a.poly_interest(i,j)==True:
            count_full+=1
        elif a.poly_interest(i,j)!=[]:
            count_edge+=1
            edge.append(a.poly_interest(i,j))
            img1_temp.polygon(edge[-1],outline="white")
        shape = [(i, j), (i+x-1, j+y-1)] 
        shape1 = [(i+1, j+1), (i+x-2, j+y-2)] 
        img1 = ImageDraw.Draw(img)   
        img1.rectangle(shape, fill ="#fff") 
        img1.rectangle(shape1, fill ="#000")
shape = [(0, 0), (A-1,B-1)] 
img1 = ImageDraw.Draw(img)   
img1.rectangle(shape, outline="#fff") 
img = ImageChops.multiply(img, img_mask)
img1 = ImageDraw.Draw(img) 
img1.polygon(a.point,outline="white")
img=img.transpose(Image.FLIP_TOP_BOTTOM)
imgo=imgo.transpose(Image.FLIP_TOP_BOTTOM)
img.show()
imgo.show()
# print("Number of Complete Panel of size ",C,"*",D," is ",count_full)
# print("Number of Edge Panel is ",count_edge)
# in_=input("Do you want the coordinates of the edge panel(y/n):")
# if in_.lower()=="y":
#     for i in range(len(edge)):
#         print(edge[i])