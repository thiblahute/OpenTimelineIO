#!/usr/bin/env python

import unittest

import opentimelineio as otio


class ClipTests(unittest.TestCase):

    def test_cons(self):
        name = "test"
        rt = otio.opentime.RationalTime(5, 24)
        tr = otio.opentime.TimeRange(rt, rt)
        tt = otio.opentime.TimeTransform(offset=otio.opentime.RationalTime())
        mr = otio.media_reference.External(
            available_range=otio.opentime.TimeRange(
                rt,
                otio.opentime.RationalTime(10, 24)
            ),
            target_url="/var/tmp/test.mov"
        )

        cl = otio.schema.Clip(
            name=name,
            media_reference=mr,
            source_range=tr,
            transform=tt,
            # transition_in
            # transition_out
        )
        self.assertEquals(cl.name, name)
        self.assertEquals(cl.source_range, tr)
        self.assertEquals(cl.transform, tt)
        self.assertEquals(cl.media_reference, mr)
        self.assertEquals(cl.source_range, tr)

        encoded = otio.adapters.otio_json.write_to_string(cl)
        decoded = otio.adapters.otio_json.read_from_string(encoded)
        self.assertEquals(cl, decoded)

    def test_each_clip(self):
        cl = otio.schema.Clip(name="test_clip")
        self.assertEquals(list(cl.each_clip()), [cl])

    def test_str(self):
        cl = otio.schema.Clip(name="test_clip")

        self.assertMultiLineEqual(
            str(cl),
            'Clip("test_clip", MissingReference(), None, None)'
        )
        self.assertMultiLineEqual(
            repr(cl),
            'otio.schema.Clip('
            "name='test_clip', "
            'media_reference=otio.media_reference.MissingReference(), '
            'transform=None, '
            'source_range=None'
            ')'
        )

    def test_str_with_filepath(self):
        cl = otio.schema.Clip(
            name="test_clip",
            media_reference=otio.media_reference.External(
                "/var/tmp/foo.mov"
            )
        )
        self.assertMultiLineEqual(
            str(cl),
            'Clip("test_clip", External("/var/tmp/foo.mov"), None, None)'
        )
        self.assertMultiLineEqual(
            repr(cl),
            'otio.schema.Clip('
            "name='test_clip', "
            "media_reference=otio.media_reference.External("
            "target_url='/var/tmp/foo.mov'"
            "), "
            'transform=None, '
            'source_range=None'
            ')'
        )

if __name__ == '__main__':
    unittest.main()
