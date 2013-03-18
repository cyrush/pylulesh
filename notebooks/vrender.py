db  = Argv()[0]
var = Argv()[1]
f   = Argv()[2]
from visit_utils import *
OpenDatabase(db)
AddPlot("Mesh","Mixed")
AddPlot("Pseudocolor",var)
DrawPlots()
vs = query("MinMax")
pa = PseudocolorAttributes()
pa.minFlag = 1
pa.maxFlag = 1
pa.min = vs[0] - vs[0] * .01
pa.max = vs[1] + vs[1] * .01
SetPlotOptions(pa)
v = GetView3D()
v.viewNormal = (-0.717679, 0.420023, -0.555443)
v.focus = (0.5625, 0.5625, 0.5625)
v.viewUp = (0.340422, 0.90743, 0.24634)
v.viewAngle = 30
v.parallelScale = 0.974279
v.nearPlane = -1.94856
v.farPlane = 1.94856
v.imagePan = (0, 0)
v.imageZoom = 1
v.perspective = 1
v.eyeAngle = 2
v.centerOfRotationSet = 0
v.centerOfRotation = (0.5625, 0.5625, 0.5625)
v.axis3DScaleFlag = 0
v.axis3DScales = (1, 1, 1)
v.shear = (0, 0, 1)
SetView3D(v)
swa = SaveWindowAttributes()
swa.width = 2000
swa.height = 2000
swa.family = 0
swa.fileName = f
SetSaveWindowAttributes(swa)
SaveWindow()
os.system("convert -resize 500x500 %s %s" % (f,f))
sys.exit()
