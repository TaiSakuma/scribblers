# Tai Sakuma <tai.sakuma@gmail.com>
import numpy as np

##__________________________________________________________________||
class Len(object):
    def __init__(self, src_name, out_name):
        self.src_name = src_name
        self.out_name = out_name

        self._repr_pairs = [
            ('src_name', self.src_name),
            ('out_name', self.out_name),
        ]

    def __repr__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{}={!r}'.format(n, v) for n, v in self._repr_pairs]),
        )

    def __str__(self):
        nwidth = max(len(n) for n, _ in self._repr_pairs)
        nwidth += 4
        return '{}:\n{}'.format(
            self.__class__.__name__,
            '\n'.join(['{:>{}}: {!r}'.format(n, nwidth, v) for n, v in self._repr_pairs]),
        )

    def begin(self, event):
        self.out = [ ]
        self._attach_to_event(event)

    def _attach_to_event(self, event):
        setattr(event, self.out_name, self.out)

    def event(self, event):
        self._attach_to_event(event)

        try:
            self.out[:] = [getattr(event, self.src_name).GetEntriesFast()]
            # for TClonesArray
            return
        except AttributeError:
            pass

        self.out[:] = [len(getattr(event, self.src_name))]

##__________________________________________________________________||
class FuncOnNumpyArrays(object):
    def __init__(self, src_arrays, out_name, func):
        self.src_arrays = src_arrays
        self.out_name = out_name
        self.func = func

    def __repr__(self):
        name_value_pairs = (
            ('src_arrays', self.src_arrays),
            ('out_name', self.out_name),
            ('func', self.func),
        )
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{}={!r}'.format(n, v) for n, v in name_value_pairs]),
        )

    def begin(self, event):
        self.out = [ ]
        self._attach_to_event(event)

    def _attach_to_event(self, event):
        setattr(event, self.out_name, self.out)

    def event(self, event):
        self._attach_to_event(event)
        out = self.func(*[np.array(getattr(event, n)) for n in self.src_arrays])
        try:
            self.out[:] = out
        except TypeError:
            self.out[:] = [out]

    def end(self):
        self.func = None

##__________________________________________________________________||
