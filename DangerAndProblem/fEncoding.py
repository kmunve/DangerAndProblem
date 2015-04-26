# -*- coding: utf-8 -*-
# __author__ = 'ragnarekker'


def remove_norwegian_letters(nameInn):

    if nameInn is None:
        return None


    name = nameInn.strip()
    if u'å' in name:
        name = name.replace(u'å', 'aa').encode('ascii', 'ignore')
    if u'ø' in name:
        name = name.replace(u'ø', 'oe').encode('ascii', 'ignore')
    if u'æ' in name:
        name = name.replace(u'æ', 'ae').encode('ascii', 'ignore')

    name = name.encode('ascii', 'ignore')

    return name.rstrip()



def add_norwegian_letters(nameInn):

    name = nameInn
    if u'ae' in name:
        name = name.replace(u'ae', 'æ'.decode('utf8', 'ignore'))
    if u'oe' in name:
        name = name.replace(u'oe', 'ø'.decode('utf8', 'ignore'))
    if u'aa' in name:
        name = name.replace(u'aa', 'å'.decode('utf8', 'ignore'))

    return name
