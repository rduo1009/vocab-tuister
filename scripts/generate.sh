#!/bin/bash

go generate ./...

buf generate
uv run python3 -m grpc_tools.protoc \
  -I proto \
  --protobuf-to-pydantic_out=src/pb \
  proto/vocab_tuister/v1/sessionconfig.proto