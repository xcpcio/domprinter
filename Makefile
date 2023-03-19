PKGLIST=$(shell go list ./...)

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
	swag init --output=./swagger

build:
	bash ./build.sh

dev:
	bash ./build.sh
	bash ./output/bootstrap.sh

test:
	go vet $(PKGLIST)
	go test $(PKGLIST) -race -coverprofile=./unittest-coverage.out

ut:
	go test $(PKGLIST) -race -coverprofile=./unittest-coverage.out

bench:
	go test $(PKGLIST) -run=NOTEST -benchmem -bench=. -cpu=1,2,4,8
