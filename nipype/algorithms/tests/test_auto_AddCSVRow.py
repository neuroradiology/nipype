# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from nipype.testing import assert_equal
from nipype.algorithms.misc import AddCSVRow

def test_AddCSVRow_inputs():
    input_map = dict(col_width=dict(mandatory=True,
    usedefault=True,
    ),
    cols=dict(),
    field_headings=dict(mandatory=True,
    ),
    float_dec=dict(mandatory=True,
    usedefault=True,
    ),
    in_file=dict(mandatory=True,
    ),
    new_fields=dict(mandatory=True,
    separator=',',
    ),
    )
    inputs = AddCSVRow.input_spec()

    for key, metadata in input_map.items():
        for metakey, value in metadata.items():
            yield assert_equal, getattr(inputs.traits()[key], metakey), value

def test_AddCSVRow_outputs():
    output_map = dict(csv_file=dict(),
    )
    outputs = AddCSVRow.output_spec()

    for key, metadata in output_map.items():
        for metakey, value in metadata.items():
            yield assert_equal, getattr(outputs.traits()[key], metakey), value

