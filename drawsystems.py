from matplotlib import pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.patches import Rectangle
import matplotlib.lines as lines

class Planet:
    def __init__(self, name, axis, radius):
        self.name=name
        self.axis=axis
        self.radius=radius
        
class System:
    def __init__(self, name, planets):
        self.name=name
        self.planets=planets
        
def addsystem(system, y):
    axis  =list(x.axis for x in system.planets)
    radius=list(x.radius*4000 for x in system.planets)
    names =list(x.name for x in system.planets)
    yvals =[y] * len(axis)
    cols  =[]
    
    ax.text(0.06, y+0.035, system.name, fontsize="x-large")
    ax.add_artist(lines.Line2D([0.05,40], [y], color="lightgrey"))
    ax.add_artist(lines.Line2D([0.05,40], [y-offh], color="grey"))
    for z in radius:
        col='red'
        if   z<0.09*4000: col='grey'
        elif z<0.16*4000: col='green'
        elif z<0.55*4000: col='blue'
        cols.append(col)
    #ax.scatter(axis, yvals, marker="None")
    ax.scatter(axis, yvals, marker='o', s=radius, c=cols, zorder=10)
    for x, y, z, n in zip(axis, yvals, radius, names):
        image=jovian
        if   z<0.09: image=terrestial
        elif z<0.16: image=superearth
        elif z<0.55: image=neptunian
        #ab=AnnotationBbox(OffsetImage(image, zoom=z*0.6), (x,y), frameon=False)
        #ax.add_artist(ab)
        #ax.plot(x,y, marker='o')
        ax.text(x, y-0.030, n, horizontalalignment="center") 



# Thanks to matplotlib working in archaic units, come on it's the 3rd millennium there's no
# reason to ever use inches
cm=1/2.54
px=1/plt.rcParams['figure.dpi']
plth=0.10
offh=plth/2

# Load images.
terrestrial = plt.imread('images/mercury.png')
superearth = plt.imread('images/earth.png')
neptunian = plt.imread('images/neptune.png')
jovian = plt.imread('images/jupiter.png')

# Data
systems=[]
systems.append(System("Sol",[
               Planet("Mercury", 0.467, 0.035), Planet("Venus", 0.723, 0.087),
               Planet("Earth", 1, 0.091),       Planet("Mars", 1.523, 0.048),
               Planet("Jupiter", 5.204, 1),     Planet("Saturn", 9.583, 0.833),
               Planet("Uranus", 19.191, 0.363), Planet("Neptune", 30.07, 0.352)
            ]))

systems.append(System("Kepler-90",[
               Planet("b", 0.074, 0.117),       Planet("c", 0.089, 0.106),
               Planet("i", 0.2, 0.118),         Planet("d", 0.32, 0.256),
               Planet("e", 0.42, 0.237),        Planet("f", 0.48, 0.257),
               Planet("g", 0.71, 0.723),        Planet("h", 1.01, 1.008)
            ]))

systems.append(System("Kepler-33",[
               Planet("b", 0.0677, 0.115),      Planet("c", 0.1189, 0.285),
               Planet("d", 0.1662, 0.477),      Planet("e", 0.2138, 0.359),
               Planet("f", 0.2535, 0.398)
            ]))

systems.append(System("HIP 41378",[
               Planet("b",0.1283,0.26),        Planet("c",0.2061,0.228),
               Planet("d",0.88,0.353),         Planet("e",1.06,0.4916),
               Planet("f",1.37,0.821)
            ]))

# Create figure
fig, ax = plt.subplots(figsize=(1800*px, len(systems)*220*px))
ax.yaxis.set_visible(False)
ax.xaxis.tick_top()
ax.set_xlabel("Semi-major Axis / AU", fontsize='large')
ax.xaxis.set_label_position('top') 
ax.set_facecolor('white')
fig.set_facecolor('white')
plt.xscale('log')
plt.tight_layout(pad=0.05)
plt.ylim((-plth*(len(systems)-1))-(plth), 0)
plt.xlim(0.055, 40)
plt.rcParams.update({'font.size': 18})

y=-offh
for system in systems:
    addsystem(system, y)
    y -= plth

plt.savefig('images/systems.png', bbox_inches='tight')