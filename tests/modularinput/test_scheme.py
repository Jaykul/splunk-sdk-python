# -*- coding: utf-8 -*-
# Copyright 2011-2013 Splunk, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from tests.modularinput.modularinput_testlib import unittest, xml_compare
from splunklib.modularinput.scheme import Scheme
from splunklib.modularinput.argument import Argument

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

class SchemeTest(unittest.TestCase):
    def test_generate_xml_from_scheme_with_default_values(self):
        """Checks the Scheme generated by creating a Scheme object and setting no fields on it.
        This test checks for sane defaults in the class."""

        scheme = Scheme("abcd")

        constructed = scheme.to_XML()
        expected = ET.parse(open("data/scheme_with_defaults.xml")).getroot()

        self.assertTrue(xml_compare(expected, constructed))

    def test_generate_xml_from_scheme(self):
        """Checks that the XML generated by a Scheme object with all its fields set and
        some arguments added matches what we expect."""

        scheme = Scheme("abcd")
        scheme.description = u"쎼 and 쎶 and <&> für"
        scheme.streamingMode = Scheme.streaming_mode_simple
        scheme.use_external_validation = "false"
        scheme.useSingleInstance = "true"

        arg1 = Argument(name="arg1")
        scheme.add_argument(arg1)

        arg2 = Argument(
            name="arg2",
            description=u"쎼 and 쎶 and <&> für",
            validation="is_pos_int('some_name')",
            data_type=Argument.data_type_number,
            required_on_edit=True,
            required_on_create=True
        )
        scheme.add_argument(arg2)

        constructed = scheme.to_XML()
        expected = ET.parse(open("data/scheme_without_defaults.xml")).getroot()

        self.assertTrue(xml_compare(expected, constructed))

    def test_generate_xml_from_argument_with_default_values(self):
        """Checks that the XML produced from an Argument class that is initialized but has no additional manipulations
        made to it is what we expect. This is mostly a check of the default values."""

        argument = Argument("some_name")

        root = ET.Element("")
        constructed = argument.add_to_document(root)

        expected = ET.parse(open("data/argument_with_defaults.xml")).getroot()

        self.assertTrue(xml_compare(expected, constructed))

    def test_generate_xml_from_argument(self):
        """Checks that the XML generated by an Argument class with all its possible values set is what we expect."""

        argument = Argument(
            name="some_name",
            description=u"쎼 and 쎶 and <&> für",
            validation="is_pos_int('some_name')",
            data_type=Argument.data_type_boolean,
            required_on_edit="true",
            required_on_create="true"
        )

        root = ET.Element("")
        constructed = argument.add_to_document(root)

        expected = ET.parse(open("data/argument_without_defaults.xml")).getroot()

        self.assertTrue(xml_compare(expected, constructed))

if __name__ == "__main__":
    unittest.main()