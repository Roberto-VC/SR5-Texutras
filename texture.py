import struct
from gl import *
from vector import *

class Texture:
  def __init__(self,path):
    self.path = path
    self.read()

  def read(self):
    with open(self.path, "rb") as image:
      image.seek(2+4+2+2)
      header_size = struct.unpack("=l",image.read(4))[0]
      image.seek(2+4+2+2+4+4)
      self.width = struct.unpack("=l",image.read(4))[0]
      self.height = struct.unpack("=l",image.read(4))[0]

      image.seek(header_size)
      self.pixels=[]
      for y in range(self.width):
        self.pixels.append([])
        for x in range(self.height):
          b = ord(image.read(1))
          g = ord(image.read(1))
          r = ord(image.read(1))
          self.pixels[y].append(
            (b,g,r)
          )
      image.close()

  def getColor(self,tx,ty):
    x = round(tx * self.width)
    y = round(ty * self.height)

    return self.pixels[y][x]

  def getColori(self,tx,ty, intensity):
    tx = round(tx)
    ty = round(ty)
    b=round(self.pixels[ty][tx][0] * intensity)
    g=round(self.pixels[ty][tx][1] * intensity)
    r=round(self.pixels[ty][tx][2] * intensity)

    return (b,g,r)
    


b = Bitmap(1024,1024)
t = Texture("zubat.bmp")

b._fondo = t.pixels
b._color = (255,255,255)
cube = Obj("zubat.obj")

for face in cube.faces:
  if len(face) == 3:
    f1 = face[0][1]-1
    f2 = face[1][1]-1
    f3 = face[2][1]-1
    vt1 = V3(
      cube.tvertices[f1][0] * t.width,
      cube.tvertices[f1][1] * t.height
    )
    vt2 = V3(
      cube.tvertices[f2][0] * t.width,
      cube.tvertices[f2][1] * t.height
    )
    vt3 = V3(
      cube.tvertices[f3][0] * t.width,
      cube.tvertices[f3][1] * t.height
    ) 
    b.linea(vt1, vt2)
    b.linea(vt2, vt3)
    b.linea(vt3, vt1)
  else: 
    f1 = face[0][1]-1
    f2 = face[1][1]-1
    f3 = face[2][1]-1
    f4 = face[3][1]-1
    vt1 = V3(
      cube.tvertices[f1][0] * t.width,
      cube.tvertices[f1][1] * t.height
    )
    vt2 = V3(
      cube.tvertices[f2][0] * t.width,
      cube.tvertices[f2][1] * t.height
    )
    vt3 = V3(
      cube.tvertices[f3][0] * t.width,
      cube.tvertices[f3][1] * t.height
    ) 
    vt4 = V3(
      cube.tvertices[f4][0] * t.width,
      cube.tvertices[f4][1] * t.height
    ) 
    b.linea(vt1, vt2)
    b.linea(vt2, vt3)
    b.linea(vt3, vt4)
    b.linea(vt4, vt1)


b.write("hola.bmp") 


