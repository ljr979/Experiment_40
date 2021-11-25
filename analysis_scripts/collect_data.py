
import os, re
import pandas as pd
import numpy as np
from loguru import logger
import glob
import shutil

#change these for experiment
input_folder = 'raw_data/'
output_folder = 'imagejresults/'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

#can change based on proteins in experiment
hsp_colocalised = 'aB-c_coloc_traj'
hsp_noncolocal = 'aB-c_non-coloc_traj'
client_colocalised = 'CLIC_coloc_traj'
client_noncolocal ='CLIC_non-coloc_traj'


    #change these for the experiment you're using
folders = {
    #  '20201209_110525_171experiment 14 aB x linked at 5uM/Trajectories/':('crosslinked-aBc-5uM/non-coloc/', hsp_noncolocal), 

    #  '20201209_125020_554exp 14 xlinked at 20 uM/Trajectories/':('crosslinked-aBc-20uM/non-coloc/', hsp_noncolocal), 

    # 'non-colocalised aB-c/': ('noncrosslinked-aBc/non-coloc/', hsp_noncolocal,),
    # 'colocalised aB-c/': ('noncrosslinked-aBc/coloc/', hsp_colocalised,),

    # 'CLIC UNHEATED 13012021/Trajectories/':('CLIC_not-heated/non-coloc/', 'client_noncolocal'), 
    # 'CLIC HEATED 13012021/Trajectories/':('CLIC_heated/non-coloc/', 'client_noncolocal')
        

        #t=0
        '20211105 experiment38_CLIC_hsp27+t0/Trajectories/Coloc/Hsp/': ('aBc/zero-aBc-01/coloc/', hsp_colocalised),
        '20211105 experiment38_CLIC_hsp27+t0/Trajectories/non-coloc/Hsp/': ('aBc/zero-aBc-01/non-coloc/', hsp_noncolocal),
        '20211105 experiment38_CLIC_hsp27+t0/Trajectories/Coloc/Client/': ('CLIC/zero-CLIC-01/coloc/', client_colocalised),
        '20211105 experiment38_CLIC_hsp27+t0/Trajectories/non-coloc/Client/': ('CLIC/zero-CLIC-01/non-coloc/', client_noncolocal),

        #t=20
        '20211105 experiment38_CLIC_hsp27+t20/Trajectories/Coloc/Hsp/': ('aBc/20min-aBc-01/coloc/', hsp_colocalised),
        '20211105 experiment38_CLIC_hsp27+t20/Trajectories/non-coloc/Hsp/': ('aBc/20min-aBc-01/non-coloc/', hsp_noncolocal),
        '20211105 experiment38_CLIC_hsp27+t20/Trajectories/Coloc/Client/': ('CLIC/20min-CLIC-01/coloc/', client_colocalised),
        '20211105 experiment38_CLIC_hsp27+t20/Trajectories/non-coloc/Client/': ('CLIC/20min-CLIC-01/non-coloc/', client_noncolocal),

        #20_2
        # '20211105 experiment38_CLIC_hsp27+t20_2/Trajectories/Coloc/Hsp/': ('20min-aBc-01/coloc/', hsp_colocalised),
        # '20211105 experiment38_CLIC_hsp27+t20_2/Trajectories/non-coloc/Hsp/': ('20min-aBc-01/non-coloc/', hsp_noncolocal),
        # '20211105 experiment38_CLIC_hsp27+t20_2/Trajectories/Coloc/Client/': ('20min-CLIC-01/coloc/', client_colocalised),
        # '20211105 experiment38_CLIC_hsp27+t20_2/Trajectories/non-coloc/Client/': ('20min-CLIC-01/non-coloc/', client_noncolocal),

        #t=40
        '20211105 experiment38_CLIC_hsp27+t40/Trajectories/Coloc/Hsp/': ('aBc/40min-aBc-01/coloc/', hsp_colocalised),
        '20211105 experiment38_CLIC_hsp27+t40/Trajectories/non-coloc/Hsp/': ('aBc/40min-aBc-01/non-coloc/', hsp_noncolocal),
        '20211105 experiment38_CLIC_hsp27+t40/Trajectories/Coloc/Client/': ('CLIC/40min-CLIC-01/coloc/', client_colocalised),
        '20211105 experiment38_CLIC_hsp27+t40/Trajectories/non-coloc/Client/': ('CLIC/40min-CLIC-01/non-coloc/', client_noncolocal),

        #t=60
        '20211105 experiment38_CLIC_hsp27+t60/Trajectories/Coloc/Hsp/': ('aBc/60min-aBc-01/coloc/', hsp_colocalised),
        '20211105 experiment38_CLIC_hsp27+t60/Trajectories/non-coloc/Hsp/': ('aBc/60min-aBc-01/non-coloc/', hsp_noncolocal),
        '20211105 experiment38_CLIC_hsp27+t60/Trajectories/Coloc/Client/': ('CLIC/60min-CLIC-01/coloc/', client_colocalised),
        '20211105 experiment38_CLIC_hsp27+t60/Trajectories/non-coloc/Client/': ('CLIC/60min-CLIC-01/non-coloc/', client_noncolocal),

        #60_2
        # '20211105 experiment38_CLIC_hsp27+t60_2/Trajectories/Coloc/Hsp/': ('60min-aBc-01/coloc/', hsp_colocalised),
        # '20211105 experiment38_CLIC_hsp27+t60_2/Trajectories/non-coloc/Hsp/': ('60min-aBc-01/non-coloc/', hsp_noncolocal),
        # '20211105 experiment38_CLIC_hsp27+t60_2/Trajectories/Coloc/Client/': ('60min-CLIC-01/coloc/', client_colocalised),
        # '20211105 experiment38_CLIC_hsp27+t60_2/Trajectories/non-coloc/Client/': ('60min-CLIC-01/non-coloc/', client_noncolocal),
        #t=4h
        '20211105 experiment38_CLIC_hsp27+t4h/Trajectories/Coloc/Hsp/': ('aBc/4h-aBc-01/coloc/', hsp_colocalised),
        '20211105 experiment38_CLIC_hsp27+t4h/Trajectories/non-coloc/Hsp/': ('aBc/4h-aBc-01/non-coloc/', hsp_noncolocal),
        '20211105 experiment38_CLIC_hsp27+t4h/Trajectories/Coloc/Client/': ('CLIC/4h-CLIC-01/coloc/', client_colocalised),
        '20211105 experiment38_CLIC_hsp27+t4h/Trajectories/non-coloc/Client/': ('CLIC/4h-CLIC-01/non-coloc/', client_noncolocal),


        # #4h_2
        # '20211105 experiment38_CLIC_hsp27+t4h_2/Trajectories/Coloc/Hsp/': ('4h-aBc-01/coloc/', hsp_colocalised),
        # '20211105 experiment38_CLIC_hsp27+t4h_2/Trajectories/non-coloc/Hsp/': ('4h-aBc-01/non-coloc/', hsp_noncolocal),
        # '20211105 experiment38_CLIC_hsp27+t4h_2/Trajectories/Coloc/Client/': ('4h-CLIC-01/coloc/', client_colocalised),
        # '20211105 experiment38_CLIC_hsp27+t4h_2/Trajectories/non-coloc/Client/': ('4h-CLIC-01/non-coloc/', client_noncolocal),

        #t=7h

        '20211105 experiment38_7h/Trajectories/Coloc/Hsp/': ('aBc/7h-aBc-01/coloc/', hsp_colocalised),
        '20211105 experiment38_7h/Trajectories/non-coloc/Hsp/': ('aBc/7h-aBc-01/non-coloc/', hsp_noncolocal),
        '20211105 experiment38_7h/Trajectories/Coloc/Client/': ('CLIC/7h-CLIC-01/coloc/', client_colocalised),
        '20211105 experiment38_7h/Trajectories/non-coloc/Client/': ('CLIC/7h-CLIC-01/non-coloc/', client_noncolocal),




        }

for old_folder, (new_folder, filetype) in folders.items():
        old_files = [filename for filename in os.listdir(f'{input_folder}{old_folder}') if '.csv' in filename]
        if not os.path.exists(f'{output_folder}{new_folder}'):
            os.makedirs(f'{output_folder}{new_folder}')
        for x, filename in enumerate(old_files): 
            shutil.copyfile(f'{input_folder}{old_folder}{filename}', f'{output_folder}{new_folder}{filetype}{x}.csv')






