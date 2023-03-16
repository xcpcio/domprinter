idl_gen:
	hz update --idl ./idl/*.thrift --json_enumstr

idl_client_gen:
	hz client \
		--idl ./idl/*.thrift \
		--model_dir=./hertz_client \
		--client_dir=./hertz_client \
		--json_enumstr \
		-t=template=slim

gorm_gen:
	go run ./cmd/gorm_gen/generate.go

swagger_gen:
	swag init

build:
	bash ./build.sh

test:
	go test .

dev:
	bash ./build.sh
	bash ./output/bootstrap.sh
