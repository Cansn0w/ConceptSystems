

class ValidationError(Exception):
    pass


class ConceptMap:

    def __init__(self):
        self.concepts = set()  # {concept1, concept2, ...}
        self.links = set()  # {link1, link2, ...}
        self.prop = set()  # {(concept1, link1, concept2), ...}
        
    def _validate_prop(self, proposition):
        if proposition[0] not in self.concepts:
            raise ValidationError(str(proposition[0]) + ' is not a given concept.')
        if proposition[2] not in self.concepts:
            raise ValidationError(str(proposition[2]) + ' is not a given concept.')
        if proposition[0] == proposition[2]:
            raise ValidationError('Concept cannot link to itself.')
        if proposition[1] not in self.links:
            raise ValidationError(str(proposition[1]) + ' is not a given link.')

    # adders
    def add_concept(self, concept):
        self.concepts.add(concept)
        
    def add_link(self, link):
        self.links.add(link)
        
    def add_proposition(self, proposition):
        self._validate_prop(proposition)
        self.prop.add(proposition)

    # bulk adders
    def add_concepts(self, *concepts):
        self.concepts.update(set(concepts))

    def add_links(self, *links):
        self.links.update(set(links))

    def add_propositions(self, *propositions):
        """Add propositions as tuple(concept1, link, concept2)."""
        for i in propositions:
            self._validate_prop(i)
        self.prop.update(set(propositions))

    # utils
    def diff(self, other):
        diff_this = {
            'concepts': self.concepts.difference(other.concepts),
            'links': self.links.difference(other.links),
            'propositions': self.prop.difference(other.prop),
            }
        diff_other = {
            'concepts': other.concepts.difference(self.concepts),
            'links': other.links.difference(self.links),
            'propositions': other.prop.difference(self.prop),
            }
        return diff_this, diff_other

