import maya.cmds as cmds
import random as rnd

if 'myWin' in globals():
    if cmds.window(myWin, exists=True):
        cmds.deleteUI(myWin, window=True)

if 'nextBlockId' not in globals():
    nextBlockId = 1000


myWin = cmds.window(title="Lego Blocks", menuBar=True,  topLeftCorner=(100,1000))

cmds.menu(label="Basic Options")
cmds.menuItem(label="New Scene", command=('cmds.file(new=True, force=True)'))
cmds.menuItem(label="Delete Selected", command=('cmds.delete()'))

##STANDARD BLOCK
cmds.frameLayout(collapsable=True, label="Standard Block", width=475, height=130)
cmds.columnLayout()
cmds.intSliderGrp('blockHeight',l="Height", f=True, min=1, max=20, value=3)
cmds.intSliderGrp('blockWidth', l="Width (Bumps)", f=True, min=1, max=20, value=2)
cmds.intSliderGrp('blockDepth', l="Depth (Bumps)", f=True, min=1, max=20, value=8)
cmds.colorSliderGrp('blockColour', label="Colour", hsv=(120, 1, 1))
cmds.button(label="Create Basic Block", command=('basicBlock()'))
cmds.setParent( '..' )
cmds.setParent( '..' )

##SLOPED BLOCK
cmds.frameLayout(collapsable=True, label="Sloped Block", width=475, height=110)
cmds.columnLayout()
cmds.intSliderGrp('slopedWidth', l="Width (Bumps)", f=True, min=1, max=20, value=2)
cmds.intSliderGrp('slopedDepth', l="Depth (Bumps)", f=True, min=2, max=4, value=2)
cmds.colorSliderGrp('slopedColour', label="Colour", hsv=(120, 1, 1))
cmds.button(label="Create Slope Block", command=('slopedBlock()'))
cmds.setParent( '..' )
cmds.setParent( '..' )

#BLOCK WITH HOLES
cmds.frameLayout(collapsable=True, label="Hole Block", width=475, height=90)
cmds.columnLayout()

#Changed min value on width to 2 since there is no width 1
cmds.intSliderGrp('holeWidth', l="Width (Bumps)", f=True, min=2, max=20, value=2)
cmds.colorSliderGrp('holeColour', label="Colour", hsv=(120, 1, 1))
cmds.button(label="Create Hole Block", command=('holeBlock()'))
cmds.setParent( '..' )
cmds.setParent( '..' )

#BEAM
cmds.frameLayout(collapsable=True, l="Beam", width=475, height=130)
cmds.columnLayout()
cmds.radioButtonGrp('bEndHoles', la4 = ["Both Holes", "Both Crosses", "Cross, Hole", "Hole, Cross"], nrb=4, da1 = 1, da2 = 2, da3 = 3, da4 = 4, sl = 1)
cmds.radioButtonGrp('bDepths', la2 = ["Full Depth", "Half Depth"], nrb=2, da1 = 1, da2 = 2, sl = 1)
cmds.intSliderGrp('beamWidth', l="Width", f=True, min=2, max=20, value=3)
cmds.colorSliderGrp('beamColour', l="Colour", hsv=(120, 1, 1))
cmds.button(label="Create Beam Block", command=('beamBlock()'))
cmds.setParent( '..' )
cmds.setParent( '..' )

#(MULTI)ANGULAR BEAM
cmds.frameLayout(collapsable=True, l="(Multi) Angular Beam", width=475, height=190)
cmds.columnLayout()
cmds.checkBox('enMultiAngle', l = "Multi-Angle Beam", onc = ("activateCommand()"), ofc = ("deactivateCommand()"))
cmds.radioButtonGrp('degrees', la3 = ["90 deg", "53.5 deg", "T shape"], nrb=3, da1 = 1, da2 = 2, da3 = 3, sl = 1)
cmds.radioButtonGrp('endHoles', la4 = ["Both Holes", "Both Crosses", "Cross, Hole", "Hole, Cross"], nrb=4, da1 = 1, da2 = 2, da3 = 3, da4 = 4, sl = 1)
cmds.intSliderGrp('aBeamLength1', l="Length 1", f=True, min=2, max=10, value=3)
cmds.intSliderGrp('aBeamLength2', l="Length 2", f=True, min=2, max=10, value=3)
cmds.intSliderGrp('aBeamLength3', l="Length 3", f=True, min=2, max=10, value=3, en = False)
cmds.colorSliderGrp('aBeamColour', l="Colour", hsv=(120, 1, 1))
cmds.button(label="Create Angular Beam", command=('angularBeam()'))
cmds.setParent( '..' )
cmds.setParent( '..' )

