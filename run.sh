# This script is super useful to find all proto files in googleapis and pass it as an arg to protoc.

find . -type f -name '*.proto' -print | xargs protoc --plugin=protoc-gen-custom=plugin.py --custom_out=./build --custom_opt=$1 --proto_path=googleapis
