import Image

def datToImage(inFile, outFile, width, height):
  """Reads a list from inFile, outputs an image of dimensions widthXheightto outFile"""

  inFile = open(inFile, 'r')

  output = Image.new('L', (width+1,height)) #grayscale, widthXheight

  for y in range(120+451*2*30+1):
    inFile.readline()

  for y in range(height):
      for x in range(width+1):
        inFile.readline()
        a = int(inFile.readline(),16)
        if(a < 90):
          output.putpixel((x,y),3*a)
        else:
          output.putpixel((x,y),0)
      
  output.save(outFile)

      
if __name__=="__main__":
  datToImage("out.list","View2_View6_90md_3scale_60ham.bmp",450,375)