#GUI FOR WHEEL
cmds.frameLayout(collapsable=True, label="Wheel & Hub Caps", width=475, height=130)
cmds.columnLayout()
cmds.intSliderGrp('WheelSize', l="Wheel (Size)", f=True, min=1, max=20, value=2)
cmds.intSliderGrp('WheelThickness',l="Wheel (Thickness)", f=True, min=1, max=20, value=2)
cmds.colorSliderGrp('WheelColour', label="Wheel Colour", hsv=(120, 1, 1))
cmds.colorSliderGrp('hubColour', label="Hub Colour", hsv=(120, 1, 1))
cmds.button(label="Create Wheel", command=('wheel()')) 
cmds.setParent( '..' )
cmds.setParent( '..' )

cmds.showWindow(myWin)

#for the Angle beam Gui
#Activates the degree radio buttons and deactivates the length 3 slider
#Because mulit angle blocks have set degrees, and would need to set the length of the second angle's arm
def activateCommand():
    Angle = cmds.radioButtonGrp('degrees', e = True, en = False)
    Length3 = cmds.intSliderGrp('aBeamLength3', e = True, en = True)

#deactivates the degree radio buttons and activates the length 3 slider
def deactivateCommand():
    Angle = cmds.radioButtonGrp('degrees', e = True, en = True)
    Length3 = cmds.intSliderGrp('aBeamLength3', e = True, en = False)
    
#Creates a standard lego block
def basicBlock():
    blockHeight = cmds.intSliderGrp('blockHeight', q=True, v=True)
    blockWidth = cmds.intSliderGrp('blockWidth', q=True, v=True)
    blockDepth = cmds.intSliderGrp('blockDepth', q=True, v=True)
    rgb = cmds.colorSliderGrp('blockColour', q=True, rgbValue=True)

    #Creates the temporary namespace
    global nextBlockId
    nsTmp = "Block" + str(nextBlockId)
    nextBlockId = nextBlockId + 1
    createNamespace(nsTmp)

    cubeSizeX = blockWidth * 0.8
    cubeSizeZ = blockDepth * 0.8
    cubeSizeY = blockHeight * 0.32

    cmds.polyCube(h=cubeSizeY, w=cubeSizeX, d=cubeSizeZ)
    cmds.move((cubeSizeY/2.0), moveY=True)
    for i in range(blockWidth):
        for j in range(blockDepth):
            cmds.polyCylinder(r=0.25, h=0.20)
            cmds.move((cubeSizeY + 0.10), moveY=True, a=True)
            cmds.move(((i * 0.8) - (cubeSizeX/2.0) + 0.4), moveX=True, a=True)
            cmds.move(((j * 0.8) - (cubeSizeZ/2.0) + 0.4), moveZ=True, a=True)

    myShader = cmds.shadingNode('lambert', asShader=True, name="blckMat")
    cmds.setAttr(nsTmp+":blckMat.color",rgb[0],rgb[1],rgb[2], typ='double3')
    cmds.polyUnite((nsTmp+":*"), n=nsTmp, ch=False)
    cmds.delete(ch=True)
    cmds.hyperShade(assign=(nsTmp+":blckMat"))
    cmds.namespace(removeNamespace=":"+nsTmp,mergeNamespaceWithParent=True)

