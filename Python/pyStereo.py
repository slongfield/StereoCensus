import Image, ImageOps
import os, sys

def evalString(pixel, string):
    return [x>pixel for x in string]

def getMaxBoxSize(pixelCoord, imageSize):
    return min([abs(pixelCoord[0]-imageSize[0]), abs(pixelCoord[1]-imageSize[1])])


def findDisparity(currentCoord, boxSize, source, target, direction):
    boxRadius = int(boxSize/2)
    x,y = currentCoord
    sourceBox = source.crop((x-boxRadius,y-boxRadius,x+boxRadius,y+boxRadius))

    sourceString = list(sourceBox.getdata())
    sourceString = evalString(sourceBox.getpixel((boxRadius,boxRadius)), sourceString)

    disparities = []
    
    if(direction == 1):
        for x2 in xrange(21):
            targetBox = target.crop((x2+x-boxRadius, y-boxRadius, x2+x+boxRadius, y+boxRadius))
            targetString = list(targetBox.getdata())

            targetString = evalString(targetBox.getpixel((boxRadius,boxRadius)), targetString)
            
            disparities.append(sum([a^b for a,b in zip(sourceString,targetString)]))
            
    elif(direction == -1):
        for x2 in xrange(20,-1,-1):
            targetBox = target.crop((x2+x-boxRadius, y-boxRadius, x2+x+boxRadius, y+boxRadius))
            targetString = list(targetBox.getdata())

            targetString = evalString(targetBox.getpixel((boxRadius,boxRadius)), targetString)

            disparities.append(sum([a^b for a,b in zip(sourceString,targetString)]))

    return disparities.index(min(disparities))

def disparitize(outFile, leftFile, rightFile, boxSize, direction):
    left = ImageOps.grayscale(Image.open(leftFile))
    right = ImageOps.grayscale(Image.open(rightFile))

    boxRadius = int(boxSize/2)

    if(direction == 1):
        xBounds = (boxRadius, left.size[0] - (boxRadius+20))
        yBounds = (boxRadius, left.size[1] - boxRadius)
    if(direction == -1):
        xBounds = (boxRadius + 20, left.size[0] - boxRadius)
        yBounds = (boxRadius, left.size[1] - boxRadius)
    
    
    result = Image.new('L', (xBounds[1]-xBounds[0],yBounds[1]-yBounds[0]))
    if(right.size != left.size):
        print "Images must be the same size."
        sys.exit(0)
    disparities = []

    for x in xrange(xBounds[0], xBounds[1]):
        for y in xrange(yBounds[0], yBounds[1]):
            result.putpixel((x-xBounds[0], y-yBounds[0]), 10*findDisparity((x,y), boxSize, left, right, direction))            
        print "Got to the next line!", x
    result.save(outFile)
    print "File saved!"

def fullImageDisparity(outFile, leftFile, rightFile):
    left = ImageOps.grayscale(Image.open(leftFile))
    right = ImageOps.grayscale(Image.open(rightFile))    
    result = Image.new('L', (left.size[0]-20,left.size[1]))

    leftString = list(left.getdata())
    rightString = list(right.getdata())

    disparities = []

    for x in xrange(left.size[0]-20):
        print "Next line", x
        for y in xrange(left.size[0]):
            print "Next pixel", y
            leftEval = evalString(left.getpixel((x,y)), leftString)
            
            for x2 in xrange(21):
                rightEval = evalString(right.getpixel((x+x2,y)), rightString)
                disparities.append(sum([a^b for a,b in zip(leftEval,rightEval)]))

            result.putpixel((x, y), 10*disparities.index(min(disparities)))
            disparities = []
    result.save(outFile)
    print "Bikutorii!"
    
if __name__=="__main__":
    fullImageDisparity("out.bmp", "left.png", "right.png")