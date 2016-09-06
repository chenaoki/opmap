import sys
import os
from opmap.opmap import VmemMap

if len(sys.argv) != 2:
    print('Please enter diredtory name')
    exit()

dir_name = sys.argv[1]
dir_name = os.path.join("./", dir_name)
param_vmem = {
        'path' : 'default_path',
        'cam_type'  : 'max',
        'image_width' : 256,
        'image_height' : 256,
        'frame_start' : 0,
        'frame_end' : 1000
    }
param_vmem["path"] = dir_name

vmem = VmemMap(**param_vmem)
vmem.setDiffRange(diff_min=5)

while True:
    vmem.showMovie()
    if raw_input() == 'y':
        exit()

