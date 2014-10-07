# -*- coding: utf-8 -*-
import collections
from nose.tools import eq_, ok_

import amo
import amo.tests
from addons.addongenerator import generate_addon_data


class AddonGeneratorTests(amo.tests.TestCase):
    def test_tinyset(self):
        size = 4
        data = list(generate_addon_data(size))
        eq_(len(data), size)
        # Names are unique.
        eq_(len(set(addonname for addonname, cat in data)), size)
        # Size is smaller than name list, so no names end in numbers.
        ok_(not any(addonname[-1].isdigit() for addonname, cat in data))

    def test_smallset(self):
        size = 60
        data = list(generate_addon_data(size))
        eq_(len(data), size)
        ctr = collections.defaultdict(int)
        for addonname, category in data:
            ctr[category.slug] += 1
        eq_(set(ctr.values()), set([4]))
        eq_(len(set(addonname for addonname, cat in data)), size)
        ok_(not any(addonname[-1].isdigit() for addonname, cat in data))

    def test_bigset(self):
        size = 300
        data = list(generate_addon_data(size))
        eq_(len(data), size)
        ctr = collections.defaultdict(int)
        for addonname, cat in data:
            ctr[cat] += 1
        # Addons are spread between categories evenly - the difference between
        # the largest and smallest category is less than 2.
        ok_(max(ctr.values()) - min(ctr.values()) < 2)
        eq_(len(set(addonname for addonname, cat in data)), size)
