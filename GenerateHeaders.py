import xml.etree.ElementTree as ET

# svd parser
from SVDParser.SVD import SVD
# processor (svd to header data)
from Processors.Processors import process

# import header element classes
from Processors.HeaderElement import *

# process svd file by the xml parser
root = ET.parse('STM32L4x6_v1r1.svd').getroot()
# convert to dictionary
device = SVD.process(root)


# peripheral name prefix
periph_prefix = "TIM"
# try with tim1
dma1 = device["peripherals"][periph_prefix + "17"]
# this is where we flatten all the registers
regs = dict()


# need to flatten the hierarchy to get just the register list
def flatten_registers(collection: dict, regs):
    # got a cluster situation?
    if 'clusters' in collection:
        # clusters may come in multiples
        for cluster in collection['clusters']:
            # go down recursively since clusters may be nested!
            flatten_registers(collection['clusters'][cluster], regs)
    # got a register situation?
    if 'registers' in collection:
        # registers may come in multiples
        for register in collection['registers']:
            # show it's name
            regs[register] = collection['registers'][register]


# flatten the structure
flatten_registers(dma1, regs)

# output list
output = []

# process all fields within gathered registers
for reg_name, reg in regs.items():
    # process all fields
    for field_name, field in reg['fields'].items():
        # define label elements
        def_label_list = [periph_prefix, reg_name, field_name]
        # use the upper case and join by underscore
        def_label_name_str = "_".join(s.upper() for s in def_label_list)

        # process entire field mask
        def_value_mask = ((1 << field['bit_width']) - 1) << field['bit_offset']
        # convert to string that will hold the hex value
        def_value_mask_str = f"({def_value_mask:#010x})"

        # add entire mask element to the list
        output += [HeaderElementDefine(def_label_name_str, def_value_mask_str)]
        # add define for every bit within field
        if field['bit_width'] > 1:
            # process every bit
            for i in range(field['bit_width']):
                # convert to label name
                def_label_name_bit_str = def_label_name_str + "_" + str(i)
                # convert to label value
                def_value_mask_bit = 1 << (i + field['bit_offset'])
                # convert to string
                def_value_mask_bit_str = f"({def_value_mask_bit:#010x})"
                # add bit element to the output list
                output += [HeaderElementDefine(def_label_name_bit_str,
                                               def_value_mask_bit_str)]

for o in output:
    print(o)
