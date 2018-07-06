# Tai Sakuma <tai.sakuma@gmail.com>
import json

##__________________________________________________________________||
class InCertifiedLumiSections(object):
    def __init__(
            self, json_path,
            run_attr_name='run', lumi_attr_name='lumi',
            out_attr_name='inCertifiedLumiSections'
    ):

        self._repr_pairs = [
            ('json_path', json_path),
            ('run_attr_name', run_attr_name),
            ('lumi_attr_name', lumi_attr_name),
            ('out_attr_name', out_attr_name),
        ]

        self.json_path = json_path
        self.run_attr_name = run_attr_name
        self.lumi_attr_name = lumi_attr_name
        self.out_attr_name = out_attr_name

        self.json_dict = json.load(open(json_path))

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
        self.vals = [ ]
        self._attach_to_event(event)
        self.run_lumi_pairs = self.expand_json_dict(self.json_dict)

    def expand_json_dict(self, json_dict):
        ret = [ ]
        for run in sorted(json_dict.keys()):
            for lumi_range in json_dict[run]:
                lumis = range(lumi_range[0], lumi_range[1] + 1)
                ret.extend([(int(run), ls) for ls in lumis])
        # e.g., ret = [(256941, 137), (256941, 138), (256941, 139)]
        return set(ret)

    def _attach_to_event(self, event):
        setattr(event, self.out_attr_name, self.vals)

    def event(self, event):
        self._attach_to_event(event)
        run = getattr(event, self.run_attr_name)[0]
        lumi = getattr(event, self.lumi_attr_name)[0]
        self.vals[:] = [(run, lumi) in self.run_lumi_pairs]

    def end(self):
        self.run_lumi_pairs = None
        self.json_dict = None

##__________________________________________________________________||
