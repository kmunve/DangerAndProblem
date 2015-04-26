# -*- coding: utf-8 -*-
__author__ = 'ragnarekker'

import makeFiles as MF
import getRegObs as GRO

# Two sets of folder references: windows based og unix based.
#data_folder = "Datafiles\\"
data_folder = "Datafiles/"

if __name__ == "__main__":

    # This makes a full report

    data_output_filename = '{0}Alle skredproblemer.csv'.format(data_folder)

    regions = list(range(106, 134))

    for r in regions:
        data = GRO.get_all_problems(r)
        MF.save_problems(data, data_output_filename)

    a = 1

