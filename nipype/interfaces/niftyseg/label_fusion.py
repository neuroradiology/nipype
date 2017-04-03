# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

"""
The fusion module provides higher-level interfaces to some of the operations
that can be performed with the seg_LabFusion command-line program.

Change directory to provide relative paths for doctests
    >>> import os
    >>> filepath = os.path.dirname( os.path.realpath( __file__ ) )
    >>> datadir = os.path.realpath(os.path.join(filepath, '../../testing/data'))
    >>> os.chdir(datadir)
"""

from builtins import str
import os
import warnings

from ..base import (TraitedSpec, File, traits, isdefined, CommandLineInputSpec,
                    NipypeInterfaceError)
from .base import NiftySegCommand, get_custom_path
from ...utils.filemanip import load_json, save_json


warn = warnings.warn
warnings.filterwarnings('always', category=UserWarning)


class LabelFusionInput(CommandLineInputSpec):
    """Input Spec for LabelFusion."""
    in_file = File(argstr='-in %s',
                   exists=True,
                   mandatory=True,
                   position=1,
                   desc='Filename of the 4D integer label image.')

    template_file = File(exists=True,
                         desc='Registered templates (4D Image)')

    file_to_seg = File(exists=True,
                       mandatory=True,
                       desc='Original image to segment (3D Image)')

    mask_file = File(argstr='-mask %s',
                     exists=True,
                     desc='Filename of the ROI for label fusion')

    out_file = File(argstr='-out %s',
                    genfile=True,
                    desc='Output consensus segmentation')

    prob_flag = traits.Bool(desc='Probabilistic/Fuzzy segmented image',
                            argstr='-outProb')

    desc = 'Verbose level [0 = off, 1 = on, 2 = debug] (default = 0)'
    verbose = traits.Enum('0', '1', '2',
                          desc=desc,
                          argstr='-v %s')

    desc = 'Only consider non-consensus voxels to calculate statistics'
    unc = traits.Bool(desc=desc, argstr='-unc')

    classifier_type = traits.Enum('STEPS', 'STAPLE', 'MV', 'SBA',
                                  argstr='-%s',
                                  mandatory=True,
                                  position=2,
                                  desc='Type of Classifier Fusion.')

    desc = "Gaussian kernel size in mm to compute the local similarity"
    kernel_size = traits.Float(desc=desc)

    template_num = traits.Int(desc='Number of labels to use')

    # STAPLE and MV options
    sm_ranking = traits.Enum('ALL', 'GNCC', 'ROINCC', 'LNCC',
                             argstr='-%s',
                             usedefault=True,
                             position=3,
                             desc='Ranking for STAPLE and MV')

    dilation_roi = traits.Int(desc='Dilation of the ROI ( <int> d>=1 )')

    # STAPLE and STEPS options
    desc = 'Proportion of the label (only for single labels).'
    proportion = traits.Float(argstr='-prop %s', desc=desc)

    desc = 'Update label proportions at each iteration'
    prob_update_flag = traits.Bool(desc=desc, argstr='-prop_update')

    desc = 'Value of P and Q [ 0 < (P,Q) < 1 ] (default = 0.99 0.99)'
    set_pq = traits.Tuple(traits.Float, traits.Float,
                          argstr='-setPQ %f %f',
                          desc=desc)

    mrf_value = traits.Float(argstr='-MRF_beta %f',
                             desc='MRF prior strength (between 0 and 5)')

    desc = 'Maximum number of iterations (default = 15).'
    max_iter = traits.Int(argstr='-max_iter %d', desc=desc)

    desc = 'If <float> percent of labels agree, then area is not uncertain.'
    unc_thresh = traits.Float(argstr='-uncthres %f', desc=desc)

    desc = 'Ratio for convergence (default epsilon = 10^-5).'
    conv = traits.Float(argstr='-conv %f', desc=desc)


class LabelFusionOutput(TraitedSpec):
    """Output Spec for LabelFusion."""
    out_file = File(exists=True, desc='image written after calculations')


