#!/usr/bin/env python

""" Test harness for Item. """

import unittest

import opentimelineio as otio


class FillerTester(unittest.TestCase):

    def test_str_filler(self):
        fl = otio.schema.Filler()
        self.assertMultiLineEqual(
            str(fl),
            "Filler(" +
            str(fl.name) + ", " +
            str(fl.source_range) + ", " +
            str(fl.effects) + ", " +
            str(fl.markers) + ", " +
            str(fl.metadata) +
            ")"
        )
        self.assertMultiLineEqual(
            repr(fl),
            "otio.schema.Filler("
            "name={}, "
            "source_range={}, "
            "effects={}, "
            "markers={}, "
            "metadata={}"
            ")".format(
                repr(fl.name),
                repr(fl.source_range),
                repr(fl.effects),
                repr(fl.markers),
                repr(fl.metadata),
            )
        )

        encoded = otio.adapters.otio_json.write_to_string(fl)
        decoded = otio.adapters.otio_json.read_from_string(encoded)
        self.assertEquals(fl, decoded)


class ItemTests(unittest.TestCase):

    def test_constructor(self):
        tr = otio.opentime.TimeRange(
            otio.opentime.RationalTime(0, 1),
            otio.opentime.RationalTime(10, 1)
        )
        it = otio.core.Item(name="foo", source_range=tr)
        self.assertEquals(it.source_range, tr)
        self.assertEquals(it.name, "foo")

        encoded = otio.adapters.otio_json.write_to_string(it)
        decoded = otio.adapters.otio_json.read_from_string(encoded)
        self.assertEquals(it, decoded)

    def test_duration(self):
        it = otio.core.Item()
        self.assertRaises(NotImplementedError, lambda: it.computed_duration())

        tr = otio.opentime.TimeRange(
            otio.opentime.RationalTime(0, 1),
            otio.opentime.RationalTime(10, 1)
        )
        it = otio.core.Item(source_range=tr)

        self.assertEquals(it.duration(), tr.duration)

    def test_duration_and_source_range(self):
        it = otio.core.Item()
        self.assertRaises(NotImplementedError, lambda: it.computed_duration())
        self.assertRaises(NotImplementedError, lambda: it.duration())
        self.assertEquals(None, it.source_range)

        tr = otio.opentime.TimeRange(
            otio.opentime.RationalTime(1, 1),
            otio.opentime.RationalTime(10, 1)
        )
        it2 = otio.core.Item(source_range=tr)
        self.assertRaises(NotImplementedError, lambda: it2.computed_duration())
        self.assertEquals(tr, it2.source_range)
        self.assertEquals(tr.duration, it2.duration())

    def test_serialize(self):
        tr = otio.opentime.TimeRange(
            otio.opentime.RationalTime(0, 1),
            otio.opentime.RationalTime(10, 1)
        )
        it = otio.core.Item(source_range=tr)
        encoded = otio.adapters.otio_json.write_to_string(it)
        decoded = otio.adapters.otio_json.read_from_string(encoded)
        self.assertEquals(it, decoded)

    def test_stringify(self):
        tr = otio.opentime.TimeRange(
            duration=otio.opentime.RationalTime(10, 1))
        it = otio.core.Item(source_range=tr)
        self.assertMultiLineEqual(
            str(it),
            "Item("
            "{}, "
            "{}, "
            "{}, "
            "{}, "
            "{}"
            ")".format(
                str(it.name),
                str(it.source_range),
                str(it.effects),
                str(it.markers),
                str(it.metadata),
            )
        )

        self.assertMultiLineEqual(
            repr(it),
            "otio.core.Item("
            "name={}, "
            "source_range={}, "
            "effects={}, "
            "markers={}, "
            "metadata={}"
            ")".format(
                repr(it.name),
                repr(it.source_range),
                repr(it.effects),
                repr(it.markers),
                repr(it.metadata),
            )
        )

    def test_metadata(self):
        tr = otio.opentime.TimeRange(
            duration=otio.opentime.RationalTime(10, 1))
        it = otio.core.Item(source_range=tr)
        it.metadata["foo"] = "bar"
        encoded = otio.adapters.otio_json.write_to_string(it)
        decoded = otio.adapters.otio_json.read_from_string(encoded)
        self.assertEquals(it, decoded)
        self.assertEquals(decoded.metadata["foo"], it.metadata["foo"])

    def test_add_effect(self):
        tr = otio.opentime.TimeRange(
            duration=otio.opentime.RationalTime(10, 1))
        it = otio.core.Item(source_range=tr)
        it.effects.append(
            otio.schema.Effect(
                effect_name="blur",
                metadata={
                    'amount': '100'
                }
            )
        )
        encoded = otio.adapters.otio_json.write_to_string(it)
        decoded = otio.adapters.otio_json.read_from_string(encoded)
        self.assertEquals(it, decoded)
        self.assertEquals(it.effects, decoded.effects)

    def test_add_marker(self):
        tr = otio.opentime.TimeRange(
            duration=otio.opentime.RationalTime(10, 1))
        it = otio.core.Item(source_range=tr)
        it.markers.append(
            otio.schema.Marker(
                name="test_marker",
                range=tr,
                metadata={
                    'some stuff to mark': '100'
                }
            )
        )
        encoded = otio.adapters.otio_json.write_to_string(it)
        decoded = otio.adapters.otio_json.read_from_string(encoded)
        self.assertEquals(it, decoded)
        self.assertEquals(it.markers, decoded.markers)

if __name__ == '__main__':
    unittest.main()
