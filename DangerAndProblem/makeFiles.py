__author__ = 'ragnarekker'

import os.path

def save_problems(problems, file_path):
    '''

    :param problems:
    :param file_path:
    :return:
    '''


    if os.path.exists(file_path) == False:
       l = open(file_path, 'w')
       l.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\n'
               .format('Date', 'RegionID', 'Region', 'Source',
               'Order', 'Cause', 'Size',
               'More on the avalanche problem', 'View in regObs', 'URL'))
    else:
        l = open(file_path, 'a')

    for p in problems:
        l.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\n'.format(
            p.date,
            p.region_id,
            p.region_name,
            p.source,
            p.order,
            p.cause_name,
            p.aval_size,
            p.problem_combined,
            p.regobs_view,
            p.url))
    l.close()