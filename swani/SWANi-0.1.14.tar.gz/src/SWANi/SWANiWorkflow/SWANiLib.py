import shutil
from nipype.pipeline.engine import Workflow
from nipype.interfaces.dcm2nii import Dcm2niix, Dcm2niixInputSpec
from nipype.interfaces.base import InputMultiObject
from nipype.interfaces.fsl import  SwapDimensions, BinaryMaths, UnaryMaths, ImageStats, ProbTrackX2, ApplyWarp, BEDPOSTX5, Threshold, ApplyMask, DilateImage
from nipype.interfaces.fsl.dti import BEDPOSTX5InputSpec, ProbTrackX2InputSpec
from nipype import Node, MapNode
from nipype.interfaces.utility import IdentityInterface
from nipype.interfaces.freesurfer import Label2Vol
from os.path import abspath
import os,glob,math
import SWANi_supplement
from nipype.interfaces.fsl.maths import KernelInput
from nipype.interfaces.fsl.base import FSLCommand, FSLCommandInputSpec
from nipype.interfaces.base import (traits, BaseInterface, BaseInterfaceInputSpec,
                                    TraitedSpec, CommandLineInputSpec, CommandLine,
                                    InputMultiPath, File, Directory,
                                    isdefined)
from nipype.interfaces.io import DataSink

#SERVE NEL CONNECT PER ESTRARRE UN FILE DA UNA LISTA DI OUTPUT QUANDO L'INPUT E' SINGOLO (es. aparcaseg di reconAll)
def getn (list,index):
        return list[index]

#QUESTO NODO RESTITUISCE L'ORIENTAMENTO DELLE IMMAGINI (NEUROLOGICAL/radiological)
class OrientInputSpec(FSLCommandInputSpec):
    in_file = File(exists=True, mandatory=True, argstr="%s", position="2", desc="input image")
    _options_xor=['get_orient',"swap_orient"]
    get_orient = traits.Bool(argstr="-getorient", position="1", xor=_options_xor, desc="gets FSL left-right orientation")
    swap_orient = traits.Bool(argstr="-swaporient", position="1", xor=_options_xor, desc="swaps FSL radiological and FSL neurological")

class OrientOutputSpec(TraitedSpec):
    out_file = File(exists=True, desc="image with modified orientation")
    orient = traits.Str(desc="FSL left-right orientation")

class Orient(FSLCommand):
    _cmd = 'fslorient'
    input_spec = OrientInputSpec
    output_spec = OrientOutputSpec

    def aggregate_outputs(self, runtime=None, needed_outputs=None):
        outputs = self._outputs()
        info = runtime.stdout

        # Modified file
        if isdefined(self.inputs.swap_orient):
            outputs.out_file = self.inputs.in_file

        # Get information
        if isdefined(self.inputs.get_orient):
            outputs.orient = info

        return outputs

#REIMPLEMENTAZIONE DI DCM2NIIX PER RINOMINARE I FILE CROPPATI
class Dcm2niix_moInputSpec(Dcm2niixInputSpec):
    merge_imgs = traits.Enum(
        "2",
        "1",
        "0",
        argstr="-m %s",
        usedefault=True)

class Dcm2niix_mo(Dcm2niix):

    input_spec = Dcm2niix_moInputSpec

    def _run_interface(self, runtime):
        self.inputs.args="-w 1"
        runtime = super(Dcm2niix, self)._run_interface(
            runtime, correct_return_codes=(0, 1)
        )
        self._parse_files(self._parse_stdout(runtime.stdout))
        if len(self.bids)>0:
            os.remove(self.bids[0])
            self.bids=[]
        if self.inputs.crop == True and os.path.exists(self.output_files[0]):
            os.remove(self.output_files[0])
            os.rename(self.output_files[0].replace(".nii.gz","_Crop_1.nii.gz"),self.output_files[0])
        return runtime

#QUESTO NODO CONVERTE LE IMMAGINI IN RADIOLOGICAL E "RL","PA","IS"
class Orient_moInputSpec(BaseInterfaceInputSpec):
    in_file = File(exists=True, mandatory=True, desc='the input image')
    out_file = File(desc='the output image')

class Orient_moOutputSpec(TraitedSpec):
    out_file = File(desc='the output image')

