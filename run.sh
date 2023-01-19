# This script is super useful to find all proto files in googleapis and pass it as an arg to protoc.

find . -type f -name '*.proto' -print | xargs protoc --plugin=protoc-gen-py_reserved_names=plugin.py --py_reserved_names_out=./py_reserved_names --py_reserved_names_opt=$1 --proto_path=googleapis
