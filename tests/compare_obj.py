# Tai Sakuma <tai.sakuma@gmail.com>
import numbers

##__________________________________________________________________||
def cmp_obj_list_almost_equal(list1, list2, rtol=1e-05, atol=1e-08):
    if not len(list1) == len(list2):
        return False
    for obj1, obj2 in zip(list1, list2):
        if not cmp_obj_almost_equal(obj1, obj2, rtol=rtol, atol=atol):
            return False
    return True

def cmp_obj_almost_equal(obj1, obj2, rtol=1e-05, atol=1e-08):
    # use the same formula as in
    # https://docs.scipy.org/doc/numpy-1.14.0/reference/generated/numpy.isclose.html

    attrs1 = list(obj1._attrdict.keys())
    attrs2 = list(obj2._attrdict.keys())

    if not attrs1 == attrs2:
        return False

    for attr in attrs2:
        v1 = getattr(obj1, attr)
        v2 = getattr(obj2, attr)
        if v1 == v2:
            continue
        if isinstance(v2, numbers.Integral):
            return False
        if isinstance(v2, numbers.Real):
            if abs(v1 - v2) > (atol + rtol * abs(v2)):
                return False
    return True

##__________________________________________________________________||
