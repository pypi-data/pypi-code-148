import sys, os

def loadAnat(sceneDir,volume):
    file=os.path.join(sceneDir,volume+".nii.gz")
    node=None
    if os.path.exists(file):
        try:
            print("SLICERSWANLOADER: Loading "+volume)
            node= slicer.util.loadVolume(file)
        except:
            pass
    return node

def lesionSeg(sceneDir):
    file=os.path.join(sceneDir,"seg_lesions.seg.nrrd")
    if os.path.exists(file):
        print("SLICERSWANLOADER: Loading existing lesion segment")
        slicer.util.loadSegmentation(file)
    else:
        print("SLICERSWANLOADER: Creating lesion segment")
        segNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLSegmentationNode',"seg_lesions")
        segNode.CreateDefaultDisplayNodes()
        segNode.GetSegmentation().AddEmptySegment("Lesion","Lesion",[1,0,0])
        segNode.CreateClosedSurfaceRepresentation()
        myStorageNode = segNode.CreateDefaultStorageNode()
        myStorageNode.SetFileName(file)
        myStorageNode.WriteData(segNode)

def loadFSSurf(sceneDir,nodeName,refNode):
    file=os.path.join(sceneDir,nodeName)
    if os.path.exists(file):
        try:
            print("SLICERSWANLOADER: Loading surface "+nodeName)
            surfNode = slicer.util.loadNodeFromFile(file, 'FreeSurferModelFile', {"referenceVolumeID":refNode.GetID()})
            surfNode.GetDisplayNode().SetColor(0.82,0.82,0.82)
            return surfNode
        except:
            pass
    return None

def loadFSOverlay(sceneDir,nodeName,surfNode):
    file=os.path.join(sceneDir,nodeName)
    if os.path.exists(file):
        try:
            print("SLICERSWANLOADER: Loading surface overlay "+nodeName)
            overlayNode = slicer.util.loadNodeFromFile(file, 'FreeSurferScalarOverlayFile', {"modelNodeId":surfNode.GetID()})
            overlayNode.GetDisplayNode().SetAndObserveColorNodeID('vtkMRMLColorTableNodeFileColdToHotRainbow.txt')
            overlayNode.GetDisplayNode().SetScalarVisibility(False)
        except:
            pass


def loadFSSegmentationFile(segFile):
    if os.path.exists(segFile):
        try:
            slicer.util.loadNodeFromFile(segFile, 'FreeSurferSegmentationFile')
        except:
            pass

def loadFS(sceneDir,refNode):
    segList=["r-aparc_aseg.mgz","segmentHA/lh.hippoAmygLabels.mgz","segmentHA/rh.hippoAmygLabels.mgz"]
    for file in segList:
        segFile=os.path.join(sceneDir,file)
        loadFSSegmentationFile(segFile)

    lh_pial=loadFSSurf(sceneDir,"lh.pial",refNode)
    rh_pial=loadFSSurf(sceneDir,"rh.pial",refNode)

    surfs=["lh.white","rh.white"]
    for surf in surfs:
        loadFSSurf(sceneDir,surf,refNode)

    overlays=['pet_surf','petAI_surf','petZscore_surf','asl_surf','aslAI_surf','aslZscore_surf']
    for overlay in overlays:
        loadFSOverlay(sceneDir,overlay+"_lh.mgz",lh_pial)
        loadFSOverlay(sceneDir,overlay+"_rh.mgz",rh_pial)


def loadVein(sceneDir):
    veinVolumeName="r-venosa_inskull"
    veinNode = loadAnat(sceneDir,veinVolumeName)
    if veinNode==None: return
    print("SLICERSWANLOADER: Creating 3D model: Veins")
    parameters = {}
    parameters["InputVolume"] = veinNode.GetID()
    parameters["Threshold"] = 80
    veinModel = slicer.vtkMRMLModelNode()
    slicer.mrmlScene.AddNode( veinModel )
    parameters["OutputGeometry"] = veinModel.GetID()
    grayMaker = slicer.modules.grayscalemodelmaker
    slicer.cli.runSync(grayMaker, None, parameters)
    veinModel.GetDisplayNode().SetColor(0,0,1)
    veinModel.SetName("Veins")
    myStorageNode = veinModel.CreateDefaultStorageNode()
    myStorageNode.SetFileName(os.path.join(sceneDir,"veins.vtk"))
    myStorageNode.WriteData(veinModel)
    slicer.mrmlScene.RemoveNode(veinNode)

