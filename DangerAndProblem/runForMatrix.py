# -*- coding: utf-8 -*-
__author__ = 'raek'

import getRegObs as GRO
import getForecastApi as GFA
import makePickle as RP
import pylab as P

# Two sets of folder references: windows based og unix based.
#data_folder = "Datafiles\\"
#plot_folder = "Plotfiles\\"
data_folder = "Datafiles/"
plot_folder = "Plotfiles/"

def pickle_warnings(regions, date_from, date_to, pickle_file_name):
    '''
    All warnings and problems are selected from regObs or the avalanche api and neatly pickel'd for later use.

    :param regions:            list []
    :param date_from:          string as 'yyyy-mm-dd'
    :param date_to:            string as 'yyyy-mm-dd'
    :param pickle_file_name:   filename including directory as string
    :return:
    '''

    warnings = []

    for r in regions:

        # get all warning and problems for this region and then loop though them joining them on date
        __warnings = GFA.get_warnings(r, date_from, date_to)
        __name = GRO.get_forecast_region_name(r)
        __problems = GRO.get_problems_from_AvalancheWarnProblemV(__name, r, date_from, date_to)

        print '{0} problems found for {1}'.format(len(__problems), __name)

        for i in range(0, len(__warnings), 1):
            for j in range(0, len(__problems), 1):
                if __warnings[i].date == __problems[j].date:
                    __warnings[i].add_problem(__problems[j])

        warnings = warnings + __warnings

    RP.pickle_anything(warnings, pickle_file_name)

def pickle_data_set(warnings, file_name, use_ikke_gitt):
    '''
    Takes the warnings data set which is a list of class AvalancheDanger objects and makes a nested dictionary data set
    of if. This makes the data set easier to distribute and use if the AvalancheDanger and AvalancheProblem classes
    are missing.

    The data set also includes information on what the xKDV tables in regObs contains and preferred colors when
    plotting.

    :param warnings:        list of AvalancheDanger objects
    :param file_name:       filename to pickle the data to
    :param use_ikke_gitt:   If I dont whant to use the ID = 0 (Ikke gitt) values they can be omitted all in all.

    :return:
    '''

    level_list = []
    size_list = []
    trigger_list = []
    probability_list = []
    distribution_list = []

    for w in warnings:
        if w.danger_level > 0 and len(w.avalanche_problems) > 0:
            level_list.append(w.danger_level)
            size_list.append(w.avalanche_problems[0].aval_size)
            trigger_list.append(w.avalanche_problems[0].aval_trigger)
            probability_list.append(w.avalanche_problems[0].aval_probability)
            distribution_list.append(w.avalanche_problems[0].aval_distribution)

    level_keys = GRO.get_kdv('AvalancheDangerKDV').keys()
    size_keys = GRO.get_kdv('DestructiveSizeKDV').values()
    triggers_keys = GRO.get_kdv('AvalTriggerSimpleKDV').values()
    probability_keys = GRO.get_kdv('AvalProbabilityKDV').values()
    distribution_keys = GRO.get_kdv('AvalPropagationKDV').values()

    level_colors = ['0.5','#ccff66', '#ffff00', '#ff9900', '#ff0000', 'k']

    if use_ikke_gitt == False:
        level_keys.pop(0)
        size_keys.pop(0)
        triggers_keys.pop(0)
        probability_keys.pop(0)
        distribution_keys.pop(0)

        level_colors.pop(0)

    data_set = {'level': {'values': level_list, 'keys': level_keys, 'colors':level_colors},
                'size': {'values': size_list, 'keys': size_keys, 'colors':['0.7']},
                'trigger': {'values': trigger_list, 'keys': triggers_keys, 'colors':['0.7']},
                'probability': {'values': probability_list, 'keys': probability_keys, 'colors':['0.7']},
                'distribution': {'values': distribution_list, 'keys': distribution_keys, 'colors':['0.7']}}

    RP.pickle_anything(data_set, file_name)

def plot_histogram(title, data_series, data_labels, filename):
    '''
    Takes a data series and plots the count of each event given in data labels list.
    The plot i saved to file.

    :param title:           string
    :param data_series:     a list of values. Type of values must match elements in data labels.
    :param data_labels:     list of values. Types must match elements in the data series.
    :param filename:        String. filename including path

    :return:
    '''

    # Figure dimensions
    fig = P.figure(figsize=(12, 5))
    P.clf()
    P.title(title)

    # look up and count each occurence in the dataset
    level_distribution = []
    for dl in data_labels:
        level_distribution.append(data_series.count(dl))

    # add coordinates to a vline plot
    P.vlines(0, 0, 0, lw=20)                # add whitespace to the left
    x = range(1, len(data_labels)+1, 1)     # odd numbering because of white spaces
    for i in x:
        P.vlines(i, 0, data_series.count(data_labels[i-1]), lw=30)
    P.vlines(i+1, 0, 0, lw=20)              # add whitespace to the right

    x_ticks = data_labels
    P.xticks(x, x_ticks)

    # This saves the figure til file
    P.savefig(filename)
    P.close(fig)

