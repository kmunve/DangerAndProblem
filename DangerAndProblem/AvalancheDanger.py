# -*- coding: utf-8 -*-
__author__ = 'ragnarekker'

class AvalancheDanger:
    def __init__(self, region_regobs_id_inn, region_name_inn, data_table_inn, date_inn, danger_level_inn, danger_level_name_inn):
        '''
        AvalancheDanger object since there are 3 different tables to get regObs-data from and one from the forecast

        :param region_regobs_id_inn:
        :param region_name_inn:
        :param data_table_inn:
        :param date_inn:
        :param danger_level_inn:
        :param danger_level_name_inn:
        :return:

        Other variables:
        metadata:                       [{key:value}, ..]
        avalanche_problems:             [AvalancheProblem, ..]
        '''

        if region_regobs_id_inn < 100: # makes sure that it is regObs ID used in this program
            region_regobs_id_inn = region_regobs_id_inn + 100

        self.region_regobs_id = region_regobs_id_inn    # [int]
        self.region_name = region_name_inn              # [String]
        self.data_table = data_table_inn                # [String]
        self.date = date_inn                            # [date]
        self.danger_level = danger_level_inn            # [Int]
        self.danger_level_name = danger_level_name_inn  # [String]

        self.metadata = []                              # list with dictionariues [{},{},..]
        self.avalanche_problems = []

    def add_problem(self, problem_inn):
        self.avalanche_problems.append(problem_inn)
        self.avalanche_problems.sort(key=lambda problems: problems.order)       # make sure sort lowest order first