#creates a sloped block
def slopedBlock():
    blockHeight = 3
    blockWidth = cmds.intSliderGrp('slopedWidth', q=True, v=True)
    blockDepth = cmds.intSliderGrp('slopedDepth', q=True, v=True)
    rgb = cmds.colorSliderGrp('slopedColour', q=True, rgbValue=True)

    global nextBlockId
    nsTmp = "Block" + str(nextBlockId)
    nextBlockId = nextBlockId + 1
    createNamespace(nsTmp)

    cubeSizeX = blockWidth * 0.8
    cubeSizeZ = blockDepth * 0.8
    cubeSizeY = blockHeight * 0.32

    cmds.polyCube(h=cubeSizeY, w=cubeSizeX, d=cubeSizeZ, sz=blockDepth)
    cmds.move((cubeSizeY/2.0), y=True, a=True)

    for i in range(blockWidth):
        cmds.polyCylinder(r=0.25, h=0.20)
        cmds.move((cubeSizeY + 0.10), moveY=True, a=True)
        cmds.move(((i * 0.8) - (cubeSizeX/2.0) + 0.4), moveX=True, a=True)
        cmds.move((0 -(cubeSizeZ/2.0) + 0.4), moveZ=True)

    myShader = cmds.shadingNode('lambert', asShader=True, name="blckMat")
    cmds.setAttr(nsTmp+":blckMat.color", rgb[0], rgb[1], rgb[2], typ='double3')

    cmds.polyUnite((nsTmp+":*"), n=nsTmp, ch=False)
    cmds.delete(ch=True)
    cmds.hyperShade(assign=(nsTmp+":blckMat"))

    cmds.select((nsTmp+":"+nsTmp+".e[1]"), r=True)
    cmds.move(0, -0.8, 0, r=True)
    if blockDepth == 4:
        tV = cmds.xform((nsTmp + ":" + nsTmp + ".vtx[8]"), q=True, t=True)
        cmds.select((nsTmp + ":" + nsTmp + ".vtx[6]"), r=True)
        cmds.move(tV[0], tV[1], tV[2], a=True)

        tV = cmds.xform((nsTmp + ":" + nsTmp + ".vtx[9]"), q=True, t=True)
        cmds.select((nsTmp + ":" + nsTmp + ".vtx[7]"), r=True)
        cmds.move(tV[0], tV[1], tV[2], a=True)

    if blockDepth >= 3:
        tV = cmds.xform((nsTmp + ":" + nsTmp + ".vtx[6]"), q=True, t=True)
        cmds.select((nsTmp + ":" + nsTmp + ".vtx[4]"), r=True)
        cmds.move(tV[0], tV[1], tV[2], a=True)

        tV = cmds.xform((nsTmp + ":" + nsTmp + ".vtx[7]"), q=True, t=True)
        cmds.select((nsTmp + ":" + nsTmp + ".vtx[5]"), r=True)
        cmds.move(tV[0], tV[1], tV[2], a=True)

    cmds.namespace( removeNamespace=":"+nsTmp, mergeNamespaceWithParent = True)

#creates the hole block
def holeBlock():
    blockWidth = cmds.intSliderGrp('holeWidth', q=True, v=True)
    rgb = cmds.colorSliderGrp('holeColour', q=True, rgbValue=True)

    global nextBlockId
    nsTmp = "Block" + str(nextBlockId)
    nextBlockId = nextBlockId + 1
    createNamespace(nsTmp)
    
    cubeSizeX = (blockWidth) * 0.8
    cubeSizeZ = 0.8
    cubeSizeY = .96

    #Create Cube
    cmds.polyCube(width = cubeSizeX, height = cubeSizeY, depth = cubeSizeZ, sh = 2, sd = 2)
    cmds.move(0, (cubeSizeY/2), 0)

    #separate loop for punching holes 
    for i in range(blockWidth-1):
        moveX = (((i+.5) * 0.8) - (cubeSizeX/2.0) + 0.4)
        punchHole(.25, 2, 90, moveX, .5, nsTmp, ":pCube1", "pCube1")

    #add bumps to cube and also rename it to pCube1 for loop friendly code
    for i in range(blockWidth):
        #Create pipe, used to make bump
        cmds.polyPipe(r=.25, h=.4, t=.05)
        cmds.move(((i * 0.8) - (cubeSizeX/2.0) + 0.4), moveX=True, a=True)
        cmds.move((cubeSizeY + 0.10), moveY=True, a=True)
        BOOLEAN(nsTmp, ":pPipe1", ":pCube1", 1, "pCube1")
    
    myShader = cmds.shadingNode('lambert', asShader=True, name="blckMat")
    cmds.setAttr(nsTmp+":blckMat.color", rgb[0], rgb[1], rgb[2], typ='double3')

    #since there is no need for unite, one last rename to nsTMP to add texture
    cmds.select(nsTmp +":pCube1")
    cmds.rename(nsTmp)
    cmds.hyperShade(assign=(nsTmp+":blckMat"))
    cmds.namespace( removeNamespace=":"+nsTmp, mergeNamespaceWithParent = True)