def tractModel(segmentationNode,dtiDir,tract,side):
    tractFile=os.path.join(dtiDir,"r-"+tract['name']+"_"+side+".nii.gz")
    if not os.path.exists(tractFile): return

    tractNode = slicer.util.loadVolume(tractFile)
    segmentationNode.SetReferenceImageGeometryParameterFromVolumeNode(tractNode)

    # Create temporary segment editor to get access to effects
    segmentEditorWidget = slicer.qMRMLSegmentEditorWidget()
    segmentEditorWidget.setMRMLScene(slicer.mrmlScene)
    segmentEditorNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentEditorNode")
    segmentEditorWidget.setMRMLSegmentEditorNode(segmentEditorNode)
    segmentEditorWidget.setSegmentationNode(segmentationNode)
    segmentEditorWidget.setMasterVolumeNode(tractNode)

    # Create segment
    tractSegmentID = segmentationNode.GetSegmentation().AddEmptySegment(tract['name'],tract['name'],tract['color'])
    segmentEditorNode.SetSelectedSegmentID(tractSegmentID)
    # Fill by thresholding
    segmentEditorWidget.setActiveEffectByName("Threshold")
    effect = segmentEditorWidget.activeEffect()
    effect.setParameter("MinimumThreshold",tract['thr'])
    effect.self().onApply()
    #slicer.cli.runSync(effect.self().onApply, None, None, delete_temporary_files=True)

    # Delete temporary segment editor
    segmentEditorWidget = None
    slicer.mrmlScene.RemoveNode(segmentEditorNode)
    slicer.mrmlScene.RemoveNode(tractNode)

def mainTract(dtiDir,sceneDir):
    sides=["rh","lh"]
    tracts = [
      {"name":"cst", "thr":"500", "color":[0,1,0]},
      {"name":"af", "thr":"1500", "color":[1,0,1]},
      {"name":"or", "thr":"500", "color":[1,1,0]}
    ]

    print("SLICERSWANLOADER: Creating DTI tracts 3D models (some minutes!)")

    for side in sides:
        # Create segmentation
        segmentationNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentationNode","tracts_"+side)
        segmentationNode.CreateDefaultDisplayNodes() # only needed for display
        for tract in tracts:
            tractModel(segmentationNode,dtiDir,tract,side)
        segmentationNode.CreateClosedSurfaceRepresentation()
        myStorageNode = segmentationNode.CreateDefaultStorageNode()
        myStorageNode.SetFileName(os.path.join(sceneDir,"tracts_"+side+".seg.nrrd"))
        myStorageNode.WriteData(segmentationNode)




slicer.mrmlScene.Clear(0)
sceneDir=os.path.join(os.getcwd(),"scene")

if not os.path.isdir(sceneDir):
    print("SLICERSWANLOADER: Results folder not found")
else:
    refNode=loadAnat(sceneDir,"ref")
    if refNode!=None:

        dtiDir=os.path.join(sceneDir,"dti")
        if os.path.isdir(dtiDir):
            mainTract(dtiDir,sceneDir)

        lesionSeg(sceneDir)

        baseList=['ref_brain','r-flair_brain','r-mdc_brain','r-pet_brain_smooth',
                  'r-pet_brain_AI','r-pet_brain_z','r-asl','r-asl_AI','r-asl_brain_z','r-FA',
                  'r-flair2d_tra_brain','r-flair2d_cor_brain','r-flair2d_sag_brain']

        for volume in baseList:
            loadAnat(sceneDir,volume)

        loadVein(sceneDir)

        loadFS(sceneDir,refNode)

        print("SLICERSWANLOADER: Saving multimodale scene (some minutes)")
        slicer.util.saveScene(os.path.join(sceneDir,"scene.mrb"))

sys.exit(0)