class LabelFusion(NiftySegCommand):
    """Interface for executable seg_LabelFusion from NiftySeg platform using
    type STEPS as classifier Fusion.

    For source code, see http://cmictig.cs.ucl.ac.uk/wiki/index.php/NiftySeg
    For Documentation, see:
        http://cmictig.cs.ucl.ac.uk/wiki/index.php/NiftySeg_documentation

    Examples
    --------
    >>> from nipype.interfaces import niftyseg
    >>> node = niftyseg.LabelFusion()
    >>> node.inputs.in_file = 'im1.nii'
    >>> node.inputs.kernel_size = 2.0
    >>> node.inputs.file_to_seg = 'im2.nii'
    >>> node.inputs.template_file = 'im3.nii'
    >>> node.inputs.template_num = 2
    >>> node.inputs.classifier_type = 'STEPS'
    >>> node.cmdline  # doctest: +ELLIPSIS +ALLOW_UNICODE
    'seg_LabFusion -in im1.nii -STEPS 2.000000 2 im2.nii im3.nii -out \
.../im1_steps.nii'

    """
    _cmd = get_custom_path('seg_LabFusion')
    input_spec = LabelFusionInput
    output_spec = LabelFusionOutput
    _suffix = '_label_fused'

    def _format_arg(self, opt, spec, val):
        """Convert input to appropriate format for seg_maths."""
        # Remove options if not STAPLE or STEPS as fusion type:
        if opt in ['proportion', 'prob_update_flag', 'set_pq', 'mrf_value',
                   'max_iter', 'unc_thresh', 'conv'] and\
           self.inputs.classifier_type not in ['STAPLE', 'STEPS']:
            return ''

        if opt == 'sm_ranking':
            return self.get_staple_args(val)

        # Return options string if STEPS:
        if opt == 'classifier_type' and val == 'STEPS':
            return self.get_steps_args()

        return super(LabelFusion, self)._format_arg(opt, spec, val)

    def get_steps_args(self):
        if not isdefined(self.inputs.template_file):
            err = "LabelFusion requires a value for input 'template_file' \
when 'classifier_type' is set to 'STEPS'."
            raise NipypeInterfaceError(err)
        if not isdefined(self.inputs.kernel_size):
            err = "LabelFusion requires a value for input 'kernel_size' when \
'classifier_type' is set to 'STEPS'."
            raise NipypeInterfaceError(err)
        if not isdefined(self.inputs.template_num):
            err = "LabelFusion requires a value for input 'template_num' when \
'classifier_type' is set to 'STEPS'."
            raise NipypeInterfaceError(err)
        return "-STEPS %f %d %s %s" % (self.inputs.kernel_size,
                                       self.inputs.template_num,
                                       self.inputs.file_to_seg,
                                       self.inputs.template_file)

    def get_staple_args(self, ranking):
        classtype = self.inputs.classifier_type
        if classtype not in ['STAPLE', 'MV']:
            return None

        if ranking == 'ALL':
            return '-%s' % ranking

        if not isdefined(self.inputs.template_file):
            err = "LabelFusion requires a value for input 'tramplate_file' \
when 'classifier_type' is set to '%s' and 'sm_ranking' is set to '%s'."
            raise NipypeInterfaceError(err % (classtype, ranking))
        if not isdefined(self.inputs.template_num):
            err = "LabelFusion requires a value for input 'template-num' when \
'classifier_type' is set to '%s' and 'sm_ranking' is set to '%s'."
            raise NipypeInterfaceError(err % (classtype, ranking))

        if ranking == 'GNCC':
            if not isdefined(self.inputs.template_num):
                err = "LabelFusion requires a value for input 'template_num' \
when 'classifier_type' is set to '%s' and 'sm_ranking' is set to '%s'."
                raise NipypeInterfaceError(err % (classtype, ranking))

            return "-%s %d %s %s" % (ranking,
                                     self.inputs.template_num,
                                     self.inputs.file_to_seg,
                                     self.inputs.template_file)

        elif ranking == 'ROINCC':
            if not isdefined(self.inputs.dilation_roi):
                err = "LabelFusion requires a value for input 'dilation_roi' \
when 'classifier_type' is set to '%s' and 'sm_ranking' is set to '%s'."
                raise NipypeInterfaceError(err % (classtype, ranking))

            elif self.inputs.dilation_roi < 1:
                err = "The 'dilation_roi' trait of a LabelFusionInput \
instance must be an integer >= 1, but a value of '%s' was specified."
                raise NipypeInterfaceError(err % self.inputs.dilation_roi)

            return "-%s %d %d %s %s" % (ranking,
                                        self.inputs.dilation_roi,
                                        self.inputs.template_num,
                                        self.inputs.file_to_seg,
                                        self.inputs.template_file)
        elif ranking == 'LNCC':
            if not isdefined(self.inputs.kernel_size):
                err = "LabelFusion requires a value for input 'kernel_size' \
when 'classifier_type' is set to '%s' and 'sm_ranking' is set to '%s'."
                raise NipypeInterfaceError(err % (classtype, ranking))

            return "-%s %f %d %s %s" % (ranking,
                                        self.inputs.kernel_size,
                                        self.inputs.template_num,
                                        self.inputs.file_to_seg,
                                        self.inputs.template_file)

    def _list_outputs(self):
        outputs = self.output_spec().get()
        if isdefined(self.inputs.out_file):
            outputs['out_file'] = self.inputs.out_file
        else:
            outputs['out_file'] = self._gen_filename('out_file')
        return outputs

    def _gen_filename(self, name):
        _suffix = '_%s' % self.inputs.classifier_type.lower()
        if name == 'out_file':
            return self._gen_fname(self.inputs.in_file, suffix=_suffix)
        return None


