# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from __future__ import unicode_literals
from ..convert import NIfTIDT2Camino


def test_NIfTIDT2Camino_inputs():
    input_map = dict(
        args=dict(argstr='%s', ),
        bgmask=dict(argstr='-bgmask %s', ),
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
            argstr='-inputfile %s',
            mandatory=True,
            position=1,
        ),
        lns0_file=dict(argstr='-lns0 %s', ),
        out_file=dict(
            argstr='> %s',
            genfile=True,
            position=-1,
        ),
        s0_file=dict(argstr='-s0 %s', ),
        scaleinter=dict(argstr='-scaleinter %s', ),
        scaleslope=dict(argstr='-scaleslope %s', ),
        terminal_output=dict(
            deprecated='1.0.0',
            nohash=True,
        ),
        uppertriangular=dict(argstr='-uppertriangular %s', ),
    )
    inputs = NIfTIDT2Camino.input_spec()

    for key, metadata in list(input_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(inputs.traits()[key], metakey) == value
def test_NIfTIDT2Camino_outputs():
    output_map = dict(out_file=dict(), )
    outputs = NIfTIDT2Camino.output_spec()

    for key, metadata in list(output_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(outputs.traits()[key], metakey) == value