#creates beam
def beamBlock():
    endHole = cmds.radioButtonGrp('bEndHoles', q = True, sl = True)
    blockWidth = cmds.intSliderGrp('beamWidth', q=True, v=True)
    blockDepth = cmds.radioButtonGrp('bDepths', q = True, sl = True)
    rgb = cmds.colorSliderGrp('beamColour', q=True, rgbValue=True)

    global nextBlockId
    nsTmp = "Beam" + str(nextBlockId)
    nextBlockId = nextBlockId + 1
    createNamespace(nsTmp)
    
    #determines the hole type [crosses/holes] at each end of the beam
    if endHole == 1:
        aHole = 1
        bHole = 1
    elif endHole == 2:
        aHole = 2
        bHole = 2
    elif endHole == 3:
        aHole = 2
        bHole = 1
    elif endHole == 4:
        aHole = 1
        bHole = 2

    buildBeam(blockWidth, blockDepth, nsTmp, aHole, bHole, "beam")
    myShader = cmds.shadingNode('lambert', asShader=True, name="blckMat")
    cmds.setAttr(nsTmp+":blckMat.color", rgb[0], rgb[1], rgb[2], typ='double3')

    cmds.select(nsTmp + ":beam")
    cmds.rename(nsTmp)
    
    cmds.xform(cp = True)
    cmds.move(0, nsTmp + ":" + nsTmp + ".scalePivot", nsTmp + ":" + nsTmp + ".rotatePivot", moveY = True)
    cmds.hyperShade(assign=(nsTmp+":blckMat"))
    cmds.namespace( removeNamespace=":"+nsTmp, mergeNamespaceWithParent = True)

#creates the angular and multi angular beam
def angularBeam():
    Length1 = cmds.intSliderGrp('aBeamLength1', q=True, v=True)
    Length2 = cmds.intSliderGrp('aBeamLength2', q=True, v=True)
    endHole = cmds.radioButtonGrp('endHoles', q = True, sl = True)
    Angle = cmds.radioButtonGrp('degrees', q = True, sl = True)
    MultiAngle = cmds.checkBox('enMultiAngle', q = True, v = True)
    rgb = cmds.colorSliderGrp('aBeamColour', q=True, rgbValue=True)


    global nextBlockId
    nsTmp = "Beam" + str(nextBlockId)
    nextBlockId = nextBlockId + 1
    createNamespace(nsTmp)

    if endHole == 1:
        aHole = 1
        bHole = 1
    elif endHole == 2:
        aHole = 2
        bHole = 2
    elif endHole == 3:
        aHole = 2
        bHole = 1
    elif endHole == 4:
        aHole = 1
        bHole = 2

    #if/else statement handleing if the user is building a muli-angular or just a regular angular beam
    buildBeam(Length1, 1, nsTmp, 1, aHole, "BeamA")
    if MultiAngle == False:
        buildBeam(Length2, 1, nsTmp, 1, bHole, "BeamB")
        cmds.select(nsTmp +":BeamB")
        cmds.move(.4, nsTmp + ":BeamB.scalePivot", nsTmp + ":BeamB.rotatePivot", moveY = True)

    if MultiAngle == True:
        buildBeam(Length2, 1, nsTmp, 1, 1,"BeamB")
        cmds.select(nsTmp +":BeamB")
        cmds.move(.4, nsTmp + ":BeamB.scalePivot", nsTmp + ":BeamB.rotatePivot", moveY = True)

        Length3 = cmds.intSliderGrp('aBeamLength3', q=True, v=True)
        buildBeam(Length3, 1, nsTmp, 1, bHole, "BeamC")
        cmds.select(nsTmp +":BeamC")
        cmds.move(.4, nsTmp + ":BeamC.scalePivot", nsTmp + ":BeamC.rotatePivot", moveY = True)

        cmds.select(nsTmp +":BeamB")
        cmds.rotate(143.5, rotateZ=True)

        cmds.select(nsTmp +":BeamC")
        cmds.rotate(90, rotateZ=True)
        cmds.move((Length2-1)*-.643, moveX = True)
        cmds.move(((Length2-1)*.476), moveY = True)

    else:
        if Angle == 1:
            cmds.select(nsTmp +":BeamB")
            cmds.rotate(90, rotateZ=True)
        elif Angle == 2:
            cmds.select(nsTmp +":BeamB")
            cmds.rotate(143.5, rotateZ=True)
        elif Angle == 3:

            if Length1 % 2 == 1:
                cmds.select(nsTmp +":BeamB")
                cmds.rotate(90, rotateZ=True)
                cmds.move((Length1/2)*.8, moveX = True)
            else:
                print["Error: Length 1 must be an odd number"]
                cmds.delete(nsTmp + ":BeamB")
                cmds.delete(nsTmp + ":BeamB")
    
    myShader = cmds.shadingNode('lambert', asShader=True, name="blckMat")
    cmds.setAttr(nsTmp+":blckMat.color",rgb[0],rgb[1],rgb[2], typ='double3')

    cmds.polyUnite((nsTmp+":*"), n=nsTmp, ch=False)
    cmds.delete(ch=True)

    cmds.hyperShade(assign=(nsTmp+":blckMat"))
    cmds.namespace(removeNamespace=":"+nsTmp,mergeNamespaceWithParent=True)

