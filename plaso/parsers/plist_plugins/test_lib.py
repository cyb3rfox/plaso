#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2014 The Plaso Project Authors.
# Please see the AUTHORS file for details on individual authors.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Plist plugin related functions and classes for testing."""

from dfvfs.lib import definitions
from dfvfs.path import factory as path_spec_factory
from dfvfs.resolver import resolver as path_spec_resolver

from plaso.lib import queue
from plaso.parsers import test_lib


class PlistPluginTestCase(test_lib.ParserTestCase):
  """The unit test case for a plist plugin."""

  def _ParsePlistFileWithPlugin(
      self, parser_object, plugin_object, path, plist_name,
      knowledge_base_values=None):
    """Parses a file using the parser and plugin object.

    Args:
      parser_object: the parser object.
      plugin_object: the plugin object.
      path: the path of the file to parse.
      plist_name: the name of the plist to parse.
      knowledge_base_values: optional dict containing the knowledge base
                             values. The default is None.

    Returns:
      An event object queue consumer object (instance of
      TestEventObjectQueueConsumer).
    """
    path_spec = path_spec_factory.Factory.NewPathSpec(
        definitions.TYPE_INDICATOR_OS, location=path)
    file_entry = path_spec_resolver.Resolver.OpenFileEntry(path_spec)

    file_object = file_entry.GetFileObject()
    top_level_object = parser_object.GetTopLevel(file_object)
    self.assertNotEquals(top_level_object, None)

    return self._ParsePlistWithPlugin(
        plugin_object, plist_name, top_level_object,
        knowledge_base_values=knowledge_base_values)

  def _ParsePlistWithPlugin(
      self, plugin_object, plist_name, top_level_object,
      knowledge_base_values=None):
    """Parses a plist using the plugin object.

    Args:
      plugin_object: the plugin object.
      plist_name: the name of the plist to parse.
      top_level_object: the top-level plist object.
      knowledge_base_values: optional dict containing the knowledge base
                             values. The default is None.

    Returns:
      An event object queue consumer object (instance of
      TestEventObjectQueueConsumer).
    """
    event_queue = queue.SingleThreadedQueue()
    event_queue_consumer = test_lib.TestEventObjectQueueConsumer(event_queue)

    parse_error_queue = queue.SingleThreadedQueue()

    parser_context = self._GetParserContext(
        event_queue, parse_error_queue,
        knowledge_base_values=knowledge_base_values)
    plugin_object.Process(
        parser_context, plist_name=plist_name, top_level=top_level_object)

    return event_queue_consumer
