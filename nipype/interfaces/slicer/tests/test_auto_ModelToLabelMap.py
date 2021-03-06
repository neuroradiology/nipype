# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from __future__ import unicode_literals
from ..surface import ModelToLabelMap


def test_ModelToLabelMap_inputs():
    input_map = dict(
        InputVolume=dict(
            argstr='%s',
            position=-3,
        ),
        OutputVolume=dict(
            argstr='%s',
            hash_files=False,
            position=-1,
        ),
        args=dict(argstr='%s', ),
        distance=dict(argstr='--distance %f', ),
        environ=dict(
            nohash=True,
            usedefault=True,
        ),
        ignore_exception=dict(
            deprecated='1.0.0',
            nohash=True,
            usedefault=True,
        ),
        surface=dict(
            argstr='%s',
            position=-2,
        ),
        terminal_output=dict(
            deprecated='1.0.0',
            nohash=True,
        ),
    )
    inputs = ModelToLabelMap.input_spec()

    for key, metadata in list(input_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(inputs.traits()[key], metakey) == value
def test_ModelToLabelMap_outputs():
    output_map = dict(OutputVolume=dict(position=-1, ), )
    outputs = ModelToLabelMap.output_spec()

    for key, metadata in list(output_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(outputs.traits()[key], metakey) == value