#creates the wheel and calls the hub cap function
def wheel():
    wheelSize = cmds.intSliderGrp('WheelSize', q = True, v= True)
    wheelThickness = cmds.intSliderGrp('WheelThickness', q = True, v= True)
    rgb = cmds.colorSliderGrp('WheelColour', q=True, rgbValue=True) 
    global nextBlockId

    nsTmp = "Wheel" + str(nextBlockId)

    hubCap(nextBlockId, wheelSize, wheelThickness)
    
    createNamespace(nsTmp)

    wheelSizeY = wheelThickness *.1
    displaceY = (wheelThickness*.5) *.1
    for i in range(0, 2):   
        #Create cylinder
        cmds.polyCylinder(r=wheelSize*0.3, h=wheelSizeY, sa = 50)
        facetCount = cmds.polyEvaluate(nsTmp + ":pCylinder1", face=True)
        cmds.move((-1*((wheelSizeY)/2)), nsTmp + ":pCylinder1.scalePivot", nsTmp + ":pCylinder1.rotatePivot", moveY = True, os = True)
        cmds.move(displaceY, moveY = True)
        #eliminating the non-side Faces
        facetCount = facetCount - 2

        for j in range(0, facetCount):
            faceName = nsTmp + ":pCylinder1" + ".f[" + str(j) + "]"
            if j % 2 == 0: #Extrudes every other face
                cmds.polyExtrudeFacet(faceName, ltz=((wheelSize*0.1)/4))

        cmds.rename("wheel1")
    
    cmds.select(nsTmp + ":wheel2")
    cmds.rotate(7.25, rotateY = True)
    cmds.move(((wheelThickness * .5)*.3), moveY= True)

    BOOLEAN(nsTmp, ":wheel1", ":wheel2", 1, "wheel")
    punchHole((wheelSize*.175), (wheelSizeY * 7), 0, 0, 0 , nsTmp, ":wheel", "wheel")

    myShader = cmds.shadingNode('lambert', asShader=True, name="WheelColour")
    cmds.setAttr(nsTmp+":WheelColour.color",rgb[0],rgb[1],rgb[2], typ='double3')

    cmds.select(nsTmp + ":wheel")
    cmds.rename(nsTmp)       
    
    cmds.hyperShade(assign=(nsTmp+":WheelColour"))
    cmds.namespace(removeNamespace=":"+nsTmp,mergeNamespaceWithParent=True)

    cmds.polyUnite(nsTmp, "Hub" + str(nextBlockId - 1))
    cmds.delete(ch = True)
    cmds.rename(nsTmp)
    cmds.xform(cp = True)

#creates the individaual namespacecs
def createNamespace(nsTmp):
    cmds.select(clear=True)
    cmds.namespace(set=":")
    cmds.namespace(add=nsTmp)
    cmds.namespace(set=nsTmp)

#creates a hub cap that fits into the the wheel
def hubCap(blockID, wSize, wThickness):
    rgb = cmds.colorSliderGrp('hubColour', q=True, rgbValue=True) 
    global nextBlockId

    nsTmp = "Hub" + str(nextBlockId)

    nextBlockId = nextBlockId + 1
    
    createNamespace(nsTmp)

    oRADIUS = wSize * .175
    iRADIUS = wSize * .15
    cRADIUS = (wSize *.1) * 2
    HEIGHT = (wThickness * .1) * 2
    SPACER = wSize * .5 *.1
    SPACERLENGTH = iRADIUS * 2.1

    cmds.polyCylinder(r = oRADIUS, h = HEIGHT, n = "hub")
    cmds.move(HEIGHT/2, moveY = True)

    punchHole(iRADIUS, HEIGHT, 0, 0 , HEIGHT, nsTmp, ":hub", "hub")

    cmds.polyCylinder(r=cRADIUS/3, h = HEIGHT/4)
    cmds.move(HEIGHT/1.8, moveY = True)

    BOOLEAN(nsTmp,":hub", ":pCylinder1", 1, "hub")

    cmds.polyCube(w = SPACER, h = HEIGHT/2, d = SPACERLENGTH)
    cmds.move((HEIGHT/2)/1.3, moveY = True)
    
    cmds.polyCube(w = SPACERLENGTH, h = HEIGHT/2, d = SPACER)
    cmds.move((HEIGHT/2)/1.3 , moveY = True)

    myShader = cmds.shadingNode('lambert', asShader=True, name="hubColour")
    cmds.setAttr(nsTmp+":hubColour.color",rgb[0],rgb[1],rgb[2], typ='double3')

    cmds.polyUnite((nsTmp+":*"), n=nsTmp, ch=False)
    cmds.delete(ch=True)

    cmds.hyperShade(assign=(nsTmp+":hubColour"))
    cmds.namespace(removeNamespace=":"+nsTmp,mergeNamespaceWithParent=True)

