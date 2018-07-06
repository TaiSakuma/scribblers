# Tai Sakuma <tai.sakuma@gmail.com>

##__________________________________________________________________||
class ObjectSelection(object):
    """select objects

    """
    def __init__(self, in_obj, out_obj, selection):
        self.in_obj_name = in_obj
        self.out_obj_name = out_obj
        self.selection = selection

        self._repr_pairs = [
            ('in_obj',    self.in_obj_name),
            ('out_obj',   self.out_obj_name),
            ('selection', self.selection),
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

        if hasattr(self.selection, 'begin'):
            self.selection.begin(event)

    def _attach_to_event(self, event):
        setattr(event, self.out_obj_name, self.out)

    def event(self, event):
        self._attach_to_event(event)

        self.out[:] = [o for o in getattr(event, self.in_obj_name) if self.selection(o)]

    def end(self):
        if hasattr(self.selection, 'end'):
            self.selection.end()
        self.out = None

##__________________________________________________________________||
