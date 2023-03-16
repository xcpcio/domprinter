idl_gen:
	hz update --idl ./idl/*.thrift --json_enumstr

gorm_gen:
	go run ./cmd/gorm_gen/generate.go

build:
	bash ./build.sh

test:
	go test .

dev:
	bash ./build.sh
	bash ./output/bootstrap.sh
