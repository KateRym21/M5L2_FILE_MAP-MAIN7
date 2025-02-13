import pickle
class Mapmanager():
   """ Управління карткою """
   def __init__(self):
       self.model = 'block' # модель кубика лежить у файлі block.egg
       # # використовуються такі текстури:
       self.texture = 'block.png'
       self.colors = [
           (0.2, 0.2, 0.35, 1),
           (0.2, 0.5, 0.2, 1),
           (0.7, 0.2, 0.2, 1),
           (0.5, 0.3, 0.0, 1)
       ]

       # створюємо основний вузол картки:
       self.startNew()
        # створюємо будівельні блоки   
       self.addBlock((0,10, 0))
       self.addBlock((10,10, 0))
       self.addBlock((0,10, 10))


   def startNew(self):
       """створює основу для нової картки"""
       self.land = render.attachNewNode("Land") # вузол, до якого прив'язані всі блоки картки

   def getColor(self, z):
       if z < len(self.colors):
           return self.colors[z]
       else:
           return self.colors[len(self.colors) - 1]
   def addBlock(self, position):
       self.block = loader.loadModel(self.model)
       self.block.setTexture(loader.loadTexture(self.texture))
       self.block.setPos(position)
       self.color = self.getColor(int(position[2]))
       self.block.setColor(self.color)
       self.block.reparentTo(self.land)

       self.block.setTag("at", str(position))
       self.block.reparentTo(self.land)

   def buildBlocks(self,pos):
       x, y, z = pos
       new = self.findHighestEmpty(pos)
       if new[2] <= z + 1:
           self.addBlock(new)

   def buildBlocks(self,position):
       x, y, z = self.findHighestEmpty(position)
       pos = x, y, z, -1
       for block in self.finalBlocks(pos):
           block.removeNode()

   def delBlock(self,position):
       blocks = self.finalBlocks(position)
       for block in blocks:
           block.removeNode()

   def finalBlocks(self,pos):
        return self.land.findAllMatches("=at="+ str(pos))

   def isEmpty(self,pos):
       blocks = self.finalBlocks(pos)
       if blocks:
           return False
       else:
           return True

   def findHighestEmpty(self, pos):
       x, y, z = pos
       z = 1
       while not self.isEmpty((x, y, z)):
           z += 1
       return (x, y, z)


   def loadLand(self, fileName):
       with open(fileName) as file:
           y = 0
           for line in file:
                x = 0
                line = line.split(' ')
                for z in line:
                    for z0 in range(int(z)+1):
                        block = self.addBlock((x,y, z0))
                    x +=1
                y +=1
           return x,y


   def clear(self):
    self.land.removeNode()
    self.startNew()

   def saveMap(self):
         blocks = self.land.getChildren()
         with open("my_map.dat", "wb") as fout:
             pickle.dump(len(blocks),fout)

             for block in blocks:
                 x,y, z = block.getPos()
                 pos = (int(x), int(y),int(z))
                 pickle.dump(pos,fout)


   def loadMap(self):
     self.clear()
     with open("my_map.dat", "rb") as fin:
        lenght = pickle.load(fin)

        for i in range(lenght):
            pos = pickle.load(fin)
            self.addBlock(pos)



