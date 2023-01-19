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

# This script is super useful to find all proto files in googleapis and pass it as an arg to protoc.

find . -type f -name '*.proto' -print | xargs protoc --plugin=protoc-gen-py_reserved_names=plugin.py --py_reserved_names_out=./py_reserved_names --py_reserved_names_opt=$1 --proto_path=googleapis
