from pywht import WhtProject

whtProject = WhtProject("/path/to/wht/project/folder")

featureList = ["", "", "", ""]
def train():
	whtProject.discoverFeatures()
	availableFeaturesInfo = whtProject.getHistoricalFeatures(featureList)

def infer():