#creates the rounded end of the beam and either punches in a
#cross or a hole depending on the specified hole type
def beamEnd(Height, Width, Depth, rad, flatDir, baseX, NSTMP, holeType, name):    
    cmds.polyCylinder(r=(Height*.5), h=Depth, n = "Cyl")
    cmds.move(baseX, (Height*.5), 0)
    cmds.rotate(90, rotateX=True)

    cmds.polyCube(width = (Width *.5), height = Height, depth = Depth, n = "Flat")
    cmds.move(((Width*.25 * flatDir) + baseX), (Height * .5), 0)
    BOOLEAN(NSTMP, ":Cyl", ":Flat", 2, "polySurface1")
    
    cmds.polyCube(width = (Width *.5), height = Height, depth = Depth, n= "Flat2")
    cmds.move(((Width*.25 *flatDir) + baseX), (Height * .5), 0)
    BOOLEAN(NSTMP, ":polySurface1", ":Flat2", 1, "pCube1")

    if holeType == 1:
        punchHole(rad, 2, 90, baseX, (Height * .5), NSTMP, ":pCube1", name)
    elif holeType == 2:
        cmds.polyCube(w = rad*2, h = (rad * .5), d = 2, n = "hori")
        cmds.move(baseX, .4, 0)
        cmds.polyCube(w = rad*.5, h = (rad * 2), d = 2, n = "vert")
        cmds.move(baseX, .4, 0)
        BOOLEAN(NSTMP, ":hori", ":vert", 1, "hole")
        BOOLEAN(NSTMP, ":pCube1", ":hole", 2, name)

#builds the entire beam, can be used for all beam functions
def buildBeam(blockWidth, blockDepth, nsTmp, startHole, endHole, NAME):
    ##The the beams are not spawned with the holes facing up.  They are facing out
    cubeSizeX = .8
    cubeSizeY = .8
    cubeSizeZ = .8/blockDepth
    radius = .25

    for i in range(blockWidth):
        offset = i * cubeSizeX
        if i == 0:
            beamEnd(cubeSizeX, cubeSizeY, cubeSizeZ, radius, 1, offset, nsTmp, startHole, "sec1")
        if i == (blockWidth - 1):
            beamEnd(cubeSizeX, cubeSizeY, cubeSizeZ, radius, -1, offset, nsTmp, endHole, "sec1")
        if i > 0 and i <(blockWidth-1):
            cmds.polyCube(width = cubeSizeX, height = cubeSizeY, depth = cubeSizeZ)
            cmds.move(offset, (cubeSizeY * .5), 0)
            punchHole(radius, 2, 90, offset, (cubeSizeY * .5), nsTmp, ":pCube1", "sec1")

    cmds.polyUnite((nsTmp+":sec*"), n=NAME, ch=False)
    cmds.delete(ch=True)

#preforms a boolean between two objects, deletes the history on 
#the merged project, and renames the object
def BOOLEAN(NSTMP, obj1, obj2, OP, RENAME):
    cmds.polyBoolOp( NSTMP + obj1, NSTMP + obj2, op=OP, n = "merge")
    cmds.delete(ch = True)
    cmds.rename(RENAME) 

#punches a cylindrical hole into an object
def punchHole(rad, height, rotX, posX, posY, NSTMP, obj1, name):
    #made the cylinder here instead 
    cmds.polyCylinder(r=rad, h = height )
    cmds.move(posX, moveX=True, a=True)
    cmds.move(posY, moveY=True)
    cmds.rotate(rotX, rotateX=True)

    #punched the hole in the block and renamed it back to pCube1 so that it loop friendly
    BOOLEAN(NSTMP, obj1, ":pCylinder1", 2, name)

 
