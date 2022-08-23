from logging import exception
import struct

class Bitmap():
  def __init__(self, width, height):
    self._bcBitCount = 24
    self._headerbits = 14
    self._headerbitmap = 40
    self._bcWidth = width
    self._bcHeight = height
    self._color = (45, 0, 0)
    self._bfSize = self._bcWidth*3*self._bcHeight
    self._dotsx= []
    self._dotsy= []
    self._texture = None
    self.clear()


  def clear(self):
    self._fondo = [ [self._color]*self._bcHeight for i in range(self._bcWidth)]
    self._zbuffer = [ [-999999]*self._bcHeight for i in range(self._bcWidth)]
    

  def clearColor(self, r, g, b):
    self._color = (b,g,r)

  def Vertex(self, x, y):
    if isinstance(self._color, tuple):
      if x < 0 or y < 0 or x > self._bcWidth or y > self._bcHeight:
        raise ValueError('Coords out of range')
      if len(self._color) != 3:
        raise ValueError('Color must be a tuple of 3 elems')
      self._fondo[y-1][x-1] = (self._color[0], self._color[1], self._color[2])
      self._dotsx.append(x)
      self._dotsy.append(y)
  
    else:
      raise ValueError('Color must be a tuple of 3 elems')


  def getDotx(self):
      return self._dotsx

  def getDoty(self):
      return self._dotsy

  def Clear(self):
    self._dotsx.clear()
    self._dotsy.clear()
    
  def write(s, file):
    with open(file, 'wb') as f:
      f.write(struct.pack('<hlhhl', 
                   19778,
                   14+40+s._bcHeight*s._bcWidth*3, 
                   0,
                   0,
                   40+14)) # Writing BITMAPFILEHEADER
      f.write(struct.pack('<lllhhllllll', 
                   40, 
                   s._bcWidth, 
                   s._bcHeight, 
                   1, 
                   s._bcBitCount,
                   0,
                   s._bfSize,
                   0,
                   0,
                   0,
                   0)) # Writing BITMAPINFO
      for x in range(s._bcWidth):
        for y in range(s._bcHeight):
          f.write(struct.pack('<BBB', s._fondo[x][y][0], s._fondo[x][y][1], s._fondo[x][y][2]))


  def linea(self, A, B):
    
    x0 = round(A.x)
    x1 = round(B.x)
    y0 = round(A.y)
    y1 = round(B.y)
    
    dx = abs(x1-x0)
    dy = abs(y1-y0)
    
    inclinado = dy>dx
    if inclinado:
      x0, y0 = y0, x0
      x1, y1 = y1, x1
  
    if x0 > x1:
      x0,x1=x1,x0
      y0,y1=y1,y0

    dy = abs(y1 - y0)
    dx = abs(x1 - x0)
    
    offset = 0
    thres = dx
    y = y0

    for x in range(x0,x1+1):
      if inclinado:
        self.Vertex(y, x)
      else:
        self.Vertex(x, y)

        
      
      offset += dy*2
      if offset >= thres:
        y += 1 if y0<y1 else -1
        thres += dx *2

class Obj(object):
  def __init__(self, filename):
    with open(filename) as f:
      self.lines = f.read().splitlines()
      self.tvertices = []
      self.vertices = []
      self.faces = []

      for line in self.lines:
        prefix, value = line.split(" ",1)
        if prefix == "v":
          self.vertices.append((list(map(float,value.split(' ')))))
        if prefix == "vt":
          self.tvertices.append((list(map(float,value.split(' ')))))
        if prefix == "f":
          self.faces.append([list(map(int,face.split("/"))) for face in value.split()])