# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from __future__ import unicode_literals
from ..registration import RegisterAVItoTalairach


def test_RegisterAVItoTalairach_inputs():
    input_map = dict(
        args=dict(argstr='%s', ),
        environ=dict(
            nohash=True,
            usedefault=True,
        ),
        ignore_exception=dict(
            deprecated='1.0.0',
            nohash=True,
            usedefault=True,
        ),
        in_file=dict(
            argstr='%s',
            mandatory=True,
            position=0,
        ),
        out_file=dict(
            argstr='%s',
            position=3,
            usedefault=True,
        ),
        subjects_dir=dict(),
        target=dict(
            argstr='%s',
            mandatory=True,
            position=1,
        ),
        terminal_output=dict(
            deprecated='1.0.0',
            nohash=True,
        ),
        vox2vox=dict(
            argstr='%s',
            mandatory=True,
            position=2,
        ),
    )
    inputs = RegisterAVItoTalairach.input_spec()

    for key, metadata in list(input_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(inputs.traits()[key], metakey) == value
def test_RegisterAVItoTalairach_outputs():
    output_map = dict(
        log_file=dict(usedefault=True, ),
        out_file=dict(),
    )
    outputs = RegisterAVItoTalairach.output_spec()

    for key, metadata in list(output_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(outputs.traits()[key], metakey) == value
