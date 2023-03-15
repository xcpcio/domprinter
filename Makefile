idl_gen:
	hz update --idl ./idl/*.thrift

build:
	bash ./build.sh

dev:
	bash ./build.sh
	bash ./output/bootstrap.sh