class Orient_mo(BaseInterface):
    input_spec = Orient_moInputSpec
    output_spec = Orient_moOutputSpec

    def _run_interface(self, runtime):
        self.inputs.out_file=self._gen_outfilename()
        shutil.copy(self.inputs.in_file,self.inputs.out_file)
        getOrient=Orient(in_file=self.inputs.out_file)
        getOrient.inputs.get_orient=True
        res=getOrient.run()
        if res.outputs.orient=="NEUROLOGICAL":
            swap_NR=SwapDimensions()
            swap_NR.inputs.in_file=self.inputs.out_file
            swap_NR.inputs.out_file=self.inputs.out_file
            swap_NR.inputs.new_dims=("-x","y","z")
            swap_NR.run()
            swapOrient=Orient(in_file=self.inputs.out_file)
            swapOrient.inputs.swap_orient=True
            swapOrient.run()
        swap_dim=SwapDimensions()
        swap_dim.inputs.in_file=self.inputs.out_file
        swap_dim.inputs.out_file=self.inputs.out_file
        swap_dim.inputs.new_dims=("RL","PA","IS")
        swap_dim.run()

        return runtime

    def _gen_outfilename(self):
        out_file = self.inputs.out_file
        if not isdefined(out_file) and isdefined(self.inputs.in_file):
            out_file = os.path.basename(self.inputs.in_file)
        return abspath(out_file)

    def _list_outputs(self):
        outputs = self.output_spec().get()
        outputs['out_file'] = self._gen_outfilename()
        return outputs

#NODO PER IL CALCOLO GENERICO DI UN ASIMMERY INDEX DATI I DUE FILE INVERTITI
class AIndexInputSpec(BaseInterfaceInputSpec):
    in_file = File(exists=True, mandatory=True, desc='the input image')
    swapped_file = File(exists=True, mandatory=True, desc='the swapped input image')
    out_file = File(desc='the output image')

class AIndexOutputSpec(TraitedSpec):
    out_file = File(desc='the output image')

class AIndex(BaseInterface):
    input_spec = AIndexInputSpec
    output_spec = AIndexOutputSpec

    def _run_interface(self, runtime):
        self.inputs.out_file=self._gen_outfilename()

        add=BinaryMaths()
        add.inputs.in_file=self.inputs.in_file
        add.inputs.operand_file=self.inputs.swapped_file
        add.inputs.operation="add"
        add.inputs.out_file=abspath("add_"+os.path.basename(self.inputs.in_file))
        add_res=add.run()

        sub=BinaryMaths()
        sub.inputs.in_file=self.inputs.in_file
        sub.inputs.operand_file=self.inputs.swapped_file
        sub.inputs.operation="sub"
        sub.inputs.out_file=abspath("sub_"+os.path.basename(self.inputs.in_file))
        sub_res=sub.run()

        div=BinaryMaths()
        div.inputs.in_file=sub_res.outputs.out_file
        div.inputs.operand_file=add_res.outputs.out_file
        div.inputs.operation="div"
        div.inputs.out_file=self.inputs.out_file
        div.run()

        return runtime

    def _gen_outfilename(self):
        out_file = self.inputs.out_file
        if not isdefined(out_file) and isdefined(self.inputs.in_file):
            out_file = "Aindex_"+os.path.basename(self.inputs.in_file)
        return abspath(out_file)

    def _list_outputs(self):
        outputs = self.output_spec().get()
        outputs['out_file'] = self._gen_outfilename()
        return outputs

#QUESO NODO DISCRIMINA LA FASE VENOSA DA QUELLA MORFOLOGICA DELLA PHASE CONTRAST
class VenosaCheckInputSpec(BaseInterfaceInputSpec):
    in_files=InputMultiObject(File(exists=True), desc="List of splitted file")
    out_file_venosa = File(desc='the output venous image')
    out_file_modulo = File(desc='the output anatomic image')

class VenosaCheckOutputSpec(TraitedSpec):
    out_file_venosa = File(desc='the output venous image')
    out_file_modulo = File(desc='the output anatomic image')

