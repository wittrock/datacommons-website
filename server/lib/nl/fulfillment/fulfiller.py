# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Module for NL page data spec"""

import logging

from server.lib.nl.common import counters as ctr
from server.lib.nl.common.utterance import QueryType
from server.lib.nl.common.utterance import Utterance
from server.lib.nl.detection import utils as detection_utils
from server.lib.nl.detection.types import Detection
from server.lib.nl.fulfillment import context
import server.lib.nl.fulfillment.handlers as handlers


#
# Populate chart candidates in the utterance.
#
def fulfill(uttr: Utterance) -> Utterance:
  query_types = [handlers.first_query_type(uttr)]
  while query_types[-1] != None:
    if fulfill_query_type(uttr, query_types[-1]):
      break
    query_types.append(handlers.next_query_type(query_types))

  rank_charts(uttr)
  return uttr


def fulfill_query_type(uttr: Utterance, query_type: QueryType) -> bool:
  # Reset previous state
  uttr.query_type = query_type
  uttr.chartCandidates = []

  # If we could not detect query_type from user-query, infer from past context.
  if (uttr.query_type == QueryType.UNKNOWN):
    uttr.query_type = context.query_type_from_context(uttr)

  found = False

  # Each query-type has its own handler. Each knows what arguments it needs and
  # will call on the *_from_context() routines to obtain missing arguments.
  handler = handlers.QUERY_HANDLERS.get(query_type, None)
  if handler:
    found = handler.module.populate(uttr)
    uttr.counters.info('processed_fulfillment_types',
                       handler.module.__name__.split('.')[-1])

  return found


#
# Rank candidate charts in the given Utterance.
#
# TODO: Maybe improve in future.
def rank_charts(utterance: Utterance):
  for chart in utterance.chartCandidates:
    logging.info("Chart: %s %s\n" % (chart.places, chart.svs))
  utterance.rankedCharts = utterance.chartCandidates
