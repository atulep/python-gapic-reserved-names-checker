#!/usr/bin/env python

import sys
from google.protobuf.compiler import plugin_pb2 as plugin
from collections import defaultdict
import keyword
from typing import List, Dict, Set

api_to_fields = defaultdict(list)


def format_output(violations: Dict[str, Set], pattern: List[str]):
    # Total violations are useful for the 
    total_violations = set()
    for v_set in violations.values():
        total_violations = total_violations.union(v_set)

    out_str = [f'Pattern: {pattern}', 'Violations:']
    for k, v in violations.items():
        out_str.append(f'{k} has the following violations {v}')
    # TODO: api_to_violations dict instead ...
    out_str.append(f'Total violations: {total_violations}')
    # Total violations are what's actually used from the pattern in googleapis.
    reserved_list_should_be = total_violations.union(set(keyword.kwlist))
    out_str.append(f'Reserved names list should be: {reserved_list_should_be}')
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
    total_violations = set()
    api_to_violations = defaultdict(set)
    for api, fields in api_to_fields.items():
        sys.stderr.write(api + "\n")  # for debug purposes
        violations = []
        for pat in patterns:
            violations += list(filter(lambda name: name == pat, fields))
        violations = set(violations)
        if violations:
            api_to_violations[api] = violations
        total_violations = total_violations.union(violations)
    return api_to_violations


#  protoc --plugin=protoc-gen-custom=plugin.py --custom_out=./build googleapis/google/actions/sdk/v2/action.proto 
def generate_code(request, response):
    f = response.file.add()
    f.name = 'final_report.txt'
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