class VenosaCheck(BaseInterface):
    input_spec = VenosaCheckInputSpec
    output_spec = VenosaCheckOutputSpec

    def _run_interface(self, runtime):
        self.inputs.out_file_venosa=abspath("venosa.nii.gz")
        self.inputs.out_file_modulo=abspath("venosa_modulo.nii.gz")
        s0=ImageStats()
        s0.inputs.in_file=self.inputs.in_files[0]
        s0.inputs.op_string="-s"
        res0=s0.run()
        s1=ImageStats()
        s1.inputs.in_file=self.inputs.in_files[1]
        s1.inputs.op_string="-s"
        res1=s1.run()
        if res0.outputs.out_stat < res1.outputs.out_stat:
            shutil.copy(self.inputs.in_files[0], self.inputs.out_file_venosa)
            shutil.copy(self.inputs.in_files[1], self.inputs.out_file_modulo)
        else:
            shutil.copy(self.inputs.in_files[1], self.inputs.out_file_venosa)
            shutil.copy(self.inputs.in_files[0], self.inputs.out_file_modulo)

        return runtime

    def _list_outputs(self):
        outputs = self.output_spec().get()
        outputs['out_file_venosa'] = abspath("venosa.nii.gz")
        outputs['out_file_modulo'] = abspath("venosa_modulo.nii.gz")
        return outputs

#IMPLEMENTAZIONE DI PROBRACKX2 IN PARALLELO - DA COMPLETARE
def create_probtrackx2_pipeline(name,tract_name,resultDir):

    inputnode = Node(
        IdentityInterface(fields=['xfm', 'inv_xfm', 'fsamples', 'mask', 'phsamples', 'thsamples', 'mni2ref_warp', 'ref']),
        name='inputnode')

    out_fields = ['fdt_paths_rh', 'fdt_paths_lh', 'fdt_paths_normalized_rh', 'fdt_paths_normalized_lh']

    outputnode = Node(
        IdentityInterface(fields=out_fields), name='outputnode')

    wf = Workflow_mo(name=name)

    sides=["lh","rh"]

    track_loop={}
    warp_loop={}
    norm_loop={}

    #GENERO I RANDOM SEED COME NODO ALTRIMENTI OGNI ESECUZIONE CAMBIA LA CACHE DEL WORKFLOW
    randomSeed = Node(randomSeedGenerator(),name='randomSeed')
    randomSeed.inputs.seeds_n=5

    wf.connect(inputnode, "mask", randomSeed, "mask")

    for side in sides:
        track_loop[side]=[None] * 5
        protocol_dir = os.path.join(SWANi_supplement.protocol_dir,tract_name+"_"+side)

        track_loop[side] = MapNode(ProbTrackX2_mo(),name="%s_track_loop_%s"%(tract_name,side),iterfield=["rseed"])
        track_loop[side].inputs.seed = os.path.join(protocol_dir,"seed.nii.gz")
        track_loop[side].inputs.onewaycondition = True
        track_loop[side].inputs.n_samples = 100
        track_loop[side].inputs.loop_check = True
        track_loop[side].inputs.avoid_mp = os.path.join(protocol_dir,"exclude.nii.gz")
        track_loop[side].inputs.waypoints = os.path.join(protocol_dir,"target.nii.gz")
        sumTrack = Node(sumMultiTracks(),name='sumTrack_%s'%(side))
        warp_loop[side] = Node(ApplyWarp(), name='%s_warp_%s'%(tract_name,side))
        warp_loop[side].inputs.out_file = "r-%s_%s.nii.gz"%(tract_name,side)
        norm_loop[side] = Node(BinaryMaths(), name='%s_norm_%s'%(tract_name,side))
        norm_loop[side].inputs.operation = "div"
        norm_loop[side].inputs.out_file = "r-%s_normalized_%s.nii.gz"%(tract_name,side)

        wf.connect(inputnode, "fsamples", track_loop[side], "fsamples")
        wf.connect(inputnode, "mask", track_loop[side], "mask")
        wf.connect(inputnode, "phsamples", track_loop[side], "phsamples")
        wf.connect(inputnode, "thsamples", track_loop[side], "thsamples")
        wf.connect(inputnode, "xfm", track_loop[side], "xfm")
        wf.connect(inputnode, "inv_xfm", track_loop[side], "inv_xfm")
        wf.connect(randomSeed, "seeds", track_loop[side], "rseed")
        wf.connect(track_loop[side], "fdt_paths", sumTrack, "path_files")
        wf.connect(track_loop[side], "way_total", sumTrack, "waytotal_files")
        wf.connect(inputnode, "ref", warp_loop[side], "ref_file")
        wf.connect(sumTrack, "out_file", warp_loop[side], "in_file")
        wf.connect(inputnode, "mni2ref_warp", warp_loop[side], "field_file")
        wf.connect(warp_loop[side], "out_file", outputnode, "fdt_paths_%s"%(side))
        wf.connect(warp_loop[side], "out_file", norm_loop[side], "in_file")
        wf.connect(sumTrack, "waytotal_sum", norm_loop[side], "operand_value")
        wf.connect(norm_loop[side], "out_file", outputnode, "fdt_paths_normalized_%s"%(side))

        wf.sink_result(resultDir,warp_loop[side],'out_file','scene.dti')
        wf.sink_result(resultDir,norm_loop[side],'out_file','scene.dti')

    return wf