class CalcTopNCCInputSpec(CommandLineInputSpec):
    """Input Spec for CalcTopNCC."""
    in_file = File(argstr='-target %s',
                   exists=True,
                   mandatory=True,
                   desc='Target file',
                   position=1)

    num_templates = traits.Int(argstr='-templates %s',
                               mandatory=True,
                               position=2,
                               desc='Number of Templates')

    in_templates = traits.List(File(exists=True),
                               argstr="%s",
                               position=3,
                               mandatory=True)

    top_templates = traits.Int(argstr='-n %s',
                               mandatory=True,
                               position=4,
                               desc='Number of Top Templates')

    mask_file = File(argstr='-mask %s',
                     exists=True,
                     mandatory=False,
                     desc='Filename of the ROI for label fusion')


class CalcTopNCCOutputSpec(TraitedSpec):
    """Output Spec for CalcTopNCC."""
    out_files = traits.Any(File(exists=True))


class CalcTopNCC(NiftySegCommand):
    """Interface for executable seg_CalcTopNCC from NiftySeg platform.

    Examples
    --------
    >>> from nipype.interfaces import niftyseg
    >>> node = niftyseg.CalcTopNCC()
    >>> node.inputs.in_file = 'im1.nii'
    >>> node.inputs.num_templates = 2
    >>> node.inputs.in_templates = ['im2.nii', 'im3.nii']
    >>> node.inputs.top_templates = 1
    >>> node.cmdline  # doctest: +ALLOW_UNICODE
    'seg_CalcTopNCC -target im1.nii -templates 2 im2.nii im3.nii -n 1'

    """
    _cmd = get_custom_path('seg_CalcTopNCC')
    _suffix = '_topNCC'
    input_spec = CalcTopNCCInputSpec
    output_spec = CalcTopNCCOutputSpec

    def aggregate_outputs(self, runtime=None, needed_outputs=None):
        outputs = self._outputs()
        # local caching for backward compatibility
        outfile = os.path.join(os.getcwd(), 'CalcTopNCC.json')
        if runtime is None:
            try:
                out_files = load_json(outfile)['files']
            except IOError:
                return self.run().outputs
        else:
            out_files = []
            for line in runtime.stdout.split('\n'):
                if line:
                    values = line.split()
                    if len(values) > 1:
                        out_files.append([str(val) for val in values])
                    else:
                        out_files.extend([str(val) for val in values])
            if len(out_files) == 1:
                out_files = out_files[0]
            save_json(outfile, dict(files=out_files))
        outputs.out_files = out_files
        return outputs
