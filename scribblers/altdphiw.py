# Tai Sakuma <tai.sakuma@gmail.com>
import numpy as np

from altdphi import AltDphi

##__________________________________________________________________||
class AltDphiWrapper(object):
    """

    """

    def __init__(self,
                 pt_name, phi_name, mht_name=None, mht_phi_name=None,
                 out_attr_name_dict={}):

        self.pt_name = pt_name
        self.phi_name = phi_name
        self.mht_name = mht_name
        self.mht_phi_name = mht_phi_name
        self.out_attr_name_dict = out_attr_name_dict

    def __repr__(self):
        name_value_pairs = (
            ('pt_name', self.pt_name),
            ('phi_name',  self.phi_name),
            ('mht_name',    self.mht_name),
            ('mht_phi_name',  self.mht_phi_name),
            ('out_attr_name_dict',  self.out_attr_name_dict),
        )
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{}={!r}'.format(n, v) for n, v in name_value_pairs]),
        )

    def begin(self, event):
        self.out = {k: [ ] for k in self.out_attr_name_dict.keys()}
        self._attach_to_event(event)

    def _attach_to_event(self, event):
        for k, v in self.out_attr_name_dict.items():
            setattr(event, v, self.out[k])

    def event(self, event):
        self._attach_to_event(event)

        pt = np.array(getattr(event, self.pt_name))
        phi = np.array(getattr(event, self.phi_name))

        mht = None
        if self.mht_name is not None:
            mht = getattr(event, self.mht_name)[0]

        mht_phi = None
        if self.mht_phi_name is not None:
            mht_phi = getattr(event, self.mht_phi_name)[0]

        alt = AltDphi(pt=pt, phi=phi, mht=mht, mht_phi=mht_phi)

        for k in self.out_attr_name_dict.keys():
            v = getattr(alt, k)
            try:
                self.out[k][:] = v
            except TypeError:
                self.out[k][:] = [v]

    def end(self):
        self.out = None

##__________________________________________________________________||
