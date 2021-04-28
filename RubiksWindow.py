import copy
import tkinter as tk
from tkinter import Canvas, BOTH
from RubixCube import RubixCube, Faces, Colors

rubik = RubixCube()

def rotateRight():
    rubik.rotateFace(Faces.RIGHT, 0)
    updateCanvas()

def rotateTop():
    rubik.rotateFace(Faces.TOP, 0)
    updateCanvas()

def rotateFront():
    rubik.rotateFace(Faces.FRONT, 0)
    updateCanvas()

root = tk.Tk()
root.geometry("550x480")
root.title("Rubiks Cube")
topBar = tk.Label(root)
topBar.pack()
b1 = tk.Button(root, text='FRONT', width=15, command=rotateFront)
b1.place(x=30,y=0)
b2 = tk.Button(root, text='RIGHT', width=15, command=rotateRight)
b2.place(x=220,y=0)
b2 = tk.Button(root, text='TOP', width=15, command=rotateTop)
b2.place(x=400,y=0)
canvas = Canvas(root,bg="#fff")

def drawOnCanvas(frontFace,rightFace,topFace):
    canvas.delete("all")
    drawRubixCube(canvas,frontFace,(70,50))
    drawRubixCube(canvas, rightFace, (320, 50))
    drawRubixCube(canvas, topFace, (180, 260))
    canvas.pack(fill=BOTH, expand=1)

colorMappings= {
    Colors.WHITE:"#fff",
    Colors.RED: "#f00",
    Colors.BLUE: "#22f",
    Colors.ORANGE: "#f60",
    Colors.GREEN: "#0f0",
    Colors.YELLOW: "#f66"
}
def drawRubixCube(canvas, face1State, startPos):
    cubeSize = 50
    y = startPos[1]
    padding = 2
    for row in face1State:
        x = startPos[0]
        for color in row:
            canvas.create_rectangle(x, y , x + cubeSize , y + cubeSize , outline="#111",fill=colorMappings[color], width=2)
            x += cubeSize + padding
        y += cubeSize + padding

def updateCanvas():
    #Some transformations are applied to the rubiks cube view so the data is formatted how the presentation code expects
    frontFace = reverseVertical(ninteyDegrees(convertToArrArr(rubik.viewFace(Faces.FRONT))))
    rightFace = reverseVertical((reverseHorizontal(convertToArrArr(rubik.viewFace(Faces.RIGHT)))))
    topFace = ninteyDegrees(convertToArrArr(rubik.viewFace(Faces.TOP)))
    drawOnCanvas(frontFace, rightFace , topFace)

def convertToArrArr(face):
    return  [face[0:3],face[3:6],face[6:9]]

def ninteyDegrees(face):
    return [[face[0][0],face[1][0],face[2][0]],
        [face[0][1], face[1][1], face[2][1]],
        [face[0][2], face[1][2], face[2][2]]]

def reverseVertical(face):
    faceCops = copy.deepcopy(face)
    faceCops.reverse()
    return faceCops

def reverseHorizontal(face):
    faceCopy = copy.deepcopy(face)
    faceCopy[0].reverse()
    faceCopy[1].reverse()
    faceCopy[2].reverse()
    return faceCopy

updateCanvas()
root.mainloop()