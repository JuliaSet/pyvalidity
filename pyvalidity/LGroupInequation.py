from typing import Set

from MultiplicativelyClosedSet import MultiplicativelyClosedSet
from PartialOrder import PartialOrder
from TruncatedFreeGroup import TruncatedFreeGroup
from pyvalidity.LGroupTerm import LGroupTerm, Atom, Join


class LGroupInequation:
    # LGroupInequation(s, t) stands for s <= t
    def __init__(self, left_hand_side: LGroupTerm, right_hand_side: LGroupTerm):
        self.left_hand_side = left_hand_side
        self.right_hand_side = right_hand_side

    # LGroupInequation(s, t) returns ts^{-1}, which is the thing that "should be positive"
    def _relevant_cnf(self) -> LGroupTerm:
        return self.right_hand_side.prod(self.left_hand_side.inv()).cnf()

    def is_valid(self) -> bool:
        cnf_set = _cnf_to_set(self._relevant_cnf())
        for candidate in cnf_set:
            max_length = _longest_element(cnf_set)
            candidate_terms = {t.atom for t in candidate}
            closed = MultiplicativelyClosedSet(candidate_terms, max_length)
            generators = {x.positive_literals() for x in candidate_terms}
            truncated = TruncatedFreeGroup(max_length, generators)
            partial = PartialOrder(closed, truncated)
            if partial.extends_to_total_order():
                return False
        # none of the meetands extend
        return True


def _longest_element(things):
    return max([x.length for x in things])


def _cnf_to_set(cnf: LGroupTerm) -> Set[Set[LGroupTerm]]:
    # cnf is now of one of the following forms:
    # (i)   a meet of joins of atoms
    # (ii)  a join of atoms
    # (iii) an atom

    # (i)
    if isinstance(cnf, Atom):
        return {{cnf}}
    if isinstance(cnf, Join):
        return {cnf.joinands}
    return {t.joinands for t in cnf.meetands}