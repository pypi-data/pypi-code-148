from nipype.interfaces.fsl import (BET, FLIRT, ConvertXFM, IsotropicSmooth, FNIRT, InvWarp,
                                    ApplyWarp, Split, ApplyMask, ExtractROI, EddyCorrect, DTIFit,
                                    ConvertWarp,BinaryMaths,FAST,ImageStats)
from nipype.interfaces.freesurfer import ReconAll, SampleToSurface
from nipype.interfaces.utility import Merge
from nipype.pipeline.engine import Node
from os.path import abspath
import os

from ..SWANiWorkflow.SWANiLib import (Workflow_mo, create_probtrackx2_pipeline, Dcm2niix_mo,Orient_mo,
                                  SwapDimensions,segmentHA_mo,Label2Vol_mo,thrROI, AIndex, Zscore,
                                  VenosaCheck, BEDPOSTX5_mo, getn, DilateImage_mo, DOmap_outliers_mask_mo)
from multiprocessing import cpu_count

import SWANi_supplement

class SWANi_wf(Workflow_mo):

    def __init__(self, name, base_dir=None):
        super(SWANi_wf,self).__init__(name, base_dir)


    def add_input_folders(self,SWANiGlobalConfig,wfType,check_input,isfreesurfer):

        if not check_input['mr_t13d']:
            return

        isfreesurfer= isfreesurfer and SWANiGlobalConfig.getboolean('MAIN', 'freesurfer')
        isHippoAmygLabels=SWANiGlobalConfig.getboolean('MAIN', 'hippoAmygLabels')
        DOmap = SWANiGlobalConfig.getboolean('MAIN', 'DOmap')
        flair2D = SWANiGlobalConfig.getboolean('OPTIONAL_SERIES', 'mr_flair2d')

        #WFTYPE 0=surgical, 1=EZ
        #wfType=SWANiGlobalConfig.patientConfiguration['ptConfig'].getint('wfType')

        self.max_cpu=SWANiGlobalConfig.getint('MAIN','maxPtCPU')

        if self.max_cpu>0:
            max_node_cpu= max(self.max_cpu/2,1)
        else:
            max_node_cpu= max(int((cpu_count()-2)/2),1)

        #ELABORAZIONE T1 3D
        #coversione dicom->nifti
        ref_dir = os.path.join(self.base_dir,SWANiGlobalConfig['DEFAULTFOLDERS']['default_mr_t13d_folder'])
        ref_conv = Node(Dcm2niix_mo(),name='ref_conv')
        ref_conv.inputs.source_dir=ref_dir
        ref_conv.inputs.crop=True
        ref_conv.inputs.out_filename ="ref"
        #orientamento in convenzione radiologica
        ref_reOrient=Node(Orient_mo(),name='ref_reOrient')
        #rimozione dello scalpo
        ref_BET = Node(BET(),name='ref_BET')
        ref_BET.inputs.frac = 0.5
        ref_BET.inputs.mask = True
        ref_BET.inputs.robust = True
        ref_BET.inputs.threshold = True

        #REGISTRAZIONE AD ALTANTE MNI (SOLO PER I FASCI!)
        if wfType==0 and check_input['mr_dti']:
            #registrazione lineare
            ref2mni_FLIRT = Node(FLIRT(), name='ref2mni_FLIRT')
            mni = abspath(os.path.join(os.environ["FSL_DIR"],'data/standard/MNI152_T1_2mm_brain.nii.gz'))
            ref2mni_FLIRT.inputs.reference = mni
            ref2mni_FLIRT.inputs.cost = "mutualinfo"
            ref2mni_FLIRT.inputs.searchr_x = [-90,90]
            ref2mni_FLIRT.inputs.searchr_y = [-90,90]
            ref2mni_FLIRT.inputs.searchr_z = [-90,90]
            ref2mni_FLIRT.inputs.dof = 12
            ref2mni_FLIRT.inputs.cost = "corratio"
            ref2mni_FLIRT.inputs.out_matrix_file  = "ref2mni.mat"
            #registrazione non lineare
            ref2mni_FNIRT = Node(FNIRT(), name='ref2mni_FNIRT')
            ref2mni_FNIRT.inputs.ref_file = mni
            ref2mni_FNIRT.inputs.fieldcoeff_file = True
            #matrice inversa da atlante mni a ref
            ref2mni_INVWARP = Node(InvWarp(), name='ref2mni_INVWARP')

        #REGISTRAZIONE AD ALTANTE MNI1mm (SERVE SOLO PER DOmap)
        if wfType==1 and check_input['mr_flair3d'] and DOmap:
            #registrazione lineare
            ref2mni1_FLIRT = Node(FLIRT(), name='ref2mni1_FLIRT')
            mni1 = abspath(os.path.join(os.environ["FSL_DIR"],'data/standard/MNI152_T1_1mm_brain.nii.gz'))
            ref2mni1_FLIRT.inputs.reference = mni1
            ref2mni1_FLIRT.inputs.cost = "mutualinfo"
            ref2mni1_FLIRT.inputs.searchr_x = [-90,90]
            ref2mni1_FLIRT.inputs.searchr_y = [-90,90]
            ref2mni1_FLIRT.inputs.searchr_z = [-90,90]
            ref2mni1_FLIRT.inputs.dof = 12
            ref2mni1_FLIRT.inputs.cost = "corratio"
            ref2mni1_FLIRT.inputs.out_matrix_file  = "ref2mni1.mat"
            #registrazione non lineare
            ref2mni1_FNIRT = Node(FNIRT(), name='ref2mni1_FNIRT')
            ref2mni1_FNIRT.inputs.ref_file = mni1
            ref2mni1_FNIRT.inputs.fieldcoeff_file = True
            #matrice inversa da atlante mni a ref
            ref2mni1_INVWARP = Node(InvWarp(), name='ref2mni1_INVWARP')

        #REGISTRAZIONE AD ALTANTE SIMMETRICO PER EVENTUALI ASIMMETRY index
        if wfType==1 and (check_input['mr_asl'] or check_input['pet_brain']):
            #registrazione lineare
            ref2sym_FLIRT = Node(FLIRT(), name='ref2sym_FLIRT')
            sym_template = SWANi_supplement.sym_template
            ref2sym_FLIRT.inputs.reference = sym_template
            ref2sym_FLIRT.inputs.cost = "mutualinfo"
            ref2sym_FLIRT.inputs.searchr_x = [-90,90]
            ref2sym_FLIRT.inputs.searchr_y = [-90,90]
            ref2sym_FLIRT.inputs.searchr_z = [-90,90]
            ref2sym_FLIRT.inputs.dof = 12
            ref2sym_FLIRT.inputs.cost = "corratio"
            ref2sym_FLIRT.inputs.out_matrix_file  = "ref2sym.mat"
            #registrazione non lineare
            ref2sym_FNIRT = Node(FNIRT(), name='ref2sym_FNIRT')
            ref2sym_FNIRT.inputs.ref_file = sym_template
            ref2sym_FNIRT.inputs.fieldcoeff_file = True
            #matrice inversa da atlante simmetrico a ref
            ref2sym_INVWARP = Node(InvWarp(), name='ref2sym_INVWARP')
            #immagine ribaltata in RL del soggetto nello spazio dell'atlante simmetrico
            sym_SWAP=Node(SwapDimensions(), name='sym_SWAP')
            sym_SWAP.inputs.out_file="sym_ref_brain_swapped.nii.gz"
            sym_SWAP.inputs.new_dims=("-x","y","z")
            #trasformazione lineare dell'immagine ribaltata sull'originale
            swap2sym_FLIRT = Node(FLIRT(), name='swap2sym_FLIRT')
            swap2sym_FLIRT.inputs.cost = "mutualinfo"
            swap2sym_FLIRT.inputs.searchr_x = [-90,90]
            swap2sym_FLIRT.inputs.searchr_y = [-90,90]
            swap2sym_FLIRT.inputs.searchr_z = [-90,90]
            swap2sym_FLIRT.inputs.dof = 6
            swap2sym_FLIRT.inputs.interp = "trilinear"
            swap2sym_FLIRT.inputs.out_matrix_file  = "swap2sym.mat"
            #trasformazione non lineare dell'immagine ribaltata sull'originale
            swap2sym_FNIRT = Node(FNIRT(), name='swap2sym_FNIRT')
            swap2sym_FNIRT.inputs.fieldcoeff_file = True
            swap2sym_FNIRT.inputs.ref_file=sym_template

        #ELABORAZIONE FREESURFER
        if isfreesurfer:
            #recon all
            reconAll=Node(ReconAll(), name='reconAll')
            reconAll.inputs.subjects_dir=self.base_dir
            reconAll.inputs.subject_id="FS"
            reconAll.inputs.openmp=max_node_cpu
            reconAll.inputs.parallel=True
            reconAll.inputs.directive = 'all'
            #sposto aparcaseg nello spazio ref
            aparaseg2Volmgz = Node(Label2Vol_mo(),name="aparaseg2Volmgz")
            aparaseg2Volmgz.inputs.vol_label_file="./r-aparc_aseg.mgz"
            aparaseg2Volnii = Node(Label2Vol_mo(),name="aparaseg2Volnii")
            aparaseg2Volnii.inputs.vol_label_file="r-aparc_aseg.nii.gz"
            #estrazione ROI sostanza bianca
            lhwmROI = Node(thrROI(),name='lhwmROI')
            lhwmROI.inputs.seg_val_min=2
            lhwmROI.inputs.seg_val_max=2
            lhwmROI.inputs.out_file="lhwmROI.nii.gz"
            rhwmROI = Node(thrROI(),name='rhwmROI')
            rhwmROI.inputs.seg_val_min=41
            rhwmROI.inputs.seg_val_max=41
            rhwmROI.inputs.out_file="rhwmROI.nii.gz"
            wmROI = Node(BinaryMaths(),name='wmROI')
            wmROI.inputs.operation="add"
            wmROI.inputs.out_file="wmROI.nii.gz"
            #estrazione ROI bgt
            lhbgtROI = Node(thrROI(),name='lhbgtROI')
            lhbgtROI.inputs.seg_val_min=10
            lhbgtROI.inputs.seg_val_max=13
            lhbgtROI.inputs.out_file="lhbgtROI.nii.gz"
            rhbgtROI = Node(thrROI(),name='rhbgtROI')
            rhbgtROI.inputs.seg_val_min=49
            rhbgtROI.inputs.seg_val_max=52
            rhbgtROI.inputs.out_file="rhbgtROI.nii.gz"
            bgtROI = Node(BinaryMaths(),name='bgtROI')
            bgtROI.inputs.operation="add"
            bgtROI.inputs.out_file="bgtROI.nii.gz"
            if wfType==1 and isHippoAmygLabels:
                #segmentazione ippocampo e amigdala
                segmentHA = Node(segmentHA_mo(),name="segmentHA_mo")
                segmentHA.inputs.num_threads=max_node_cpu
                #sposto la segmentazione ippocampo e amigdala nello spazio ref
                # self.segmentHA_lh2Vol = Node(Label2Vol_mo(),name="segmentHA_lh2Vol")
                # self.segmentHA_lh2Vol.inputs.vol_label_file="./r-lh.hippoAmygLabels-T1.mgz"
                # self.segmentHA_rh2Vol = Node(Label2Vol_mo(),name="segmentHA_rh2Vol")
                # self.segmentHA_rh2Vol.inputs.vol_label_file="./r-rh.hippoAmygLabels-T1.mgz"

        #ELABORAZIONE FLAIR
        if check_input['mr_flair3d']:
            #conversione dicom->nifti
            flair_conv = Node(Dcm2niix_mo(),name='flair_conv')
            flair_dir = os.path.join(self.base_dir,SWANiGlobalConfig['DEFAULTFOLDERS']['default_mr_flair3d_folder'])
            flair_conv.inputs.source_dir=flair_dir
            flair_conv.inputs.crop=True
            flair_conv.inputs.out_filename ="flair"
            #orientamento in convenzione radiologica
            flair_reOrient=Node(Orient_mo(),name='flair_reOrient')
            #rimozione scalpo
            flair_BET = Node(BET(),name='flair_BET')
            flair_BET.inputs.frac = 0.5
            flair_BET.inputs.robust = True
            flair_BET.inputs.threshold = True
            #trasformazione lineare nello spazio ref
            flair2ref_FLIRT = Node(FLIRT(), name='flair2ref_FLIRT')
            flair2ref_FLIRT.inputs.out_file  = "r-flair_brain.nii.gz"
            flair2ref_FLIRT.inputs.out_matrix_file  = "flair2ref.mat"
            flair2ref_FLIRT.inputs.cost = "mutualinfo"
            flair2ref_FLIRT.inputs.searchr_x = [-90,90]
            flair2ref_FLIRT.inputs.searchr_y = [-90,90]
            flair2ref_FLIRT.inputs.searchr_z = [-90,90]
            flair2ref_FLIRT.inputs.dof = 6
            flair2ref_FLIRT.inputs.interp = "trilinear"

        #ELABORAZIONE script_DOmap
        if wfType==1 and check_input['mr_flair3d'] and DOmap:
            #segmentazione con fast
            DOmap_FAST = Node(FAST(),name="DOmap_FAST")
            DOmap_FAST.inputs.img_type=1
            DOmap_FAST.inputs.number_classes=3
            DOmap_FAST.inputs.hyper=0.1
            DOmap_FAST.inputs.bias_lowpass=40
            DOmap_FAST.inputs.output_biascorrected=True
            DOmap_FAST.inputs.bias_iters=4
            #flair in atlante MNI1
            DOmap_flair2mni1 = Node(ApplyWarp(), name="DOmap_flair2mni1")
            DOmap_flair2mni1.inputs.ref_file = mni1
            #t1_restore in atlante MNI1
            DOmap_restore2mni1 = Node(ApplyWarp(), name="DOmap_restore2mni1")
            DOmap_restore2mni1.inputs.ref_file = mni1
            #GM in atlante MNI1
            DOmap_gm2mni1 = Node(ApplyWarp(), name="DOmap_gm2mni1")
            DOmap_gm2mni1.inputs.ref_file = mni1
            #WM in atlante MNI1
            DOmap_wm2mni1 = Node(ApplyWarp(), name="DOmap_wm2mni1")
            DOmap_wm2mni1.inputs.ref_file = mni1
            #divido FLAIR/T1
            DOmap_flairDIVref = Node(BinaryMaths(),name="DOmap_flairDIVref")
            DOmap_flairDIVref.inputs.operation="div"
            #outliers remove from mask
            DOmap_outliers_mask = Node(DOmap_outliers_mask_mo(), name="DOmap_outliers_mask")
            DOmap_outliers_mask.inputs.mask_file=SWANi_supplement.cortex_mas
            #rimuovo il cervelletto dalla flair/t1
            DOmap_cortexMask = Node(ApplyMask(), name="DOmap_cortexMask")
            #creazione maschere gm e wn su t1_restore in MNI1
            DOmap_gmMask = Node(ApplyMask(), name="DOmap_gmMask")
            DOmap_wmMask = Node(ApplyMask(), name="DOmap_wmMask")
            #calcolo media e dev standard per gm e wm
            DOmap_gm_mean = Node(ImageStats(), name="DOmap_gm_mean")
            DOmap_gm_mean.inputs.op_string="-M"
            DOmap_wm_mean = Node(ImageStats(), name="DOmap_wm_mean")
            DOmap_wm_mean.inputs.op_string="-M"
            DOmap_gm_std = Node(ImageStats(), name="DOmap_gm_std")
            DOmap_gm_std.inputs.op_string="-S"
            DOmap_wm_std = Node(ImageStats(), name="DOmap_wm_std")
            DOmap_wm_std.inputs.op_string="-S"
            #maschera generata da soglia per media e dev standard su immagine divisa (perchè mai???)
            DOmap_binaryFLAIR = Node(thrROI(), name='DOmap_binaryFLAIR')
            DOmap_binaryFLAIR.inputs.out_file="binary_flair.nii.gz"
            #convolutional flair_reOrient
            DOmap_convolution_flair = Node(DilateImage_mo(),name="DOmap_convolution_flair")
            DOmap_convolution_flair.inputs.args="-fmean"
            DOmap_convolution_flair.inputs.kernel_shape="boxv"
            DOmap_convolution_flair.inputs.kernel_size=5
            DOmap_convolution_flair.inputs.out_file="convolution_flair.nii.gz"
            #calcolo junction e relativo zscore
            DOmap_junction = Node(BinaryMaths(), name="DOmap_junction")
            DOmap_junction.inputs.operation="sub"
            DOmap_junction.inputs.operand_file=SWANi_supplement.mean_flair
            DOmap_junction.inputs.out_file="junction_flair.nii.gz"
            DOmap_junctionz = Node(BinaryMaths(), name="DOmap_junctionz")
            DOmap_junctionz.inputs.operation="div"
            DOmap_junctionz.inputs.operand_file=SWANi_supplement.std_final_flair
            DOmap_junctionz.inputs.out_file="junctionZ_flair.nii.gz"
            DOmap_masked_cerebellum = Node(ApplyMask(), name="DOmap_masked_cerebellum")
            DOmap_masked_cerebellum.inputs.mask_file=SWANi_supplement.binary_cerebellum
            DOmap_cerebellum_mean = Node(ImageStats(), name="DOmap_cerebellum_mean")
            DOmap_cerebellum_mean.inputs.op_string="-M"
            DOmap_restore_gmMask = Node(ApplyMask(), name="DOmap_restore_gmMask")
            DOmap_restore_gmMask.inputs.out_file="masked_image_GM.nii.gz"
            DOmap_normalised_GM_mask = Node(BinaryMaths(), name="DOmap_normalised_GM_mask")
            DOmap_normalised_GM_mask.inputs.operation="div"
            DOmap_normalised_GM_mask.inputs.out_file="normalised_GM_mask.nii.gz"
            DOmap_smoothed_image_extension = Node(DilateImage_mo(),name="DOmap_smoothed_image_extension")
            DOmap_smoothed_image_extension.inputs.args="-fmean"
            DOmap_smoothed_image_extension.inputs.kernel_shape="boxv"
            DOmap_smoothed_image_extension.inputs.kernel_size=5
            DOmap_smoothed_image_extension.inputs.out_file="smoothed_image_extension.nii.gz"
            DOmap_image_extension = Node(BinaryMaths(), name="DOmap_image_extension")
            DOmap_image_extension.inputs.operation="sub"
            DOmap_image_extension.inputs.operand_file=SWANi_supplement.mean_extension
            DOmap_image_extension.inputs.out_file="extension_image.nii.gz"
            DOmap_image_extensionz = Node(BinaryMaths(), name="DOmap_image_extensionz")
            DOmap_image_extensionz.inputs.operation="div"
            DOmap_image_extensionz.inputs.operand_file=SWANi_supplement.std_final_extension
            DOmap_image_extensionz.inputs.out_file="extension_z.nii.gz"
            DOmap_no_cereb_extension_z = Node(ApplyMask(), name="no_cereb_extension_z")
            DOmap_no_cereb_extension_z.inputs.out_file="no_cereb_extension_z.nii.gz"
            DOmap_extensionz2ref = Node(ApplyWarp(),name="DOmap_extensionz2ref")
            DOmap_extensionz2ref.inputs.out_file="r-extension_z.nii.gz"
            DOmap_junctionz2ref = Node(ApplyWarp(),name="DOmap_junctionz2ref")
            DOmap_junctionz2ref.inputs.out_file="r-junction_z.nii.gz"
            DOmap_binaryFLAIR2ref = Node(ApplyWarp(),name="DOmap_binaryFLAIR2ref")
            DOmap_binaryFLAIR2ref.inputs.out_file="r-binaryFLAIR.nii.gz"

        #ELABORAZIONE FLAIR 2D TRA
        if flair2D and check_input['op_mr_flair2d_tra']:
            #conversione dicom->nifti
            flair2d_tra_conv = Node(Dcm2niix_mo(),name='flair2d_tra_conv')
            flair_dir = os.path.join(self.base_dir,SWANiGlobalConfig['DEFAULTFOLDERS']['default_op_mr_flair2d_tra_folder'])
            flair2d_tra_conv.inputs.source_dir=flair_dir
            flair2d_tra_conv.inputs.out_filename ="flair"
            #orientamento in convenzione radiologica
            flair2d_tra_reOrient=Node(Orient_mo(),name='flair2d_tra_reOrient')
            #rimozione scalpo
            flair2d_tra_BET = Node(BET(),name='flair2d_tra_BET')
            flair2d_tra_BET.inputs.frac = 0.5
            flair2d_tra_BET.inputs.robust = True
            flair2d_tra_BET.inputs.threshold = True
            #trasformazione lineare nello spazio ref
            flair2d_tra2ref_FLIRT = Node(FLIRT(), name='flair2d_tra2ref_FLIRT')
            flair2d_tra2ref_FLIRT.inputs.out_file  = "r-flair2d_tra_brain.nii.gz"
            flair2d_tra2ref_FLIRT.inputs.out_matrix_file  = "flair2d_tra2ref.mat"

        #ELABORAZIONE FLAIR 2D COR
        if flair2D and check_input['op_mr_flair2d_cor']:
            #conversione dicom->nifti
            flair2d_cor_conv = Node(Dcm2niix_mo(),name='flair2d_cor_conv')
            flair_dir = os.path.join(self.base_dir,SWANiGlobalConfig['DEFAULTFOLDERS']['default_op_mr_flair2d_cor_folder'])
            flair2d_cor_conv.inputs.source_dir=flair_dir
            flair2d_cor_conv.inputs.out_filename ="flair"
            #orientamento in convenzione radiologica
            flair2d_cor_reOrient=Node(Orient_mo(),name='flair2d_cor_reOrient')
            #rimozione scalpo
            flair2d_cor_BET = Node(BET(),name='flair2d_cor_BET')
            flair2d_cor_BET.inputs.frac = 0.5
            flair2d_cor_BET.inputs.robust = True
            flair2d_cor_BET.inputs.threshold = True
            #trasformazione lineare nello spazio ref
            flair2d_cor2ref_FLIRT = Node(FLIRT(), name='flair2d_cor2ref_FLIRT')
            flair2d_cor2ref_FLIRT.inputs.out_file  = "r-flair2d_cor_brain.nii.gz"
            flair2d_cor2ref_FLIRT.inputs.out_matrix_file  = "flair2d_cor2ref.mat"

        #ELABORAZIONE FLAIR 2D SAG
        if flair2D and check_input['op_mr_flair2d_sag']:
            #conversione dicom->nifti
            flair2d_sag_conv = Node(Dcm2niix_mo(),name='flair2d_sag_conv')
            flair_dir = os.path.join(self.base_dir,SWANiGlobalConfig['DEFAULTFOLDERS']['default_op_mr_flair2d_sag_folder'])
            flair2d_sag_conv.inputs.source_dir=flair_dir
            flair2d_sag_conv.inputs.out_filename ="flair"
            #orientamento in convenzione radiologica
            flair2d_sag_reOrient=Node(Orient_mo(),name='flair2d_sag_reOrient')
            #rimozione scalpo
            flair2d_sag_BET = Node(BET(),name='flair2d_sag_BET')
            flair2d_sag_BET.inputs.frac = 0.5
            flair2d_sag_BET.inputs.robust = True
            flair2d_sag_BET.inputs.threshold = True
            #trasformazione lineare nello spazio ref
            flair2d_sag2ref_FLIRT = Node(FLIRT(), name='flair2d_sag2ref_FLIRT')
            flair2d_sag2ref_FLIRT.inputs.out_file  = "r-flair2d_sag_brain.nii.gz"
            flair2d_sag2ref_FLIRT.inputs.out_matrix_file  = "flair2d_sag2ref.mat"



        #ELABORAZIONE MDC
        if check_input['mr_mdc']:
            #conversione dicom->nifti
            mdc_conv = Node(Dcm2niix_mo(),name='mdc_conv')
            mdc_dir = os.path.join(self.base_dir,SWANiGlobalConfig['DEFAULTFOLDERS']['default_mr_mdc_folder'])
            mdc_conv.inputs.source_dir=mdc_dir
            mdc_conv.inputs.crop=True
            mdc_conv.inputs.out_filename ="mdc"
            #orientamento in convenzione radiologica
            mdc_reOrient=Node(Orient_mo(),name='mdc_reOrient')
            #rimozione scalpo
            mdc_BET = Node(BET(),name='mdc_BET')
            mdc_BET.inputs.frac = 0.3
            mdc_BET.inputs.robust = True
            mdc_BET.inputs.threshold = True
            #trasformazione lineare nello spazio ref
            mdc2ref_FLIRT = Node(FLIRT(), name='mdc2ref_FLIRT')
            mdc2ref_FLIRT.inputs.out_file  = "r-mdc_brain.nii.gz"
            mdc2ref_FLIRT.inputs.out_matrix_file  = "mdc2ref.mat"
            mdc2ref_FLIRT.inputs.cost = "mutualinfo"
            mdc2ref_FLIRT.inputs.searchr_x = [-90,90]
            mdc2ref_FLIRT.inputs.searchr_y = [-90,90]
            mdc2ref_FLIRT.inputs.searchr_z = [-90,90]
            mdc2ref_FLIRT.inputs.dof = 6
            mdc2ref_FLIRT.inputs.interp = "trilinear"

        #ELABORAZIONE ASL
        if check_input['mr_asl']:
            #conversione dicom->nifti
            asl_conv = Node(Dcm2niix_mo(),name='asl_conv')
            asl_conv.inputs.out_filename ="asl"
            asl_dir = os.path.join(self.base_dir,SWANiGlobalConfig['DEFAULTFOLDERS']['default_mr_asl_folder'])
            asl_conv.inputs.source_dir=asl_dir
            #orientamento in convenzione radiologica
            asl_reOrient=Node(Orient_mo(),name='asl_reOrient')
            #smoothing gaussiano
            asl_SMOOTH = Node(IsotropicSmooth(),name='asl_SMOOTH')
            asl_SMOOTH.inputs.sigma = 4
            #calcolo matrice di trasformazione nello spazio ref
            asl2ref_FLIRT = Node(FLIRT(), name='asl2ref_FLIRT')
            asl2ref_FLIRT.inputs.cost = "mutualinfo"
            asl2ref_FLIRT.inputs.searchr_x = [-90,90]
            asl2ref_FLIRT.inputs.searchr_y = [-90,90]
            asl2ref_FLIRT.inputs.searchr_z = [-90,90]
            asl2ref_FLIRT.inputs.dof = 6
            asl2ref_FLIRT.inputs.interp = "trilinear"
            #trasposizione del volume smooth nello spazio ref
            aslsmooth2ref_FLIRT=Node(FLIRT(), name='aslsmooth2ref_FLIRT')
            aslsmooth2ref_FLIRT.inputs.out_file  = "r-asl.nii.gz"
            aslsmooth2ref_FLIRT.inputs.interp = "trilinear"
            #rimozione scalpo
            asl_mask = Node(ApplyMask(),name='asl_mask')
            asl_mask.inputs.out_file='r-asl.nii.gz'
            if wfType==1:
                #trasformazione non lineare delle immagini asl nell'atlante simmetrico
                asl2sym_APPLYWARP = Node(ApplyWarp(), name='asl2sym_APPLYWARP')
                asl2sym_APPLYWARP.inputs.ref_file=sym_template
                #immagine ribaltata in RL della asl nello spazio dell'atlante simmetrico
                aslsym_SWAP=Node(SwapDimensions(), name='aslsym_SWAP')
                aslsym_SWAP.inputs.out_file="asl_sym_swapped.nii.gz"
                aslsym_SWAP.inputs.new_dims=("-x","y","z")
                #trasformazione non lineare da immagine ribaltata a immagine simmetrica
                asl_swapped_APPLYWARP = Node(ApplyWarp(), name='asl_swapped_APPLYWARP')
                asl_swapped_APPLYWARP.inputs.ref_file=sym_template
                #calcolo asimmetry index
                asl_AI = Node(AIndex(), name="asl_AI")
                asl_AI.inputs.out_file="aslAI.nii.gz"
                #trasformazione non lineare da atlante simmetrico a ref
                asl_AI2ref = Node(ApplyWarp(),name="asl_AI2ref")
                asl_AI2ref.inputs.out_file="r-asl_AI.nii.gz"
            if isfreesurfer:
                #PROIEZIONE DELLA asl SULLA SUPERFICIE PIALE DI FREESURFER
                asl_surf_lh = Node(SampleToSurface(), name='asl_surf_lh')
                asl_surf_lh.inputs.hemi='lh'
                asl_surf_lh.inputs.out_file="asl_surf_lh.mgz"
                asl_surf_lh.inputs.cortex_mask=True
                asl_surf_lh.inputs.reg_header=True
                asl_surf_lh.inputs.sampling_method = "point"
                asl_surf_lh.inputs.sampling_range = 0.5
                asl_surf_lh.inputs.sampling_units = "frac"
                asl_surf_rh = Node(SampleToSurface(), name='asl_surf_rh')
                asl_surf_rh.inputs.hemi='rh'
                asl_surf_rh.inputs.out_file="asl_surf_rh.mgz"
                asl_surf_rh.inputs.cortex_mask=True
                asl_surf_rh.inputs.reg_header=True
                asl_surf_rh.inputs.sampling_method = "point"
                asl_surf_rh.inputs.sampling_range = 0.5
                asl_surf_rh.inputs.sampling_units = "frac"
                if wfType==1:
                    #PROIEZIONE DELLA asl AI SULLA SUPERFICIE PIALE DI FREESURFER
                    aslAI_surf_lh = Node(SampleToSurface(), name='aslAI_surf_lh')
                    aslAI_surf_lh.inputs.hemi='lh'
                    aslAI_surf_lh.inputs.out_file="aslAI_surf_lh.mgz"
                    aslAI_surf_lh.inputs.cortex_mask=True
                    aslAI_surf_lh.inputs.reg_header=True
                    aslAI_surf_lh.inputs.sampling_method = "point"
                    aslAI_surf_lh.inputs.sampling_range = 0.5
                    aslAI_surf_lh.inputs.sampling_units = "frac"
                    aslAI_surf_rh = Node(SampleToSurface(), name='aslAI_surf_rh')
                    aslAI_surf_rh.inputs.hemi='rh'
                    aslAI_surf_rh.inputs.out_file="aslAI_surf_rh.mgz"
                    aslAI_surf_rh.inputs.cortex_mask=True
                    aslAI_surf_rh.inputs.reg_header=True
                    aslAI_surf_rh.inputs.sampling_method = "point"
                    aslAI_surf_rh.inputs.sampling_range = 0.5
                    aslAI_surf_rh.inputs.sampling_units = "frac"
                    #STATISTICA ZSCORE SULLA asl
                    asl_zscore = Node(Zscore(),name="asl_zscore")
                    asl_zscore_mask = Node(ApplyMask(),name="asl_zscore_mask")
                    asl_zscore_mask.inputs.out_file="r-asl_brain_z.nii.gz"
                    #PROIEZIONE DELLA asl z-score SULLA SUPERFICIE PIALE DI FREESURFER
                    aslZscore_surf_lh = Node(SampleToSurface(), name='aslZscore_surf_lh')
                    aslZscore_surf_lh.inputs.hemi='lh'
                    aslZscore_surf_lh.inputs.out_file="aslZscore_surf_lh.mgz"
                    aslZscore_surf_lh.inputs.cortex_mask=True
                    aslZscore_surf_lh.inputs.reg_header=True
                    aslZscore_surf_lh.inputs.sampling_method = "point"
                    aslZscore_surf_lh.inputs.sampling_range = 0.5
                    aslZscore_surf_lh.inputs.sampling_units = "frac"
                    aslZscore_surf_rh = Node(SampleToSurface(), name='aslZscore_surf_rh')
                    aslZscore_surf_rh.inputs.hemi='rh'
                    aslZscore_surf_rh.inputs.out_file="aslZscore_surf_rh.mgz"
                    aslZscore_surf_rh.inputs.cortex_mask=True
                    aslZscore_surf_rh.inputs.reg_header=True
                    aslZscore_surf_rh.inputs.sampling_method = "point"
                    aslZscore_surf_rh.inputs.sampling_range = 0.5
                    aslZscore_surf_rh.inputs.sampling_units = "frac"


        #ELABORAZIONE PET
        if check_input['pet_brain'] and check_input['ct_brain']:
            #conversione immagine TC dicom->nifti
            pet_ct_conv = Node(Dcm2niix_mo(), name='pet_ct_conv')
            pet_ct_dir = os.path.join(self.base_dir,SWANiGlobalConfig['DEFAULTFOLDERS']['default_ct_brain_folder'])
            pet_ct_conv.inputs.source_dir=pet_ct_dir
            pet_ct_conv.inputs.out_filename ="pet_ct"
            #conversione immagine PET dicom->nifti
            pet_brain_conv = Node(Dcm2niix_mo(), name='pet_brain_conv')
            pet_brain_dir = os.path.join(self.base_dir,SWANiGlobalConfig['DEFAULTFOLDERS']['default_pet_brain_folder'])
            pet_brain_conv.inputs.source_dir=pet_brain_dir
            pet_brain_conv.inputs.out_filename ="pet_brain"
            #trasformazione lineare immagine TC su ref
            pet_ct2ref_FLIRT = Node(FLIRT(), name='pet_ct2ref_FLIRT')
            pet_ct2ref_FLIRT.inputs.out_file  = "r-pet_ct.nii.gz"
            pet_ct2ref_FLIRT.inputs.out_matrix_file  = "ct2ref.mat"
            pet_ct2ref_FLIRT.inputs.cost = "mutualinfo"
            pet_ct2ref_FLIRT.inputs.searchr_x = [-90,90]
            pet_ct2ref_FLIRT.inputs.searchr_y = [-90,90]
            pet_ct2ref_FLIRT.inputs.searchr_z = [-90,90]
            pet_ct2ref_FLIRT.inputs.dof = 6
            pet_ct2ref_FLIRT.inputs.interp = "trilinear"
            #trasformazione lineare immagine PET su TC
            pet_brain2ct_FLIRT = Node(FLIRT(), name='pet_brain2ct_FLIRT')
            pet_brain2ct_FLIRT.inputs.out_matrix_file  = "pet2ct.mat"
            pet_brain2ct_FLIRT.inputs.cost = "mutualinfo"
            pet_brain2ct_FLIRT.inputs.searchr_x = [-90,90]
            pet_brain2ct_FLIRT.inputs.searchr_y = [-90,90]
            pet_brain2ct_FLIRT.inputs.searchr_z = [-90,90]
            pet_brain2ct_FLIRT.inputs.dof = 6
            pet_brain2ct_FLIRT.inputs.interp = "trilinear"
            #concatenazione delle due trasformazioni precedenti
            pet_convert_XFM = Node(ConvertXFM(), name='pet_convert_XFM')
            pet_convert_XFM.inputs.concat_xfm = True
            pet_convert_XFM.inputs.out_file = "pet2ref.mat"
            #trasformazione lineare immagine PET su ref
            pet_brain2ref_FLIRT = Node(FLIRT(), name='pet_brain2ref_FLIRT')
            pet_brain2ref_FLIRT.inputs.out_file  = "r-pet_brain.nii.gz"
            pet_brain2ref_FLIRT.inputs.apply_xfm = True
            pet_brain2ref_FLIRT.inputs.interp = "trilinear"
            #smoothing gaussiano
            pet_brain_SMOOTH = Node(IsotropicSmooth(),name='pet_brain_SMOOTH')
            pet_brain_SMOOTH.inputs.sigma = 4
            if wfType==1:
                #trasformazione non lineare delle immagini PET nell'atlante simmetrico
                pet_brain_sm_APPLYWARP = Node(ApplyWarp(), name='pet_brain_sm_APPLYWARP')
                pet_brain_sm_APPLYWARP.inputs.ref_file=sym_template
                #immagine ribaltata in RL della PET nello spazio dell'atlante simmetrico
                petsym_SWAP=Node(SwapDimensions(), name='petsym_SWAP')
                petsym_SWAP.inputs.out_file="pet_brain_sym_swapped.nii.gz"
                petsym_SWAP.inputs.new_dims=("-x","y","z")
                #trasformazione non lineare da immagine ribaltata a immagine simmetrica
                pet_brain_swapped_APPLYWARP = Node(ApplyWarp(), name='pet_brain_swapped_APPLYWARP')
                pet_brain_swapped_APPLYWARP.inputs.ref_file=sym_template
                #calcolo asimmetry index
                pet_AI = Node(AIndex(), name="pet_AI")
                pet_AI.inputs.out_file="petAI.nii.gz"
                #trasformazione non lineare da atlante simmetrico a ref
                pet_AI2ref = Node(ApplyWarp(),name="pet_AI2ref")
                pet_AI2ref.inputs.out_file="r-petAI.nii.gz"
                #applico la maschera per eliminare il fondo
                pet_AI_mask = Node(ApplyMask(),name="pet_AI_mask")
                pet_AI_mask.inputs.out_file="r-pet_brain_AI.nii.gz"
            if isfreesurfer:
                #PROIEZIONE DELLA PET SULLA SUPERFICIE PIALE DI FREESURFER
                pet_surf_lh = Node(SampleToSurface(), name='pet_surf_lh')
                pet_surf_lh.inputs.hemi='lh'
                pet_surf_lh.inputs.out_file="pet_surf_lh.mgz"
                pet_surf_lh.inputs.cortex_mask=True
                pet_surf_lh.inputs.reg_header=True
                pet_surf_lh.inputs.sampling_method = "point"
                pet_surf_lh.inputs.sampling_range = 0.5
                pet_surf_lh.inputs.sampling_units = "frac"
                pet_surf_rh = Node(SampleToSurface(), name='pet_surf_rh')
                pet_surf_rh.inputs.hemi='rh'
                pet_surf_rh.inputs.out_file="pet_surf_rh.mgz"
                pet_surf_rh.inputs.cortex_mask=True
                pet_surf_rh.inputs.reg_header=True
                pet_surf_rh.inputs.sampling_method = "point"
                pet_surf_rh.inputs.sampling_range = 0.5
                pet_surf_rh.inputs.sampling_units = "frac"
                if wfType==1:
                    #PROIEZIONE DELLA PET AI SULLA SUPERFICIE PIALE DI FREESURFER
                    petAI_surf_lh = Node(SampleToSurface(), name='petAI_surf_lh')
                    petAI_surf_lh.inputs.hemi='lh'
                    petAI_surf_lh.inputs.out_file="petAI_surf_lh.mgz"
                    petAI_surf_lh.inputs.cortex_mask=True
                    petAI_surf_lh.inputs.reg_header=True
                    petAI_surf_lh.inputs.sampling_method = "point"
                    petAI_surf_lh.inputs.sampling_range = 0.5
                    petAI_surf_lh.inputs.sampling_units = "frac"
                    petAI_surf_rh = Node(SampleToSurface(), name='petAI_surf_rh')
                    petAI_surf_rh.inputs.hemi='rh'
                    petAI_surf_rh.inputs.out_file="petAI_surf_rh.mgz"
                    petAI_surf_rh.inputs.cortex_mask=True
                    petAI_surf_rh.inputs.reg_header=True
                    petAI_surf_rh.inputs.sampling_method = "point"
                    petAI_surf_rh.inputs.sampling_range = 0.5
                    petAI_surf_rh.inputs.sampling_units = "frac"
                    #STATISTICA Z-SCORE SULLA pet
                    pet_zscore = Node(Zscore(),name="pet_zscore")
                    pet_zscore_mask = Node(ApplyMask(),name="pet_zscore_mask")
                    pet_zscore_mask.inputs.out_file="r-pet_brain_z.nii.gz"
                    #PROIEZIONE DELLA PET z-score SULLA SUPERFICIE PIALE DI FREESURFER
                    petZscore_surf_lh = Node(SampleToSurface(), name='petZscore_surf_lh')
                    petZscore_surf_lh.inputs.hemi='lh'
                    petZscore_surf_lh.inputs.out_file="petZscore_surf_lh.mgz"
                    petZscore_surf_lh.inputs.cortex_mask=True
                    petZscore_surf_lh.inputs.reg_header=True
                    petZscore_surf_lh.inputs.sampling_method = "point"
                    petZscore_surf_lh.inputs.sampling_range = 0.5
                    petZscore_surf_lh.inputs.sampling_units = "frac"
                    petZscore_surf_rh = Node(SampleToSurface(), name='petZscore_surf_rh')
                    petZscore_surf_rh.inputs.hemi='rh'
                    petZscore_surf_rh.inputs.out_file="petZscore_surf_rh.mgz"
                    petZscore_surf_rh.inputs.cortex_mask=True
                    petZscore_surf_rh.inputs.reg_header=True
                    petZscore_surf_rh.inputs.sampling_method = "point"
                    petZscore_surf_rh.inputs.sampling_range = 0.5
                    petZscore_surf_rh.inputs.sampling_units = "frac"


        #ELABORAZIONE VENOSA
        if wfType==0 and check_input['mr_venosa']:
            #conversione dicom->nifti
            venosa_conv = Node(Dcm2niix_mo(),name='venosa_conv')
            venosa_dir = os.path.join(self.base_dir,SWANiGlobalConfig['DEFAULTFOLDERS']['default_mr_venosa_folder'])
            venosa_conv.inputs.source_dir=venosa_dir
            venosa_conv.inputs.out_filename ="venosa"
            #orientamento in convenzione radiologica
            venosa_reOrient=Node(Orient_mo(),name='venosa_reOrient')
            if check_input['mr_venosa2']:
                #se le fasi sono separate, converto anche la seconda
                #conversione dicom->nifti
                venosa2_conv = Node(Dcm2niix_mo(),name='venosa2_conv')
                venosa2_dir = os.path.join(self.base_dir,SWANiGlobalConfig['DEFAULTFOLDERS']['default_mr_venosa2_folder'])
                venosa2_conv.inputs.source_dir=venosa2_dir
                venosa2_conv.inputs.out_filename ="venosa2"
                #orientamento in convenzione radiologica
                venosa2_reOrient=Node(Orient_mo(),name='venosa2_reOrient')
                #unifico gli output dei reOrient da passare al check
                venosa_merge=Node(Merge(2),name="venosa_merge")
            else:
                #altrimenti separo le due fasi della phase contrast
                venosa_split=Node(Split(),name='venosa_split')
                venosa_split.inputs.dimension='t'
            #individuo la fase venosa dal modulo
            venosa_check=Node(VenosaCheck(), name='venosa_check')
            #segmento le strutture intracraniche nel modulo (migliore visualizzazione dell'osso)
            venosa_BET=Node(BET(),name='venosa_BET')
            venosa_BET.inputs.frac = 0.4
            venosa_BET.inputs.mask = True
            venosa_BET.inputs.threshold = True
            venosa_BET.inputs.surfaces = True
            #registrazione lineare modulo a ref
            venosa_modulo2ref_FLIRT=Node(FLIRT(), name='venosa_modulo2ref_FLIRT')
            venosa_modulo2ref_FLIRT.inputs.out_matrix_file  = "venosa2ref.mat"
            venosa_modulo2ref_FLIRT.inputs.cost = "mutualinfo"
            venosa_modulo2ref_FLIRT.inputs.searchr_x = [-90,90]
            venosa_modulo2ref_FLIRT.inputs.searchr_y = [-90,90]
            venosa_modulo2ref_FLIRT.inputs.searchr_z = [-90,90]
            venosa_modulo2ref_FLIRT.inputs.dof = 6
            venosa_modulo2ref_FLIRT.inputs.interp = "trilinear"
            #applico la maschera delle strutture intracraniche alla fase venosa
            venosa_inskull_mask=Node(ApplyMask(), name='venosa_inskull_mask')
            #trasformazione lineare fase venosa su ref
            venosa2ref_FLIRT=Node(FLIRT(), name='venosa2ref_FLIRT')
            venosa2ref_FLIRT.inputs.out_file  = "r-venosa_inskull.nii.gz"
            venosa2ref_FLIRT.inputs.interp = "trilinear"

        #ELABORAZIONE DTI
        if check_input['mr_dti']:
            #conversione dicom->nifti
            dti_conv = Node(Dcm2niix_mo(),name='dti_conv')
            dti_dir = os.path.join(self.base_dir,SWANiGlobalConfig['DEFAULTFOLDERS']['default_mr_dti_folder'])
            dti_conv.inputs.source_dir=dti_dir
            dti_conv.inputs.out_filename ="dti"
            #estrazione immagine b0
            dti_nodif = Node(ExtractROI(),name='dti_nodif')
            dti_nodif.inputs.t_min=0
            dti_nodif.inputs.t_size=1
            dti_nodif.inputs.roi_file='nodif.nii.gz'
            #rimozione scalpo al b0
            nodif_BET = Node(BET(),name='nodif_BET')
            nodif_BET.inputs.frac = 0.3
            nodif_BET.inputs.robust = True
            nodif_BET.inputs.threshold = True
            nodif_BET.inputs.mask = True
            #correzione artefatti da movimento e eddy current
            dti_eddy = Node(EddyCorrect(),name='dti_eddy')
            dti_eddy.inputs.ref_num=0
            dti_eddy.inputs.out_file="data.nii.gz"
            #calcolo delle metriche base dti
            dti_dtifit = Node(DTIFit(),name='dti_dtifit')
            #trasformazione lineare nodif nello spazio ref
            diff2ref_FLIRT = Node(FLIRT(), name='diff2ref_FLIRT')
            diff2ref_FLIRT.inputs.out_matrix_file  = "diff2ref.mat"
            diff2ref_FLIRT.inputs.cost = "corratio"
            diff2ref_FLIRT.inputs.searchr_x = [-90,90]
            diff2ref_FLIRT.inputs.searchr_y = [-90,90]
            diff2ref_FLIRT.inputs.searchr_z = [-90,90]
            diff2ref_FLIRT.inputs.dof = 6
            #sposto FA nello spazio ref
            FA2ref_FLIRT=Node(FLIRT(), name='FA2ref_FLIRT')
            FA2ref_FLIRT.inputs.out_file  = "r-FA.nii.gz"
            FA2ref_FLIRT.inputs.interp = "trilinear"
            if wfType==0:
                #calcolo del modello di trattografia
                dti_bedpostx = Node(BEDPOSTX5_mo(),name='dti_bedpostx')
                dti_bedpostx.inputs.n_fibres=2
                dti_bedpostx.inputs.rician=True
                #dti_bedpostx.inputs.num_threads=18
                dti_bedpostx.inputs.sample_every=25
                dti_bedpostx.inputs.n_jumps=1250
                dti_bedpostx.inputs.burn_in=1000
                #calcolo di varie matrici di trasformazione derivate che serviranno per la trattografia
                ref2diff_convert = Node(ConvertXFM(),name='ref2diff_convert')
                ref2diff_convert.inputs.invert_xfm=True
                ref2diff_convert.inputs.out_file='ref2diff.mat'
                diff2mni_convert = Node(ConvertXFM(),name='diff2mni_convert')
                diff2mni_convert.inputs.concat_xfm=True
                diff2mni_convert.inputs.out_file='diff2mni.mat'
                mni2diff_convert = Node(ConvertXFM(),name='mni2diff_convert')
                mni2diff_convert.inputs.invert_xfm=True
                mni2diff_convert.inputs.out_file='mni2diff.mat'
                diff2mni_convertwarp = Node(ConvertWarp(),name='diff2mni_convertwarp')
                diff2mni_convertwarp.inputs.reference=mni
                diff2mni_convertwarp.inputs.out_file='diff2mni_warp.nii.gz'
                mni2diff_convertwarp = Node(ConvertWarp(),name='mni2diff_convertwarp')
                mni2diff_convertwarp.inputs.out_file='mni2diff_warp.nii.gz'


        #WORKFLOW CREATION
        t1 = Workflow_mo(name="t13d",base_dir="./")
        t1.connect(ref_conv, "converted_files", ref_reOrient, "in_file")
        t1.connect(ref_reOrient, "out_file", ref_BET, "in_file")
        t1.sink_result(self.base_dir,ref_BET,'out_file','scene')
        t1.sink_result(self.base_dir,ref_reOrient,'out_file','scene')
        self.add_nodes([t1])

        if wfType==0 and check_input['mr_dti']:
            mni = Workflow_mo(name="mni",base_dir="./")
            mni.add_nodes([ref2mni_FLIRT,ref2mni_FNIRT])
            self.connect(t1, "ref_BET.out_file", mni, "ref2mni_FLIRT.in_file")
            self.connect(t1, "ref_BET.out_file", mni, "ref2mni_FNIRT.in_file")
            mni.connect(ref2mni_FLIRT, "out_matrix_file", ref2mni_FNIRT, "affine_file")
            mni.connect(ref2mni_FNIRT, "fieldcoeff_file", ref2mni_INVWARP, "warp")
            self.connect(t1, "ref_BET.out_file", mni, "ref2mni_INVWARP.reference")

        if wfType==1 and check_input['mr_flair3d'] and DOmap:
            mni1 = Workflow_mo(name="mni1",base_dir="./")
            mni1.add_nodes([ref2mni1_FLIRT,ref2mni1_FNIRT])
            self.connect(t1, "ref_BET.out_file", mni1, "ref2mni1_FLIRT.in_file")
            self.connect(t1, "ref_BET.out_file", mni1, "ref2mni1_FNIRT.in_file")
            mni1.connect(ref2mni1_FLIRT, "out_matrix_file", ref2mni1_FNIRT, "affine_file")
            mni1.connect(ref2mni1_FNIRT, "fieldcoeff_file", ref2mni1_INVWARP, "warp")
            self.connect(t1, "ref_BET.out_file", mni1, "ref2mni1_INVWARP.reference")

        if wfType==1 and (check_input['mr_asl'] or check_input['pet_brain']):
            sym = Workflow_mo(name="sym",base_dir="./")
            sym.add_nodes([ref2sym_FLIRT,ref2sym_FNIRT])
            self.connect(t1, "ref_BET.out_file", sym, "ref2sym_FLIRT.in_file")
            self.connect(t1, "ref_BET.out_file", sym, "ref2sym_FNIRT.in_file")
            sym.connect(ref2sym_FLIRT, "out_matrix_file", ref2sym_FNIRT, "affine_file")
            sym.connect(ref2sym_FNIRT, "fieldcoeff_file", ref2sym_INVWARP, "warp")
            self.connect(t1, "ref_BET.out_file", sym, "ref2sym_INVWARP.reference")
            sym.connect(ref2sym_FNIRT, "warped_file", sym_SWAP, "in_file")
            sym.connect(sym_SWAP, "out_file", swap2sym_FLIRT, "in_file")
            sym.connect(ref2sym_FNIRT, "warped_file", swap2sym_FLIRT, "reference")
            sym.connect(sym_SWAP, "out_file", swap2sym_FNIRT, "in_file")
            sym.connect(swap2sym_FLIRT, "out_matrix_file", swap2sym_FNIRT, "affine_file")
            sym.connect(ref2sym_FNIRT, "warped_file", swap2sym_FNIRT, "ref_file")

        if isfreesurfer:
            freesurfer = Workflow_mo(name="freesurfer",base_dir="./")
            freesurfer.add_nodes([reconAll])
            self.connect(t1, "ref_conv.converted_files", freesurfer, "reconAll.T1_files")
            freesurfer.connect(reconAll,"rawavg",aparaseg2Volmgz,"template_file")
            freesurfer.connect([(reconAll, aparaseg2Volmgz, [(('aparc_aseg', getn, 0),'reg_header')])])
            freesurfer.connect([(reconAll, aparaseg2Volmgz, [(('aparc_aseg', getn, 0),'seg_file')])])
            freesurfer.connect(reconAll,"subjects_dir",aparaseg2Volmgz,"subjects_dir")
            freesurfer.connect(reconAll,"subject_id",aparaseg2Volmgz,"subject_id")
            freesurfer.connect(reconAll,"rawavg",aparaseg2Volnii,"template_file")
            freesurfer.connect([(reconAll, aparaseg2Volnii, [(('aparc_aseg', getn, 0),'reg_header')])])
            freesurfer.connect([(reconAll, aparaseg2Volnii, [(('aparc_aseg', getn, 0),'seg_file')])])
            freesurfer.connect(aparaseg2Volnii,"vol_label_file",lhwmROI,"in_file")
            freesurfer.connect(aparaseg2Volnii,"vol_label_file",rhwmROI,"in_file")
            freesurfer.connect(lhwmROI,"out_file",wmROI,"in_file")
            freesurfer.connect(rhwmROI,"out_file",wmROI,"operand_file")
            freesurfer.connect(aparaseg2Volnii,"vol_label_file",lhbgtROI,"in_file")
            freesurfer.connect(aparaseg2Volnii,"vol_label_file",rhbgtROI,"in_file")
            freesurfer.connect(lhbgtROI,"out_file",bgtROI,"in_file")
            freesurfer.connect(rhbgtROI,"out_file",bgtROI,"operand_file")
            freesurfer.sink_result(self.base_dir,aparaseg2Volmgz,'vol_label_file','scene')
            freesurfer.sink_result(self.base_dir,reconAll,'pial','scene')
            freesurfer.sink_result(self.base_dir,reconAll,'white','scene')
            if wfType==1 and isHippoAmygLabels:
                freesurfer.connect(reconAll,"subjects_dir",segmentHA,"subjects_dir")
                freesurfer.connect(reconAll,"subject_id",segmentHA,"subject_id")
                regex_subs=[("-T1.*.mgz",".mgz")]
                freesurfer.sink_result(self.base_dir,segmentHA,'lh_hippoAmygLabels','scene.segmentHA',regex_subs)
                freesurfer.sink_result(self.base_dir,segmentHA,'rh_hippoAmygLabels','scene.segmentHA',regex_subs)

        if check_input['mr_flair3d']:
            flair = Workflow_mo(name="flair",base_dir="./")
            flair.connect(flair_conv, "converted_files", flair_reOrient, "in_file")
            flair.connect(flair_reOrient, "out_file", flair_BET, "in_file")
            flair.connect(flair_BET, "out_file", flair2ref_FLIRT, "in_file")
            self.connect(t1, "ref_BET.out_file", flair, "flair2ref_FLIRT.reference")
            flair.sink_result(self.base_dir,flair2ref_FLIRT,'out_file','scene')

        if flair2D and check_input['op_mr_flair2d_tra']:
            flair2d_tra = Workflow_mo(name="flair2d_tra",base_dir="./")
            flair2d_tra.connect(flair2d_tra_conv, "converted_files", flair2d_tra_reOrient, "in_file")
            flair2d_tra.connect(flair2d_tra_reOrient, "out_file", flair2d_tra_BET, "in_file")
            flair2d_tra.connect(flair2d_tra_BET, "out_file", flair2d_tra2ref_FLIRT, "in_file")
            self.connect(t1, "ref_BET.out_file", flair2d_tra, "flair2d_tra2ref_FLIRT.reference")
            flair2d_tra.sink_result(self.base_dir,flair2d_tra2ref_FLIRT,'out_file','scene')

        if flair2D and check_input['op_mr_flair2d_cor']:
            flair2d_cor = Workflow_mo(name="flair2d_cor",base_dir="./")
            flair2d_cor.connect(flair2d_cor_conv, "converted_files", flair2d_cor_reOrient, "in_file")
            flair2d_cor.connect(flair2d_cor_reOrient, "out_file", flair2d_cor_BET, "in_file")
            flair2d_cor.connect(flair2d_cor_BET, "out_file", flair2d_cor2ref_FLIRT, "in_file")
            self.connect(t1, "ref_BET.out_file", flair2d_cor, "flair2d_cor2ref_FLIRT.reference")
            flair2d_cor.sink_result(self.base_dir,flair2d_cor2ref_FLIRT,'out_file','scene')

        if flair2D and check_input['op_mr_flair2d_sag']:
            flair2d_sag = Workflow_mo(name="flair2d_sag",base_dir="./")
            flair2d_sag.connect(flair2d_sag_conv, "converted_files", flair2d_sag_reOrient, "in_file")
            flair2d_sag.connect(flair2d_sag_reOrient, "out_file", flair2d_sag_BET, "in_file")
            flair2d_sag.connect(flair2d_sag_BET, "out_file", flair2d_sag2ref_FLIRT, "in_file")
            self.connect(t1, "ref_BET.out_file", flair2d_sag, "flair2d_sag2ref_FLIRT.reference")
            flair2d_sag.sink_result(self.base_dir,flair2d_sag2ref_FLIRT,'out_file','scene')


        if wfType==1 and check_input['mr_flair3d'] and DOmap:
            DOmap = Workflow_mo(name="DOmap",base_dir="./")
            DOmap.add_nodes([DOmap_FAST,DOmap_flair2mni1])
            self.connect(t1, "ref_BET.out_file",DOmap,"DOmap_FAST.in_files")
            self.connect(flair,"flair_BET.out_file",DOmap,"DOmap_flair2mni1.in_file")
            self.connect(mni1,"ref2mni1_FNIRT.fieldcoeff_file",DOmap,"DOmap_flair2mni1.field_file")
            self.connect(flair,"flair2ref_FLIRT.out_matrix_file",DOmap,"DOmap_flair2mni1.premat")
            DOmap.connect(DOmap_FAST,"restored_image",DOmap_restore2mni1,"in_file")
            self.connect(mni1,"ref2mni1_FNIRT.fieldcoeff_file",DOmap,"DOmap_restore2mni1.field_file")
            DOmap.connect([(DOmap_FAST, DOmap_gm2mni1, [(('partial_volume_files', getn, 1),'in_file')])])
            self.connect(mni1,"ref2mni1_FNIRT.fieldcoeff_file",DOmap,"DOmap_gm2mni1.field_file")
            DOmap.connect([(DOmap_FAST, DOmap_wm2mni1, [(('partial_volume_files', getn, 2),'in_file')])])
            self.connect(mni1,"ref2mni1_FNIRT.fieldcoeff_file",DOmap,"DOmap_wm2mni1.field_file")
            DOmap.connect(DOmap_flair2mni1,"out_file",DOmap_flairDIVref,"in_file")
            DOmap.connect(DOmap_restore2mni1,"out_file",DOmap_flairDIVref,"operand_file")
            DOmap.connect(DOmap_flairDIVref,"out_file",DOmap_outliers_mask,"in_file")
            DOmap.connect(DOmap_outliers_mask,"out_file",DOmap_cortexMask,"mask_file")
            DOmap.connect(DOmap_flairDIVref,"out_file",DOmap_cortexMask,"in_file")
            DOmap.connect(DOmap_cortexMask,"out_file",DOmap_gmMask,"in_file")
            DOmap.connect(DOmap_gm2mni1,"out_file",DOmap_gmMask,"mask_file")
            DOmap.connect(DOmap_cortexMask,"out_file",DOmap_wmMask,"in_file")
            DOmap.connect(DOmap_wm2mni1,"out_file",DOmap_wmMask,"mask_file")
            DOmap.connect(DOmap_gmMask,"out_file",DOmap_gm_mean,"in_file")
            DOmap.connect(DOmap_gmMask,"out_file",DOmap_gm_std,"in_file")
            DOmap.connect(DOmap_wmMask,"out_file",DOmap_wm_mean,"in_file")
            DOmap.connect(DOmap_wmMask,"out_file",DOmap_wm_std,"in_file")
            DOmap.connect(DOmap_cortexMask,"out_file",DOmap_binaryFLAIR,"in_file")
            DOmap.connect(DOmap_gm_mean,"out_stat",DOmap_binaryFLAIR,"seg_val_max")
            DOmap.connect(DOmap_wm_mean,"out_stat",DOmap_binaryFLAIR,"seg_val_min")
            DOmap.connect(DOmap_binaryFLAIR,"out_file",DOmap_convolution_flair,"in_file")
            DOmap.connect(DOmap_convolution_flair,"out_file",DOmap_junction,"in_file")
            DOmap.connect(DOmap_junction,"out_file",DOmap_junctionz,"in_file")
            DOmap.connect(DOmap_restore2mni1,"out_file",DOmap_masked_cerebellum,"in_file")
            DOmap.connect(DOmap_masked_cerebellum,"out_file",DOmap_cerebellum_mean,"in_file")
            DOmap.connect(DOmap_restore2mni1,"out_file",DOmap_restore_gmMask,"in_file")
            DOmap.connect(DOmap_gm2mni1,"out_file",DOmap_restore_gmMask,"mask_file")
            DOmap.connect(DOmap_restore_gmMask,"out_file",DOmap_normalised_GM_mask,"in_file")
            DOmap.connect(DOmap_cerebellum_mean,"out_stat",DOmap_normalised_GM_mask,"operand_value")
            DOmap.connect(DOmap_normalised_GM_mask,"out_file",DOmap_smoothed_image_extension,"in_file")
            DOmap.connect(DOmap_smoothed_image_extension,"out_file",DOmap_image_extension,"in_file")
            DOmap.connect(DOmap_image_extension,"out_file",DOmap_image_extensionz,"in_file")
            DOmap.connect(DOmap_image_extensionz,"out_file",DOmap_no_cereb_extension_z,"in_file")
            DOmap.connect(DOmap_outliers_mask,"out_file",DOmap_no_cereb_extension_z,"mask_file")
            DOmap.connect(DOmap_binaryFLAIR,"out_file",DOmap_binaryFLAIR2ref,"in_file")
            self.connect(mni1,"ref2mni1_INVWARP.inverse_warp",DOmap,"DOmap_binaryFLAIR2ref.field_file")
            self.connect(t1, "ref_BET.out_file",DOmap,"DOmap_binaryFLAIR2ref.ref_file")
            DOmap.connect(DOmap_junctionz,"out_file",DOmap_junctionz2ref,"in_file")
            self.connect(mni1,"ref2mni1_INVWARP.inverse_warp",DOmap,"DOmap_junctionz2ref.field_file")
            self.connect(t1, "ref_BET.out_file",DOmap,"DOmap_junctionz2ref.ref_file")
            DOmap.connect(DOmap_no_cereb_extension_z,"out_file",DOmap_extensionz2ref,"in_file")
            self.connect(mni1,"ref2mni1_INVWARP.inverse_warp",DOmap,"DOmap_extensionz2ref.field_file")
            self.connect(t1, "ref_BET.out_file",DOmap,"DOmap_extensionz2ref.ref_file")
            DOmap.sink_result(self.base_dir,DOmap_binaryFLAIR2ref,'out_file','scene')
            DOmap.sink_result(self.base_dir,DOmap_junctionz2ref,'out_file','scene')
            DOmap.sink_result(self.base_dir,DOmap_extensionz2ref,'out_file','scene')


        if check_input['mr_mdc']:
            mdc = Workflow_mo(name="mdc",base_dir="./")
            mdc.connect(mdc_conv, "converted_files", mdc_reOrient, "in_file")
            mdc.connect(mdc_reOrient, "out_file", mdc_BET, "in_file")
            mdc.connect(mdc_BET, "out_file", mdc2ref_FLIRT, "in_file")
            self.connect(t1, "ref_BET.out_file", mdc, "mdc2ref_FLIRT.reference")
            mdc.sink_result(self.base_dir,mdc2ref_FLIRT,'out_file','scene')

        if check_input['mr_asl']:
            asl = Workflow_mo(name="asl",base_dir="./")
            asl.connect(asl_conv, "converted_files", asl_reOrient, "in_file")
            asl.connect(asl_reOrient, "out_file", asl_SMOOTH, "in_file")
            asl.connect(asl_reOrient, "out_file",asl2ref_FLIRT,"in_file")
            self.connect(t1, "ref_BET.out_file", asl, "asl2ref_FLIRT.reference")
            asl.connect(asl_SMOOTH, "out_file",aslsmooth2ref_FLIRT,"in_file")
            self.connect(t1, "ref_BET.out_file", asl, "aslsmooth2ref_FLIRT.reference")
            asl.connect(asl2ref_FLIRT, "out_matrix_file", aslsmooth2ref_FLIRT, "in_matrix_file")
            asl.connect(aslsmooth2ref_FLIRT, "out_file", asl_mask, "in_file")
            self.connect(t1, "ref_BET.mask_file", asl, "asl_mask.mask_file")
            asl.sink_result(self.base_dir,asl_mask,'out_file','scene')
            if wfType==1:
                asl.connect(asl_mask, "out_file", asl2sym_APPLYWARP, "in_file")
                self.connect(sym, "ref2sym_FNIRT.fieldcoeff_file", asl, "asl2sym_APPLYWARP.field_file")
                asl.connect(aslsym_SWAP, "out_file", asl_swapped_APPLYWARP, "in_file")
                self.connect(sym, "swap2sym_FNIRT.fieldcoeff_file", asl, "asl_swapped_APPLYWARP.field_file")
                asl.connect(asl_AI, "out_file", asl_AI2ref, "in_file")
                self.connect(sym, "ref2sym_INVWARP.inverse_warp", asl, "asl_AI2ref.field_file")
                self.connect(t1, "ref_BET.out_file", asl, "asl_AI2ref.ref_file")
                asl.connect(asl2sym_APPLYWARP, "out_file", aslsym_SWAP, "in_file")
                asl.connect(aslsym_SWAP, "out_file", asl_AI, "in_file")
                asl.connect(asl_swapped_APPLYWARP, "out_file", asl_AI, "swapped_file")
                asl.sink_result(self.base_dir,asl_AI2ref,'out_file','scene')
            if isfreesurfer:
                asl.connect(asl_mask, "out_file", asl_surf_lh, "source_file")
                asl.connect(asl_mask, "out_file", asl_surf_rh, "source_file")
                self.connect(freesurfer, "reconAll.subjects_dir", asl, "asl_surf_lh.subjects_dir")
                self.connect(freesurfer, "reconAll.subject_id", asl, "asl_surf_lh.subject_id")
                self.connect(freesurfer, "reconAll.subjects_dir", asl, "asl_surf_rh.subjects_dir")
                self.connect(freesurfer, "reconAll.subject_id", asl, "asl_surf_rh.subject_id")
                asl.sink_result(self.base_dir,asl_surf_lh,'out_file','scene')
                asl.sink_result(self.base_dir,asl_surf_rh,'out_file','scene')
                if wfType==1:
                    asl.connect(asl_AI2ref, "out_file", aslAI_surf_lh, "source_file")
                    asl.connect(asl_AI2ref, "out_file", aslAI_surf_rh, "source_file")
                    self.connect(freesurfer, "reconAll.subjects_dir", asl, "aslAI_surf_lh.subjects_dir")
                    self.connect(freesurfer, "reconAll.subject_id", asl, "aslAI_surf_lh.subject_id")
                    self.connect(freesurfer, "reconAll.subjects_dir", asl, "aslAI_surf_rh.subjects_dir")
                    self.connect(freesurfer, "reconAll.subject_id", asl, "aslAI_surf_rh.subject_id")
                    asl.sink_result(self.base_dir,aslAI_surf_lh,'out_file','scene')
                    asl.sink_result(self.base_dir,aslAI_surf_rh,'out_file','scene')
                    asl.connect(aslsmooth2ref_FLIRT, "out_file", asl_zscore, "in_file")
                    self.connect(freesurfer, "bgtROI.out_file", asl, "asl_zscore.ROI_file")
                    asl.connect(asl_zscore, "out_file", asl_zscore_mask, "in_file")
                    self.connect(t1, "ref_BET.mask_file", asl, "asl_zscore_mask.mask_file")
                    asl.sink_result(self.base_dir,asl_zscore_mask,'out_file','scene')
                    asl.connect(asl_zscore_mask, "out_file", aslZscore_surf_lh, "source_file")
                    asl.connect(asl_zscore_mask, "out_file", aslZscore_surf_rh, "source_file")
                    self.connect(freesurfer, "reconAll.subjects_dir", asl, "aslZscore_surf_lh.subjects_dir")
                    self.connect(freesurfer, "reconAll.subject_id", asl, "aslZscore_surf_lh.subject_id")
                    self.connect(freesurfer, "reconAll.subjects_dir", asl, "aslZscore_surf_rh.subjects_dir")
                    self.connect(freesurfer, "reconAll.subject_id", asl, "aslZscore_surf_rh.subject_id")
                    asl.sink_result(self.base_dir,aslZscore_surf_lh,'out_file','scene')
                    asl.sink_result(self.base_dir,aslZscore_surf_rh,'out_file','scene')

        if check_input['pet_brain'] and check_input['ct_brain']:
            pet = Workflow_mo(name="pet",base_dir="./")
            pet.connect(pet_ct_conv, "converted_files", pet_ct2ref_FLIRT, "in_file")
            self.connect(t1, "ref_reOrient.out_file", pet, "pet_ct2ref_FLIRT.reference")
            pet.connect(pet_brain_conv, "converted_files", pet_brain2ct_FLIRT, "in_file")
            pet.connect(pet_ct_conv, "converted_files", pet_brain2ct_FLIRT, "reference")
            pet.connect(pet_ct2ref_FLIRT, "out_matrix_file", pet_convert_XFM, "in_file2")
            pet.connect(pet_brain2ct_FLIRT, "out_matrix_file", pet_convert_XFM, "in_file")
            pet.connect(pet_brain_conv, "converted_files", pet_brain2ref_FLIRT, "in_file")
            pet.connect(pet_convert_XFM, "out_file", pet_brain2ref_FLIRT, "in_matrix_file")
            self.connect(t1, "ref_reOrient.out_file", pet, "pet_brain2ref_FLIRT.reference")
            pet.connect(pet_brain2ref_FLIRT, "out_file", pet_brain_SMOOTH, "in_file")
            pet.sink_result(self.base_dir,pet_brain_SMOOTH,'out_file','scene')
            if wfType==1:
                pet.connect(pet_brain_SMOOTH, "out_file", pet_brain_sm_APPLYWARP, "in_file")
                self.connect(sym, "ref2sym_FNIRT.fieldcoeff_file", pet, "pet_brain_sm_APPLYWARP.field_file")
                pet.connect(pet_brain_sm_APPLYWARP, "out_file", petsym_SWAP, "in_file")
                pet.connect(petsym_SWAP, "out_file", pet_brain_swapped_APPLYWARP, "in_file")
                self.connect(sym, "swap2sym_FNIRT.fieldcoeff_file", pet, "pet_brain_swapped_APPLYWARP.field_file")
                pet.connect(pet_brain_sm_APPLYWARP, "out_file", pet_AI, "in_file")
                pet.connect(pet_brain_swapped_APPLYWARP, "out_file", pet_AI, "swapped_file")
                pet.connect(pet_AI, "out_file", pet_AI2ref, "in_file")
                self.connect(sym, "ref2sym_INVWARP.inverse_warp", pet, "pet_AI2ref.field_file")
                self.connect(t1, "ref_BET.out_file", pet, "pet_AI2ref.ref_file")
                pet.connect(pet_AI2ref, "out_file", pet_AI_mask, "in_file")
                self.connect(t1, "ref_BET.mask_file", pet, "pet_AI_mask.mask_file")
                pet.sink_result(self.base_dir,pet_AI_mask,'out_file','scene')
            if isfreesurfer:
                pet.connect(pet_brain_SMOOTH, "out_file", pet_surf_lh, "source_file")
                pet.connect(pet_brain_SMOOTH, "out_file", pet_surf_rh, "source_file")
                self.connect(freesurfer, "reconAll.subjects_dir", pet, "pet_surf_lh.subjects_dir")
                self.connect(freesurfer, "reconAll.subject_id", pet, "pet_surf_lh.subject_id")
                self.connect(freesurfer, "reconAll.subjects_dir", pet, "pet_surf_rh.subjects_dir")
                self.connect(freesurfer, "reconAll.subject_id", pet, "pet_surf_rh.subject_id")
                pet.sink_result(self.base_dir,pet_surf_lh,'out_file','scene')
                pet.sink_result(self.base_dir,pet_surf_rh,'out_file','scene')
                if wfType==1:
                    pet.connect(pet_AI_mask, "out_file", petAI_surf_lh, "source_file")
                    pet.connect(pet_AI_mask, "out_file", petAI_surf_rh, "source_file")
                    self.connect(freesurfer, "reconAll.subjects_dir", pet, "petAI_surf_lh.subjects_dir")
                    self.connect(freesurfer, "reconAll.subject_id", pet, "petAI_surf_lh.subject_id")
                    self.connect(freesurfer, "reconAll.subjects_dir", pet, "petAI_surf_rh.subjects_dir")
                    self.connect(freesurfer, "reconAll.subject_id", pet, "petAI_surf_rh.subject_id")
                    pet.sink_result(self.base_dir,petAI_surf_lh,'out_file','scene')
                    pet.sink_result(self.base_dir,petAI_surf_rh,'out_file','scene')
                    pet.connect(pet_brain_SMOOTH, "out_file", pet_zscore, "in_file")
                    self.connect(freesurfer, "bgtROI.out_file", pet, "pet_zscore.ROI_file")
                    pet.connect(pet_zscore, "out_file", pet_zscore_mask, "in_file")
                    self.connect(t1, "ref_BET.mask_file", pet, "pet_zscore_mask.mask_file")
                    pet.sink_result(self.base_dir,pet_zscore_mask,'out_file','scene')
                    pet.connect(pet_zscore_mask, "out_file", petZscore_surf_lh, "source_file")
                    pet.connect(pet_zscore_mask, "out_file", petZscore_surf_rh, "source_file")
                    self.connect(freesurfer, "reconAll.subjects_dir", pet, "petZscore_surf_lh.subjects_dir")
                    self.connect(freesurfer, "reconAll.subject_id", pet, "petZscore_surf_lh.subject_id")
                    self.connect(freesurfer, "reconAll.subjects_dir", pet, "petZscore_surf_rh.subjects_dir")
                    self.connect(freesurfer, "reconAll.subject_id", pet, "petZscore_surf_rh.subject_id")
                    pet.sink_result(self.base_dir,petZscore_surf_lh,'out_file','scene')
                    pet.sink_result(self.base_dir,petZscore_surf_rh,'out_file','scene')

        if wfType==0 and check_input['mr_venosa']:
            venosa = Workflow_mo(name="venosa",base_dir="./")
            venosa.connect(venosa_conv, "converted_files", venosa_reOrient, "in_file")
            if check_input['mr_venosa2']:
                venosa.connect(venosa2_conv, "converted_files", venosa2_reOrient, "in_file")
                venosa.connect(venosa_reOrient,"out_file",venosa_merge,"in1")
                venosa.connect(venosa2_reOrient,"out_file",venosa_merge,"in2")
                venosa.connect(venosa_merge, "out", venosa_check, "in_files")
            else:
                venosa.connect(venosa_reOrient, "out_file", venosa_split, "in_file")
                venosa.connect(venosa_split, "out_files", venosa_check, "in_files")
            venosa.connect(venosa_check, "out_file_modulo", venosa_BET, "in_file")
            venosa.connect(venosa_BET, "out_file", venosa_modulo2ref_FLIRT, "in_file")
            self.connect(t1, "ref_BET.out_file", venosa, "venosa_modulo2ref_FLIRT.reference")
            venosa.connect(venosa_check, "out_file_venosa", venosa_inskull_mask, "in_file")
            venosa.connect(venosa_BET, "inskull_mask_file", venosa_inskull_mask, "mask_file")
            venosa.connect(venosa_inskull_mask, "out_file", venosa2ref_FLIRT, "in_file")
            venosa.connect(venosa_modulo2ref_FLIRT, "out_matrix_file", venosa2ref_FLIRT, "in_matrix_file")
            self.connect(t1, "ref_BET.out_file", venosa, "venosa2ref_FLIRT.reference")
            venosa.sink_result(self.base_dir,venosa2ref_FLIRT,'out_file','scene')

        if check_input['mr_dti']:
            dti_preproc = Workflow_mo(name="dti_preproc",base_dir="./")
            dti_preproc.connect(dti_conv, "converted_files", dti_nodif, "in_file")
            dti_preproc.connect(dti_conv, "converted_files", dti_eddy, "in_file")
            dti_preproc.connect(dti_nodif, "roi_file", nodif_BET, "in_file")
            dti_preproc.connect(dti_eddy, "eddy_corrected", dti_dtifit, "dwi")
            dti_preproc.connect(nodif_BET, "mask_file", dti_dtifit, "mask")
            dti_preproc.connect(dti_conv, "bvecs", dti_dtifit, "bvecs")
            dti_preproc.connect(dti_conv, "bvals", dti_dtifit, "bvals")
            dti_preproc.connect(nodif_BET, "out_file", diff2ref_FLIRT, "in_file")
            self.connect(t1, "ref_BET.out_file", dti_preproc, "diff2ref_FLIRT.reference")
            dti_preproc.connect(dti_dtifit, "FA", FA2ref_FLIRT, "in_file")
            dti_preproc.connect(diff2ref_FLIRT, "out_matrix_file", FA2ref_FLIRT, "in_matrix_file")
            self.connect(t1, "ref_BET.out_file", dti_preproc, "FA2ref_FLIRT.reference")
            dti_preproc.sink_result(self.base_dir,FA2ref_FLIRT,'out_file','scene')
            if wfType==0:
                dti_preproc.connect(diff2ref_FLIRT, "out_matrix_file", ref2diff_convert, "in_file")
                dti_preproc.add_nodes([diff2mni_convert])
                dti_preproc.connect(diff2ref_FLIRT, "out_matrix_file", diff2mni_convert, "in_file2")
                dti_preproc.connect(diff2mni_convert, "out_file", mni2diff_convert, "in_file")
                dti_preproc.connect(diff2ref_FLIRT, "out_matrix_file", diff2mni_convertwarp, "premat")
                dti_preproc.connect(nodif_BET, "out_file", mni2diff_convertwarp, "reference")
                dti_preproc.connect(ref2diff_convert, "out_file", mni2diff_convertwarp, "postmat")
                dti_preproc.connect(dti_eddy, "eddy_corrected", dti_bedpostx, "dwi")
                dti_preproc.connect(nodif_BET, "mask_file", dti_bedpostx, "mask")
                dti_preproc.connect(dti_conv, "bvecs", dti_bedpostx, "bvecs")
                dti_preproc.connect(dti_conv, "bvals", dti_bedpostx, "bvals")
                self.connect(mni, "ref2mni_FLIRT.out_matrix_file", dti_preproc, "diff2mni_convert.in_file")
                self.connect(mni, "ref2mni_FNIRT.fieldcoeff_file", dti_preproc, "diff2mni_convertwarp.warp1")
                self.connect(mni, "ref2mni_INVWARP.inverse_warp", dti_preproc, "mni2diff_convertwarp.warp1")
                tractWf_list={}
                for tract in SWANiGlobalConfig['DEFAULTTRACTS'].keys():
                    if not SWANiGlobalConfig.getboolean('DEFAULTTRACTS',tract): continue
                    tractWf_list[tract]=create_probtrackx2_pipeline('tract_'+tract,tract,self.base_dir)
                    self.connect(dti_preproc, "dti_bedpostx.merged_fsamples", tractWf_list[tract], "inputnode.fsamples")
                    self.connect(dti_preproc, "nodif_BET.mask_file", tractWf_list[tract], "inputnode.mask")
                    self.connect(dti_preproc, "dti_bedpostx.merged_phsamples", tractWf_list[tract], "inputnode.phsamples")
                    self.connect(dti_preproc, "dti_bedpostx.merged_thsamples", tractWf_list[tract], "inputnode.thsamples")
                    self.connect(dti_preproc, "mni2diff_convertwarp.out_file", tractWf_list[tract], "inputnode.xfm")
                    self.connect(dti_preproc, "diff2mni_convertwarp.out_file", tractWf_list[tract], "inputnode.inv_xfm")
                    self.connect(t1, "ref_BET.out_file", tractWf_list[tract], "inputnode.ref")
                    self.connect(mni, "ref2mni_INVWARP.inverse_warp", tractWf_list[tract], "inputnode.mni2ref_warp")