#IMPLEMENTAZIONE DI SEGMENT_HA
class segmentHA_moInputSpec(CommandLineInputSpec):
    subject_id = traits.Str(
        "recon_all", mandatory=True, position=0, argstr="%s", desc="subject name", usedefault=True
    )
    subjects_dir = Directory(
        exists=True,
        mandatory=True,
        position=1,
        argstr="%s",
        hash_files=False,
        desc="path to subjects directory",
        genfile=True,
    )
    num_threads = traits.Int(argstr="")

class segmentHA_moOutputSpec(TraitedSpec):
    #lh_hippoSfVolumes = File(desc="Estimated volumes of the hippocampal substructures and of the whole hippocampus")
    #lh_amygNucVolumes = File(desc="Estimated volumes of the nuclei of the amygdala and of the whole amygdala")
    lh_hippoAmygLabels = File(desc="Discrete segmentation volumes at subvoxel resolution")
    #lh_hippoAmygLabels_hierarchy = File(desc="Segmentations with the different hierarchy levels")
    #rh_hippoSfVolumes = File(desc="Estimated volumes of the hippocampal substructures and of the whole hippocampus")
    #rh_amygNucVolumes = File(desc="Estimated volumes of the nuclei of the amygdala and of the whole amygdala")
    rh_hippoAmygLabels = File(desc="Discrete segmentation volumes at subvoxel resolution")
    #rh_hippoAmygLabels_hierarchy = File(desc="Segmentations with the different hierarchy levels")


class segmentHA_mo(CommandLine):
    _cmd = 'segmentHA_T1.sh'
    input_spec = segmentHA_moInputSpec
    output_spec = segmentHA_moOutputSpec

    def _list_outputs(self):
        base=os.path.join(self.inputs.subjects_dir,self.inputs.subject_id,"mri")
        lh=''
        rh=''

        src=glob.glob(os.path.abspath(os.path.join(base,"lh.hippoAmygLabels-T1.v[0-9][0-9].mgz")))
        if len(src)==1:
            lh=src[0]

        src=glob.glob(os.path.abspath(os.path.join(base,"rh.hippoAmygLabels-T1.v[0-9][0-9].mgz")))
        if len(src)==1:
            rh=src[0]


        # Get the attribute saved during _run_interface
        # return {'lh_hippoSfVolumes':abspath(os.path.join(base,"lh.hippoSfVolumes-T1.v21.txt:")),
        #         'rh_hippoSfVolumes':abspath(os.path.join(base,"lh.hippoSfVolumes-T1.v21.txt:")),
        #         'lh_amygNucVolumes':abspath(os.path.join(base,"lh.amygNucVolumes-T1.v21.txt")),
        #         'rh_amygNucVolumes':abspath(os.path.join(base,"rh.amygNucVolumes-T1.v21.txt")),
        #         'lh_hippoAmygLabels':abspath(os.path.join(base,"lh.hippoAmygLabels-T1.v21.mgz")),
        #         'rh_hippoAmygLabels':abspath(os.path.join(base,"/rh.hippoAmygLabels-T1.v21.mgz")),
        #         'lh_hippoAmygLabels_hierarchy':abspath(os.path.join(base,"lh.hippoAmygLabels-T1.v21.[hierarchy].mgz")),
        #         'rh_hippoAmygLabels_hierarchy':abspath(os.path.join(base,"rh.hippoAmygLabels-T1.v21.[hierarchy].mgz"))
        #         }

        return {
                'lh_hippoAmygLabels':lh,
                'rh_hippoAmygLabels':rh
                }

    def _parse_inputs(self, skip=None):
        #ABILITO LA VARIABILE PER IL MULTITHREAD E IGNORO L'INPUT
        if isdefined(self.inputs.num_threads):
            skip=["num_threads"]
            self.inputs.environ["ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS"] = "%d" % self.inputs.num_threads

        parse = super(segmentHA_mo, self)._parse_inputs(skip)

        #se è rimasto il file di lock da precedente esecuzione, lo cancello
        exPath=abspath(os.path.join(self.inputs.subjects_dir,self.inputs.subject_id,"scripts/IsRunningHPsubT1.lh+rh"))

        if os.path.exists(exPath):
                os.remove(exPath)

        return parse