def plot_histogram_on_danger_level(title, key, data_set, file_name):
    '''
    Messy but generic for its use. Plots a histogram on the requested data series for each danger level.

    :param title:       string
    :param key:         which series in data_set is to be plotted.
    :param data_set:    a data set as made in the method pickle_data_set in thins file.
    :param file_name:   String. filename including path.

    :return:
    '''

    title = file_name

    data_keys = data_set[key]['keys']
    data_values = data_set[key]['values']

    level_keys = data_set['level']['keys']
    level_values = data_set['level']['values']
    level_colors =  data_set['level']['colors']

    # this list is expanded as it loops trough the for loops below. Index given by [level_keys]
    numbers = []
    for i in range(0, len(data_values), 1):
        for j in range(0, len(level_keys), 1):
            numbers.append([])
            if level_values[i] == level_keys[j]:
                # collect all data events on the danger level they occur
                numbers[j].append(data_values[i])

    # this nested list ins indexed [level_keys][data_keys]. I is expanded as it loops trough the for loops below.
    more_numbers = []
    for i in range(0, len(level_keys), 1):
        more_numbers.append([])
        for j in range(0, len(data_keys), 1):
            # count occurrences of data pr danger level
            more_numbers[i].append([numbers[i].count(data_keys[j]), level_colors[i]])

    # Figure dimensions
    fig = P.figure(figsize=(20, 10))
    P.clf()
    P.title(title)

    # prepare data set for plotting
    plot_numbers = [[0,'0']]                            # give som space from the y-axis. Add an empty item.
    for i in range(0, len(data_keys), 1):
        for j in range(0, len(level_keys), 1):
            plot_numbers.append(more_numbers[j][i])

    # add coordinates to a vline plot
    x = range(0, len(data_keys)*len(level_keys)+1, 1)   # +1 because of the empty item in plot_numbers
    for i in x:
        P.vlines(i, 0, plot_numbers[i][0], lw=25, color=plot_numbers[i][1])

    # Dynamic location of labels
    ticks_place = []
    ticks_place.append(3)
    for dk in data_keys:
        if ticks_place[-1] <= len(x):
            ticks_place.append(ticks_place[-1]+len(level_keys))

    P.xticks(ticks_place, data_keys)

    # This saves the figure til file
    P.savefig(file_name)
    P.close(fig)

    return

if __name__ == "__main__":

    #regions_kdv = GRO.get_kdv("ForecastRegionKDV")
    regions = list(range(106, 134))     # ForecastRegionTID = 133 is the last and is Salten

    date_from = "2014-12-01"
    date_to = "2015-06-01"
    pickle_warnings_file_name = '{0}{1}'.format(data_folder, 'runForMatrix warnings.pickle')
    pickle_data_set_file_name = '{0}{1}'.format(data_folder, 'runForMatrix data set.pickle')


    pickle_warnings(regions, date_from, date_to, pickle_warnings_file_name)
    warnings = RP.unpickle_anything(pickle_warnings_file_name)
    # pickle_data_set(warnings, pickle_data_set_file_name, False)
    data_set = RP.unpickle_anything(pickle_data_set_file_name)

    plot_histogram('frequency of levels', data_set['level']['values'], data_set['level']['keys'],
                '{0}Histogram of levels {1} to {2}.png'.format(plot_folder, date_from, date_to))
    plot_histogram('frequency of sizes', data_set['size']['values'], data_set['size']['keys'],
                '{0}Histogram of sizes {1} to {2}.png'.format(plot_folder, date_from, date_to))
    plot_histogram('frequency of triggers', data_set['trigger']['values'], data_set['trigger']['keys'],
                '{0}Histogram of triggers {1} to {2}.png'.format(plot_folder, date_from, date_to))
    plot_histogram('frequency of probabilities', data_set['probability']['values'], data_set['probability']['keys'],
                '{0}Histogram of probabilities {1} to {2}.png'.format(plot_folder, date_from, date_to))
    plot_histogram('frequency of distribution', data_set['distribution']['values'], data_set['distribution']['keys'],
                '{0}Histogram of distribution {1} to {2}.png'.format(plot_folder, date_from, date_to))

    plot_histogram_on_danger_level('', 'size', data_set,
                '{0}Histogram of size on danger level {1} to {2}.png'.format(plot_folder, date_from, date_to))
    plot_histogram_on_danger_level('', 'trigger', data_set,
                '{0}Histogram of triggers on danger level {1} to {2}.png'.format(plot_folder, date_from, date_to))
    plot_histogram_on_danger_level('', 'probability', data_set,
                '{0}Histogram of probabilities on danger level {1} to {2}.png'.format(plot_folder, date_from, date_to))
    plot_histogram_on_danger_level('', 'distribution', data_set,
                '{0}Histogram of distribution on danger level {1} to {2}.png'.format(plot_folder, date_from, date_to))


    a = 1

