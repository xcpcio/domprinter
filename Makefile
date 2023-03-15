idl_gen:
	hz update --idl ./idl/*.thrift --json_enumstr

build:
	bash ./build.sh

dev:
	bash ./build.sh
	bash ./output/bootstrap.sh
