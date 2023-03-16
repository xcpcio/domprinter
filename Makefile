idl_gen:
	hz update --idl ./idl/*.thrift --json_enumstr

idl_client_gen:
	cd hertz_client && \
	hz client \
		--mod github.com/Dup4/domprinter/hertz_client \
		--idl ../idl/*.thrift \
		--model_dir=./ \
		--client_dir=./ \
		--json_enumstr \
		-t=template=slim \
	&& go mod tidy

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
