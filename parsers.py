#!/usr/bin/env python3

# from util.concept_map import ConceptMap
from concept_map import ConceptMap
import json

class CsvMap:

    def __init__(self, filename):
        import csv
        ## Parse csv into Python object
        d = {}
        with open(filename, encoding='utf-8', errors='ignore') as f:
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
            if b(i[5]) and b(i[6]):
                self.map.add_proposition((i[1], i[2], i[3]))
            # # # # (concept1, link, concept2) = (supplied, correct, important, present-string, absent-string)
            self.attribute[(i[1], i[2], i[3])] = (b(i[4]), b(i[5]), b(i[6]), i[7], i[8])

    def __repr__(self):
        l = []
        l.append('Name: ' + str(self.name))
        l.append(str(self.question))
        l.append('Concepts: ' + ', '.join(self.map.concepts))
        l.append('Links: ' + ', '.join(self.map.links))
        l.append('Propositions:')
        l.extend(str(i[0]) + ' -- ' +str(i[1]) + ' -- ' +str(i[2]) + ' :\t' + str(self.attribute[(i[0], i[1], i[2])]) for i in self.map.prop)
        return '\n'.join(l)


def inner_join(table1, col1, table2, col2):
    ret = []
    for i in table1:
        for j in table2:
            if i[col1] == j[col2]:
                ret.append(i + j)
    return ret

class CxlMap:

    def __init__(self, filename):
        
        ## Parse CmapTools exported cxl file into concet map object
        import xml.etree.ElementTree as ET
        m = ET.parse(filename).getroot().find('{http://cmap.ihmc.us/xml/cmap/}map')

        concepts = {}
        links = {}
        
        self.map = ConceptMap()
        for i in m.find('{http://cmap.ihmc.us/xml/cmap/}concept-list'):
            concepts[i.attrib['id']] = i.attrib['label']
            self.map.add_concept(i.attrib['label'])

        self.attribute = {}
        for i in m.find('{http://cmap.ihmc.us/xml/cmap/}concept-appearance-list'):
            self.attribute[concepts[i.attrib['id']]] = (int(i.attrib['x']), int(i.attrib['y']))
            
        for i in m.find('{http://cmap.ihmc.us/xml/cmap/}linking-phrase-list'):
            links[i.attrib['id']] = i.attrib['label']
            self.map.add_link(i.attrib['label'])

        connections = []
        for i in m.find('{http://cmap.ihmc.us/xml/cmap/}connection-list'):
            connections.append((i.attrib['from-id'], i.attrib['to-id']))
        connections = inner_join(connections, 1, connections, 0)

        for i in connections:
            if i[0] in links:
                continue
            self.map.add_proposition((concepts[i[0]], links[i[1]], concepts[i[3]]))
            
    def __repr__(self):
        l = []
        l.append('Concepts: ' + ', '.join(i + (' (%d, %d)' % self.attribute[i]) for i in self.map.concepts))
        l.append('Links: ' + ', '.join(self.map.links))
        l.append('Propositions:')
        l.extend(str(i[0]) + ' -- ' +str(i[1]) + ' -- ' +str(i[2]) for i in self.map.prop)
        return '\n'.join(l)


class Marker:

    def __init__(self, csvmap, cxlmap):
        self.csv = csvmap
        self.cxl = cxlmap

    def _parse(self):
        dcsv, dcxl = self.csv.map.diff(self.cxl.map)
        ret = {}
        ret['missing concepts'] = list(dcsv['concepts'])
        ret['concepts'] = list({
            'name': i,
            'x': self.cxl.attribute[i][0],
            'y': self.cxl.attribute[i][1],
            'correct': i not in dcxl['concepts']
            } for i in self.cxl.map.concepts)
        
        ret['missing links'] = list(dcsv['links'])
        ret['links'] = list({
            'name': i,
            'correct': i not in dcxl['links']
            } for i in self.cxl.map.links)

        def _(frm, link, to, supplied, correct, important, present):
            return {'from': frm, 'to': to, 'link': link, 'supplied': supplied, 'correct': correct, 'important': important, 'present string': present}
        a = self.csv.attribute
        ret['present porpsitions'] = list(_(i[0], i[1], i[2], *(a[i][:-1])) if i in a else _(i[0], i[1], i[2], False, None, False, '') for i in self.cxl.map.prop)
        ret['absent porpsitions'] = list({'from': i[0], 'link': i[1], 'to': i[2], 'absent string': a[i][-1]} for i in dcsv['propositions'])
        return ret

    def to_json(self, *args, **kwargs):
        import json
        return json.dumps(self._parse(), *args, **kwargs)

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) != 3:
        print('Usage:\n\tpython parsers.py map.csv map.cxl')
        exit()

    csv = CsvMap(sys.argv[1])
    cxl = CxlMap(sys.argv[2])
    print(Marker(csv, cxl).to_json(indent=2))