#REIMPLEMENTAZIONE DI BEDPOSTX PER IGNORARE STDERR E GESTIRE MULTITHREAD
class BEDPOSTX5_moInputSpec(BEDPOSTX5InputSpec):
    num_threads = traits.Int(argstr="")

class BEDPOSTX5_mo(BEDPOSTX5):
    input_spec = BEDPOSTX5_moInputSpec

    def _run_interface(self, runtime):
        from nipype.utils.filemanip import split_filename,copyfile
        from nipype.interfaces.fsl.dti import FSLXCommand
        subjectdir = abspath(self.inputs.out_dir)
        if not os.path.exists(subjectdir):
            os.makedirs(subjectdir)
        _, _, ext = split_filename(self.inputs.mask)
        copyfile(self.inputs.mask, os.path.join(subjectdir, "nodif_brain_mask" + ext))
        _, _, ext = split_filename(self.inputs.dwi)
        copyfile(self.inputs.dwi, os.path.join(subjectdir, "data" + ext))
        copyfile(self.inputs.bvals, os.path.join(subjectdir, "bvals"))
        copyfile(self.inputs.bvecs, os.path.join(subjectdir, "bvecs"))
        if isdefined(self.inputs.grad_dev):
            _, _, ext = split_filename(self.inputs.grad_dev)
            copyfile(self.inputs.grad_dev, os.path.join(subjectdir, "grad_dev" + ext))


        self._out_dir = os.getcwd()
        retval = super(FSLXCommand, self)._run_interface(runtime)


        self._out_dir = subjectdir + ".bedpostX"
        return retval

    def _parse_inputs(self, skip=None):
        #ABILITO LA VARIABILE PER IL MULTITHREAD E IGNORO L'INPUT
        if isdefined(self.inputs.num_threads):
            skip=["num_threads"]
            self.inputs.environ["FSLPARALLEL"] = "%d" % self.inputs.num_threads

        parse = super(BEDPOSTX5_mo, self)._parse_inputs(skip)
        return parse

class ProbTrackX2_moInputSpec(ProbTrackX2InputSpec):
    rseed = traits.Int(argstr="--rseed=%s", desc="random seed")

class ProbTrackX2_mo(ProbTrackX2):
    input_spec = ProbTrackX2_moInputSpec

#NODO PER KERNEL PIU' GENERICO
class DilateImage_mo(DilateImage):
    input_spec=KernelInput

#NODO PER ESTRARRE UNA ROI DA UNA SEGMENTAZIONE CON UN DATO VALORE
class thrROIInputSpec(BaseInterfaceInputSpec):
    in_file = File(exists=True, mandatory=True, desc='the input image')
    seg_val_min = traits.Float(mandatory=True, desc='the min value of interested segmentation')
    seg_val_max = traits.Float(mandatory=True, desc='the max value of interested segmentation')
    out_file = File(desc='the output image')

class thrROIOutputSpec(TraitedSpec):
    out_file = File(desc='the output image')

class thrROI(BaseInterface):
    input_spec = thrROIInputSpec
    output_spec = thrROIOutputSpec

    def _run_interface(self, runtime):
        self.inputs.out_file=self._gen_outfilename()

        below=Threshold()
        below.inputs.in_file=self.inputs.in_file
        below.inputs.direction="below"
        below.inputs.thresh=self.inputs.seg_val_min
        below.inputs.out_file=abspath("below_"+os.path.basename(self.inputs.in_file))
        below_res=below.run()

        above=Threshold()
        above.inputs.in_file=below_res.outputs.out_file
        above.inputs.direction="above"
        above.inputs.thresh=self.inputs.seg_val_max
        above.inputs.out_file=abspath("above_"+os.path.basename(self.inputs.in_file))
        above_res=above.run()

        bin=UnaryMaths()
        bin.inputs.in_file=above_res.outputs.out_file
        bin.inputs.operation="bin"
        bin.inputs.out_file=self.inputs.out_file
        bin.run()

        return runtime

    def _gen_outfilename(self):
        out_file = self.inputs.out_file
        if not isdefined(out_file) and isdefined(self.inputs.in_file):
            out_file = "ROI_"+str(self.inputs.seg_val_min)+"_"+str(self.inputs.seg_val_min)+"_"+os.path.basename(self.inputs.in_file)
        return abspath(out_file)

    def _list_outputs(self):
        outputs = self.output_spec().get()
        outputs['out_file'] = self._gen_outfilename()
        return outputs

