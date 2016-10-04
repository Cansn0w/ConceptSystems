#!/usr/bin/env python3


def expect(err, func, *args):
    try:
        func(*args)
    except err:
        pass
    else:
        raise AssertionError


def test_map():
    from .concept_map import ValidationError, ConceptMap as M

    m = M()

    m.add_concept(1)
    m.add_concept(2)
    m.add_link('a')
    m.add_proposition((1, 'a', 2))

    assert 1 in m.concepts
    assert 2 in m.concepts
    assert 'a' in m.links
    assert (1, 'a', 2) in m.prop
    expect(ValidationError, m.add_proposition, (1, 'a', 1))
    expect(ValidationError, m.add_proposition, (1, 'a', 3))
    expect(ValidationError, m.add_proposition, (1, 'b', 2))


    m = M()

    m.add_concepts((1, 2, 3))
    m.add_links(('a', 'b'))
    m.add_propositions(((1, 'a', 2), (2, 'b', 3)))
    
    m.add_concepts((1, 2, 3))
    m.add_links(('a', 'b'))
    m.add_propositions(((1, 'a', 2), (2, 'b', 3)))

    assert 1 in m.concepts
    assert 2 in m.concepts
    assert 3 in m.concepts
    assert 'a' in m.links
    assert 'b' in m.links
    assert (1, 'a', 2) in m.prop
    assert (2, 'b', 3) in m.prop
    expect(ValidationError, m.add_proposition, ((1, 'a', 1)))
    expect(ValidationError, m.add_proposition, ((1, 'a', 4)))
    expect(ValidationError, m.add_proposition, ((1, 'c', 2)))
    

    a = M()
    b = M()
    
    a.add_concept(1)
    a.add_concept(2)
    a.add_link('a')
    a.add_proposition((1, 'a', 2))
    
    b.add_concept(1)
    b.add_concept(2)
    b.add_link('a')
    b.add_proposition((1, 'a', 2))

    assert a.diff(b) == b.diff(a)
    assert a.diff(b) == ({'concepts': set(), 'links': set(), 'propositions': set()}, {'concepts': set(), 'links': set(), 'propositions': set()})

    a.add_concept(0)
    a.add_proposition((1, 'a', 0))
    b.add_concept(4)
    b.add_proposition((1, 'a', 4))

    assert a.diff(b) == ({'links': set(), 'concepts': {0}, 'propositions': {(1, 'a', 0)}}, {'links': set(), 'concepts': {4}, 'propositions': {(1, 'a', 4)}})

    
if __name__ == '__main__':
    test_map()
    
    
