import mcpi.minecraft as minecraft
import mcpi.block as block

mc = minecraft.Minecraft.create()
pos = mc.player.getTilePos()
elem=5




class House:
    def __init__(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z
        print("I will build a house at",self.x,self.y,self.z)

    def naming(self,n):
        self.name=n
        
        
    def setLWH(self,l,w,h):
        self.l=l
        self.w=w
        self.h=h
        print("set the house's LWH:",l,w,h)
        
    def buildwall(self):
        for y in range(self.h):
            for a in range(self.l):
                mc.setBlock(self.x+a, self.y+y, self.z,elem)
                mc.setBlock(self.x+a, self.y+y, self.z+self.w-1,elem)
            for a in range(self.w):
                mc.setBlock(self.x, self.y+y, self.z+a,elem)
                mc.setBlock(self.x+self.l-1, self.y+y, self.z+a,elem)
                
    def buildroof(self):
        print("I will build a roof")
        '''
        for x in range(self.l):
            for z in range(self.w):
                mc.setBlock(pos.x+x, pos.y, pos.z+z,elem)
        '''
        for x in range(self.l+2):
            mc.setBlock(self.x-1+x, self.y, self.z-1,4)
            mc.setBlock(self.x-1+x, self.y, self.z+self.w,4)
        for z in range(self.w+2):
            mc.setBlock(self.x-1, self.y, self.z-1+z,4)
            mc.setBlock(self.x+self.l, self.y, self.z-1+z,4)
        
    def buildfloor(self):
        print("I will build floor")
        for x in range(self.l):
            for z in range(self.w):
                mc.setBlock(self.x+x, self.y+self.h-1, self.z+z,elem)
                mc.setBlock(self.x+x, self.y, self.z+z,elem)

    def buildDoorAndWindow(self):
        if self.h<4 or self.l<4 or self.w<4:
            print("The House is too small!")
            return
        mc.setBlock(self.x+self.l//2, self.y+1, self.z,64)
        mc.setBlock(self.x+self.l//2, self.y+2, self.z,64)

        mc.setBlock(self.x+self.l//2-1, self.y+1, self.z-1,38)
        mc.setBlock(self.x+self.l//2+1, self.y+1, self.z-1,38)
        
        for z in range(2):
            for y in range(2):
                mc.setBlock(self.x, self.y+y+2, self.z+z+self.w//2-1, 20)
                mc.setBlock(self.x+self.l-1, self.y+y+2, self.z+z+self.w//2-1, 20)

    def buildall(self):
        self.buildwall()
        self.buildroof()
        self.buildfloor()
        self.buildDoorAndWindow()
        #装饰
        for y in range(self.h):
            mc.setBlock(self.x,self.y+y,self.z,17)
            mc.setBlock(self.x+self.l-1,self.y+y,self.z,17)
            mc.setBlock(self.x,self.y+y,self.z+self.w-1,17)
            mc.setBlock(self.x+self.l-1,self.y+y,self.z+self.w-1,17)
            
        for x in range(self.l+2):
            mc.setBlock(self.x-1+x, self.y+self.h-1, self.z-1,5)
            mc.setBlock(self.x-1+x, self.y+self.h-1, self.z+self.w,5)
        for z in range(self.w+2):
            mc.setBlock(self.x-1, self.y+self.h-1, self.z-1+z,5)
            mc.setBlock(self.x+self.l, self.y+self.h-1, self.z-1+z,5)
            
        for x in range(self.l):
            mc.setBlock(self.x+x, self.y+self.h, self.z,5)
            mc.setBlock(self.x+x, self.y+self.h, self.z+self.w-1,5)
        for z in range(self.w):
            mc.setBlock(self.x, self.y+self.h, self.z+z,5)
            mc.setBlock(self.x+self.l-1, self.y+self.h, self.z+z,5)

        for x in range(self.l-2):
            for z in range(self.w-2):
                mc.setBlock(self.x+1+x, self.y+self.h+1, self.z+1+z,5)

        mc.setBlock(self.x+self.l//2, self.y, self.z-1,44)
        
    def buildcsv(self):
        elem1=57
        elem2=42

        f=open("floor.csv","r")
        x=0
        while True:
            line=f.readline()
            if line=="":
                break
            linedata=line.strip('\n').split(",")
            for z in range(len(linedata)):
                if linedata[z]=='1':
                    mc.setBlock(pos.x+x, pos.y, pos.z+z,elem1)
                else:
                    mc.setBlock(pos.x+x, pos.y, pos.z+z,elem2)
            x=x+1


house=House(pos.x,pos.y,pos.z)
house.setLWH(10,10,5)
house.naming("Bob")
house.buildall()



    
'''

#制作地板
elem1=57
elem2=42

f=open("floor.csv","r")
x=0
while True:
    line=f.readline()
    if line=="":
        break
    linedata=line.strip('\n').split(",")
    for z in range(len(linedata)):
        if linedata[z]=='1':
            mc.setBlock(pos.x+x, pos.y, pos.z+z,elem1)
        else:
            mc.setBlock(pos.x+x, pos.y, pos.z+z,elem2)
    x=x+1


house1=House(pos.x, pos.y, pos.z)

house1.setLWH(10,10,5)

house1.buildall()
house1.buildfloor()
'''

'''
def house(x0,y0,z0,L,W,H,M):
    for a in range(L):
        mc.setBlock(x0+a, y0, z0, elem)
        mc.setBlock(x0+a, y0, z0+W-1, elem)
    for a in range(W):
        mc.setBlock(x0, y0, z0+1+a, elem)
        mc.setBlock(x0+L-1, y0, z0+1+a, elem)
'''