#NODO PER CALCOLARE Z SCORE DA ROI
class ZscoreInputSpec(BaseInterfaceInputSpec):
    in_file = File(exists=True, mandatory=True, desc='the input image')
    ROI_file = File(exists=True, mandatory=True, desc='the input image')
    out_file = File(desc='the output image')

class ZscoreOutputSpec(TraitedSpec):
    out_file = File(exists=True, desc='the output image')

class Zscore(BaseInterface):
    input_spec = ZscoreInputSpec
    output_spec = ZscoreOutputSpec

    def _run_interface(self, runtime):
        self.inputs.out_file=self._gen_outfilename()

        mask=ApplyMask()
        mask.inputs.in_file=self.inputs.in_file
        mask.inputs.mask_file=self.inputs.ROI_file
        mask.inputs.out_file=abspath("mask_"+os.path.basename(self.inputs.in_file))
        res_mask=mask.run()

        mean=ImageStats()
        mean.inputs.in_file=res_mask.outputs.out_file
        mean.inputs.op_string="-M"
        mean_res=mean.run()

        sd=ImageStats()
        sd.inputs.in_file=res_mask.outputs.out_file
        sd.inputs.op_string="-S"
        sd_res=sd.run()

        sub=BinaryMaths()
        sub.inputs.in_file=self.inputs.in_file
        sub.inputs.operation="sub"
        sub.inputs.operand_value=mean_res.outputs.out_stat
        sub_res=sub.run()

        div=BinaryMaths()
        div.inputs.in_file=sub_res.outputs.out_file
        div.inputs.operation="div"
        div.inputs.operand_value=sd_res.outputs.out_stat
        div.inputs.out_file=self.inputs.out_file
        div.run()

        return runtime

    def _gen_outfilename(self):
        out_file = self.inputs.out_file
        if not isdefined(out_file) and isdefined(self.inputs.in_file):
            out_file = "zscore_"+os.path.basename(self.inputs.in_file)
        return abspath(out_file)

    def _list_outputs(self):
        outputs = self.output_spec().get()
        outputs['out_file'] = self._gen_outfilename()
        return outputs

#QUESO NODO GENERA UNA LISTA DI SEED RANDOM
class randomSeedGeneratorInputSpec(BaseInterfaceInputSpec):
    seeds_n=traits.Int(mandatory=True, desc="The number of needed seeds")
    mask=File(mandatory=True, exists=True, desc="Just for depend")

class randomSeedGeneratorOutputSpec(TraitedSpec):
    seeds = traits.List(desc='the list of seeds')

class randomSeedGenerator(BaseInterface):
    input_spec = randomSeedGeneratorInputSpec
    output_spec = randomSeedGeneratorOutputSpec
    seedlist =[]

    def _run_interface(self, runtime):
        from random import randrange
        for x in range(self.inputs.seeds_n):
            self.seedlist.append(randrange(1000))


    def _list_outputs(self):
        outputs = self.output_spec().get()
        outputs['seeds'] = self.seedlist
        return outputs

#nodo per rimozione outliers nel DOmap
class DOmap_outliers_mask_moInputSpec(BaseInterfaceInputSpec):
    in_file=File(exists=True, mandatory=True, desc='the input image')
    mask_file=File(exists=True, mandatory=True, desc='the original mask image')
    out_file = File(desc='the output mask name')

class DOmap_outliers_mask_moOutputSpec(TraitedSpec):
    out_file = File(exists=True, desc='the output image')

