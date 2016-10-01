#!/usr/bin/env python3

from concept_map import ConceptMap


class CsvMap:

    def __init__(self, filename):
        import csv
        ## Parse csv into Python object
        d = {}
        with open(filename) as f:
            _ = f.readline()
            keyword = None
            for i in csv.reader(f):
                if i[0]:
                    keyword = i[0]
                    d[keyword] = []
                else:
                    d[keyword].append(i)

        ## read entries from Python object to construct a map
        self.name = d['Concept map name:'][0][1]
        self.question = d['Focus Question:'][0][1]

        self.attribute = {}  # (concept1, link, concept2): (supplied, correct, important, present-string, absent-string)
        
        self.map = ConceptMap()
        self.map.add_concepts(i[1] for i in d['Concepts:'])
        self.map.add_links(i[1] for i in d['Links:'])
        
        b = lambda x: True if x.lower() == 'yes' else False
        for i in d['Propositions:']:
            self.map.add_proposition((i[1], i[2], i[3]))
            # # # # (concept1, link, concept2) = (supplied, correct, important, present-string, absent-string)
            self.attribute[(i[1], i[2], i[3])] = (b(i[4]), b(i[5]), b(i[6]), i[7], i[8])

    def __repr__(self):
        l = []
        l.append(str(self.name))
        l.append(str(self.question))
        l.append(repr(self.map))
        return '\n'.join(l)
