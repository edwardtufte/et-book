.PHONY: all clean

clean:
	rm -rf build/

ALL_OTFS = $(patsubst ufo/%.ufo,build/%.otf,$(wildcard ufo/*.ufo))

build:
	mkdir build

build/%.otf: ufo/%.ufo | build
	makeotf -r -f $< -o build/

all: ${ALL_OTFS}