class DOmap_outliers_mask_mo(BaseInterface):
    input_spec = DOmap_outliers_mask_moInputSpec
    output_spec = DOmap_outliers_mask_moOutputSpec

    def _run_interface(self, runtime):
        self.inputs.out_file=self._gen_outfilename()

        mean=ImageStats()
        mean.inputs.in_file=self.inputs.in_file
        mean.inputs.op_string="-M"
        mean_res=mean.run()

        meanValue=math.trunc(mean_res.outputs.out_stat)

        if meanValue<=100:
            threshold=meanValue+1
            thr=Threshold()
            thr.inputs.in_file=self.inputs.in_file
            thr.inputs.thresh=threshold
            thr_res=thr.run()

            bin=UnaryMaths()
            bin.inputs.in_file=thr_res.outputs.out_file
            bin.inputs.operation="bin"
            bin_res=bin.run()

            sub=BinaryMaths()
            sub.inputs.in_file=self.inputs.mask_file
            sub.inputs.operation="sub"
            sub.inputs.operand_file=bin_res.outputs.out_file
            sub.inputs.out_file=self.inputs.out_file
            sub_res=sub.run()
        else:
            shutil.copy(self.inputs.mask_file,self.inputs.out_file)

        return runtime

    def _gen_outfilename(self):
        out_file = self.inputs.out_file
        if not isdefined(out_file):
            out_file = "brain_cortex_mas_refined.nii.gz"
        return abspath(out_file)

    def _list_outputs(self):
        outputs = self.output_spec().get()
        outputs['out_file'] = self._gen_outfilename()
        return outputs


#SOMMA UNA LISTA DI VOLUMI
class sumMultiTracksInputSpec(BaseInterfaceInputSpec):
    path_files= InputMultiPath(File(exists=True), mandatory=True, desc="list of path file to sum togheter")
    waytotal_files= InputMultiPath(File(exists=True), mandatory=True, desc="list of waytotal files to sum togheter")
    out_file = File(desc='the output image')

class sumMultiTracksOutputSpec(TraitedSpec):
    out_file = File(exists=True, desc='the output image')
    waytotal_sum = traits.Int()

class sumMultiTracks(BaseInterface):
    input_spec = sumMultiTracksInputSpec
    output_spec = sumMultiTracksOutputSpec

    def _run_interface(self, runtime):
        self.inputs.out_file=self._gen_outfilename()

        steps=len(self.inputs.path_files)-1
        sum=[None] * steps
        sum_res=[None] * steps

        self.waytotal_sum=0

        for x in range(steps):

            #SUM FTP_PATHS
            sum[x] = BinaryMaths()
            sum[x].inputs.operation="add"

            if x==0:
                sum[x].inputs.in_file=self.inputs.path_files[x]
            else:
                sum[x].inputs.in_file=sum_res[(x-1)].outputs.out_file

            sum[x].inputs.operand_file=self.inputs.path_files[(x+1)]

            if x==(steps-1):
                sum[x].inputs.out_file=self.inputs.out_file

            sum_res[x]=sum[x].run()

            #SUM WAYTOTAL
            if os.path.exists(self.inputs.waytotal_files[x]):
                with open(self.inputs.waytotal_files[x], 'r') as file:
                    for line in file.readlines():
                        self.waytotal_sum+=int(line)

        return runtime

    def _gen_outfilename(self):
        out_file = self.inputs.out_file
        if not isdefined(out_file):
            out_file = "sum.nii.gz"
        return abspath(out_file)

    def _list_outputs(self):
        outputs = self.output_spec().get()
        outputs['out_file'] = self._gen_outfilename()
        outputs['waytotal_sum'] = self.waytotal_sum
        return outputs


class Label2Vol_mo(Label2Vol):

        def _list_outputs(self):
            outputs=super(Label2Vol_mo, self)._list_outputs()
            outputs["vol_label_file"] = abspath(outputs["vol_label_file"])
            return outputs


class Workflow_mo(Workflow):
    def get_node_array(self):
            """List names of all nodes in a workflow"""
            from  networkx import topological_sort

            outlist = {}
            for node in topological_sort(self._graph):
                if isinstance(node, Workflow):
                    outlist[node.name]=node.get_node_array()
                elif not isinstance(node.interface, IdentityInterface):
                        outlist[node.name]={}
            return outlist

    def sink_result(self,savePath,resultNode,resultName,subfolder,regexp_substitutions=None):

        datasink = Node(DataSink(), name='SaveResults_'+resultNode.name+"_"+resultName.replace(".","_"))
        datasink.inputs.base_directory = savePath

        if regexp_substitutions!=None:
            datasink.inputs.regexp_substitutions=regexp_substitutions

        #self.add_nodes([datasink])

        self.connect(resultNode, resultName, datasink, subfolder)
