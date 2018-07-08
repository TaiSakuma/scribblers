# Tai Sakuma <tai.sakuma@gmail.com>
import numpy as np

from altdphi import AltDphi

##__________________________________________________________________||
class LheHTnoT(object):

    def __repr__(self):
        name_value_pairs = ()
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{}={!r}'.format(n, v) for n, v in name_value_pairs]),
        )

    def begin(self, event):
        self.out = [ ]
        self._attach_to_event(event)

    def _attach_to_event(self, event):
        event.lheHTnoT = self.out

    def event(self, event):
        self._attach_to_event(event)

        pt = np.array(event.GenPart_pt)
        status = np.array(event.GenPart_status)
        abspdgid = np.absolute(np.array(event.GenPart_pdgId))
        motheridx = np.array(event.GenPart_genPartIdxMother)
        b = (status == 23) & (((1 <= abspdgid) & (abspdgid <= 6)) | (21 == abspdgid))
        idx = np.where(b)[0]
        idx_from_top_quark = self._is_from_top_quark(idx, abspdgid, motheridx)
        idx = np.setdiff1d(idx, idx_from_top_quark)
        lheHTnoT = np.sum(pt[idx])
        self.out[:] = [lheHTnoT]

    def _is_from_top_quark(self, idx, abspdgid, motheridx):
        idx_for_top_quarks = idx[abspdgid[idx] == 6]
        idx_for_non_top_quarks = np.setdiff1d(idx, idx_for_top_quarks)
        idx_for_mother_of_non_top_quarks = motheridx[idx_for_non_top_quarks]
        idx_for_mother_of_non_top_quarks = idx_for_mother_of_non_top_quarks[idx_for_mother_of_non_top_quarks >= 0]
        if idx_for_mother_of_non_top_quarks.size == 0:
            return idx_for_top_quarks
        idx_for_mother_from_top_quarks = self._is_from_top_quark(idx_for_mother_of_non_top_quarks, abspdgid, motheridx)
        idx_from_toq_quarks = np.where(np.isin(motheridx, idx_for_mother_from_top_quarks))[0]
        idx_from_toq_quarks = idx_from_toq_quarks[np.isin(idx_from_toq_quarks, idx_for_non_top_quarks)]
        idx_from_toq_quarks = np.union1d(idx_for_top_quarks, idx_from_toq_quarks)
        return idx_from_toq_quarks

    def end(self):
        self.out = None

##__________________________________________________________________||
class NLheLeptons(object):

    def __repr__(self):
        name_value_pairs = ()
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{}={!r}'.format(n, v) for n, v in name_value_pairs]),
        )

    def begin(self, event):
        self.out = [ ]
        self._attach_to_event(event)

    def _attach_to_event(self, event):
        event.nLheLeptons = self.out

    def event(self, event):
        self._attach_to_event(event)

        status = np.array(event.GenPart_status)
        abspdgid = np.absolute(np.array(event.GenPart_pdgId))
        b = (status == 23) & ( (11 == abspdgid) | (13 == abspdgid) | (15 == abspdgid))
        self.out[:] = [abspdgid[b].size]

##__________________________________________________________________||
