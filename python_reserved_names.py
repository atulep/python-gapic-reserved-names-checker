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

from gapic.utils.reserved_names import RESERVED_NAMES
import subprocess
import argparse
import os


parser = argparse.ArgumentParser(description='Determine if the keyword is used in googleapis.')
parser.add_argument('--keywords', metavar='K', type=str, nargs='+', required=False,
                    help='Keywords to analyze.')
args = parser.parse_args()


def analyze_all_reserved_names():
    opt_str = ','.join(RESERVED_NAMES)
    subprocess.call(['sh', 'run.sh', opt_str])


def analyze_specific_word(word):
    """Specific keyword passed to protoc. When for example in the PR.
    protoc ... --gapic_opt=foo,foo,foo
    """
    if isinstance(word, list):
        opt_str = ','.join(word)
    else:
        opt_str = word
    subprocess.call(['sh', 'run.sh', opt_str])


if __name__ == '__main__':
    assert os.path.isdir('googleapis'), 'Please run `git clone https://github.com/googleapis/googleapis.git`'
    if not os.path.isdir('py_reserved_names'):
        os.makedirs('py_reserved_names')
    if args.keywords is None:
        # Analyze the existing GAPIC keywords.
        analyze_all_reserved_names()
    else:
        analyze_specific_word(args.keywords)
