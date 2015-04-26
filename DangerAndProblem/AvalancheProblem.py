# -*- coding: utf-8 -*-
__author__ = 'raek'

from fEncoding import *

class AvalancheProblem:
    def __init__(self, region_id_inn, region_name_inn, date_inn, order_inn, cause_name_inn, source_inn):
        '''
        The AvalancheProblem object is usefull since there are 3 different tables to get regObs-data from and 2 tables
        from forecasts. Thus avalanache problems are saved in 5 ways. The structure of this object is based on the
        "latest" model and the other/older ways to save avalanche problems on may be mapped to these.

        Parameters part of the constructor:
        :param region_id_inn:       [int]       Region ID is as given in ForecastRegionKDV.
        :param region_name_inn:     [String]    Region name as given in ForecastRegionKDV.
        :param date_inn:            [Date]      Date for avalanche problem.
        :param order_inn:           [int]       The order of the avalanche problem*.
        :param cause_name_inn:      [String]    Avalanche cause. For newer problems this as given in AvalancheCauseKDV.
        :param source_inn:          [String]    The source of the data. Normally 'Observation' og 'Forecast'.

        *   Order should be indexed from 0 (main problem) and up, but I see that they often start on higher indexes
            and don't always have a step of +1. A rule is that the higher the order the higher the priority.

        Other variables:
        regid               [int]
        municipal_name      [String]
        aval_type           [String]
        aval_size           [String]
        aval_trigger        [String]
        aval_probability    [String]
        aval_distribution   [String]        # named AvalPropagation in regObs
        problem_combined    [String]
        regobs_view         [String]
        url = None          [String]
        metadata = []       [list with dictionaries [{},{},..] ]

        '''

        self.region_id = region_id_inn
        self.region_name = remove_norwegian_letters(region_name_inn)
        self.date = date_inn
        self.order = order_inn
        self.cause_name = remove_norwegian_letters(cause_name_inn)
        self.source = remove_norwegian_letters(source_inn)

        self.regid = None               # int
        self.municipal_name = None      # string
        self.aval_type = None           # string
        self.aval_size = None           # string
        self.aval_trigger = None        # string
        self.aval_probability = None    # string
        self.aval_distribution = None   # string
        self.problem_combined = None    # string
        self.regobs_view = None         # string
        self.url = None                 # string
        self.metadata = []              # list with dictionariues [{},{},..]

    def set_municipal(self, municipal_inn):
        try:
            self.municipal_name = remove_norwegian_letters(municipal_inn)
        except ValueError:
            print "Got ValueError on setting municipal name on {0} for {1}."\
                .format(self.date, self.region_name)
        except:
            print "Got un expected error on setting municipal name on {0} for {1}."\
                .format(self.date, self.region_name)

    def set_regid(self, regid_inn):
        self.regid = regid_inn

    def set_url(self, url_inn):
        self.url = url_inn

    def set_aval_type(self, aval_type_inn):
        self.aval_type = aval_type_inn

    def set_aval_size(self, aval_size_inn):
        aval_size = remove_norwegian_letters(aval_size_inn)
        if aval_size != "Ikke gitt":
            self.aval_size = aval_size

    def set_aval_trigger(self, aval_trigger_inn):
        self.aval_trigger = aval_trigger_inn

    def set_aval_probability(self, aval_probability_inn):
        self.aval_probability = aval_probability_inn

    def set_aval_distribution(self, aval_distribution_inn):
        self.aval_distribution = aval_distribution_inn

    def set_problem_combined(self, problem_inn):
        self.problem_combined = remove_norwegian_letters(problem_inn)

    def set_regobs_view(self, view_inn):
        self.regobs_view = view_inn

