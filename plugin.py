#!/usr/bin/env python

# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# 		https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
from google.protobuf.compiler import plugin_pb2 as plugin
from collections import defaultdict
from typing import List, Dict, Set

api_to_fields = defaultdict(list)


def format_output(violations: Dict[str, Set], pattern: List[str]) -> str:
    """format_output returns a nicely formatted summary."""
    out_str = [f'Pattern: {pattern}', 'Violations:']
    for k, v in violations.items():
        out_str.append(f'{k} has the following violations {v}')
    return '\n'.join(out_str)


def match_field_name(api_to_fields: Dict[str, List[str]], patterns: List[str]) -> Dict[str, Set[str]]:
    """match_field_name returns a set of violations occured for each api in api_to_fields.

    The function checks occurence of each pattern in the list of field names of the given APIs.

    Args:
        api_to_fields: a dict of api names to a list of its fields as found in protos.
        pattern: a list of patterns that the function should match against.
    Returns:
        api_to_violations: a dict of api names to a set of fields matching any of the patterns.
    """
    api_to_violations = defaultdict(set)
    for api, fields in api_to_fields.items():
        sys.stderr.write(api + "\n")  # for debug purposes
        violations = []
        for pat in patterns:
            violations += list(filter(lambda name: name == pat, fields))
        violations = set(violations)
        if violations:
            api_to_violations[api] = violations
    return api_to_violations


def generate_code(request, response):
    """Main function that generates summary report."""
    f = response.file.add()
    f.name = 'python_reserved_names_final_report.txt'
    # Store all of fields from all googleapis.
    for proto_file in request.proto_file:
        for msg in proto_file.message_type:
            for field in msg.field:
                api_to_fields[proto_file.name].append(field.name)
    pattern = request.parameter.split(',')
    f.content = format_output(match_field_name(api_to_fields, pattern), pattern)


if __name__ == '__main__':
    # Read request message from stdin
    # Parse request
    request = plugin.CodeGeneratorRequest.FromString(sys.stdin.buffer.read())

    # Create response
    response = plugin.CodeGeneratorResponse()

    # Generate code
    generate_code(request, response)
    response.supported_features = plugin.CodeGeneratorResponse.FEATURE_PROTO3_OPTIONAL

    # Serialise response message
    output = response.SerializeToString()

    # Write to stdout
    sys.stdout.buffer.write(output)