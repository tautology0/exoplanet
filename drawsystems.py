from matplotlib import pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.patches import Rectangle
import matplotlib.lines as lines
import matplotlib.patches as mpatches
import pyvo
import math

class Planet:
	def __init__(self, name, axes, period, radius):
		self.name=name
		self.axes=axes
		self.period=period
		self.radius=radius
		
	def __str__(self):
		return str(self.__class__) + ": " + str(self.__dict__)
		
class System:
	def __init__(self, name, planets=None, epaname=None):
		self.name=name
		self.epaname=epaname
		print(f"Adding system {self.name}")
		
		if name == "Sol":
			self.planets=[
			   Planet("Mercury", 0.467, 88, 0.035),	Planet("Venus", 0.723, 225, 0.087),
			   Planet("Earth", 1, 365, 0.091),		 Planet("Mars", 1.523, 687, 0.048),
			   Planet("Jupiter", 5.204, 4333, 1),	  Planet("Saturn", 9.583, 10759, 0.833),
			   Planet("Uranus", 19.191, 30687, 0.363), Planet("Neptune", 30.07, 60190, 0.352)
			]
			return
	   
		if planets is not None:
			self.planets=planets
			return
		
		# Download the planet data from the Exoplanet archive
		self.planets=getsystemdata(self.name, epaname=epaname)
			
	def smallest(self, attribute):
		return min(getattr(planet, attribute) for planet in self.planets)
	
	def largest(self, attribute):
		return max(getattr(planet, attribute) for planet in self.planets)


def getsystemdata(name, epaname=None):
	def search_epa(name, value, key):
		if math.isnan(value):
			for r in eparesults:
				if r['pl_name'] == name: return r[key]
		return value
			
	if epaname == None: epaname=name
	service=pyvo.dal.TAPService("https://exoplanetarchive.ipac.caltech.edu/TAP")
	eparesults=service.search(f"select pl_name, pl_radj, pl_orbper, pl_orbsmax from pscomppars where hostname = '{epaname}' ")
	
	service=pyvo.dal.TAPService("http://voparis-tap-planeto.obspm.fr/tap")
	eeuresults=service.search(f"select target_name, radius, period, semi_major_axis from exoplanet.epn_core where star_name = '{name}'")
	
	planets=[]
	for result in eeuresults:
		name=result['target_name']
		axes=search_epa(name, result['semi_major_axis'], 'pl_orbsmax')
		period=search_epa(name, result['period'], 'pl_orbper')
		radius=search_epa(name, result['radius'], 'pl_radj')

		planets.append(Planet(name.split(' ')[-1], axes, period, radius))

	return planets
			
def plotsystem(system, y, scalefactor, plotheight):
	period=list(planet.period for planet in system.planets)
	radius=list(planet.radius for planet in system.planets)
	names =list(planet.name for planet in system.planets)
	
	# This is a hack to make life easier
	yvals =[y] * len(period)
	
	# Assign a colour depending on planet type
	cols  =[]
	for z in radius:
		col='red'
		if   z<0.09: col='grey'
		elif z<0.16: col='green'
		elif z<0.55: col='blue'
		cols.append(col)
	
	# draw system boundaries and label it
	ax.text(xstart*1.1, y+0.035, system.name, fontsize="x-large")
	ax.add_artist(lines.Line2D([xstart,xend], [y], color="lightgrey"))
	ax.add_artist(lines.Line2D([xstart,xend], [y-plotheight/2], color="grey"))

	# Plot the system
	ax.scatter(period, yvals, marker='o', s=[r*scalefactor for r in radius], c=cols, zorder=10, edgecolors='black')
	
	# Label each planet
	for period, y, name in zip(period, yvals, names):
		ax.text(period, y-0.030, name, horizontalalignment="center") 

def addlegend(plt):
	terrestrial = mpatches.Patch(color='grey', label='Terrestrial')
	earth = mpatches.Patch(color='green', label='Super-Earth')
	neptunian = mpatches.Patch(color='blue', label='Neptunian')
	jovian = mpatches.Patch(color='red', label='Jovian')
	legend = plt.legend(handles=[terrestrial, earth, neptunian, jovian], loc='center right', prop={'size':25}, frameon=False)

# Thanks to matplotlib working in archaic units, come on it's the 3rd millennium there's no
# reason to ever use inches
px=1/plt.rcParams['figure.dpi']
plotheight=0.10

# targets is a list of systems to plot, if the contents are a string then it's the name of the system
# sometimes exoplanet archive has a different name, in this case, use a tuple of ("exoplanet.eu", "exoplanet archive")
targets=["Sol",("Kepler-90", "KOI-351"), "Kepler-33", "HD 10180",
		 "HIP 41378", "HD 191939", "HD 34445", "K2-138", "TRAPPIST-1" ]

systems=[]
for target in targets:
	if type(target) is str: 
		systems.append(System(target))
	else:
		systems.append(System(target[0], epaname=target[1]))

smallest=min(system.smallest("period") for system in systems)
largest=max(system.largest("period") for system in systems)
xstart=smallest-1
# Making it a 1/3rd again ensures Neptune isn't clipped
xend=largest*(3/2)

fig, ax = plt.subplots(figsize=(2000*px, len(systems)*220*px))

# set up axes
ax.yaxis.set_visible(False)
ax.xaxis.tick_bottom()
ax.set_xlabel("Orbital Period / days", fontsize='xx-large')
ax.xaxis.set_label_position('bottom') 

# Generic plot configuration
fig.set_facecolor('white')
plt.xscale('log')
plt.tight_layout(pad=0.05)
plt.ylim((-plotheight*(len(systems)-1))-(plotheight), 0)
plt.xlim(xstart, xend)
plt.rcParams.update({'font.size': 18})

y=-plotheight/2
for system in systems:
	print(f"Plotting system {system.name}")
	plotsystem(system, y, 3500, plotheight)
	y -= plotheight

addlegend(plt)

plt.savefig('systems.png', bbox_inches='tight')