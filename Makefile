.PHONY: all clean
ALL_OTFS = $(patsubst ufo/%.ufo,build/otf/%.otf,$(wildcard ufo/*.ufo))
ALL_WOFFS = $(patsubst ufo/%.ufo,build/woff/%.woff,$(wildcard ufo/*.ufo))
ALL_WOFF2S = $(patsubst ufo/%.ufo,build/woff2/%.woff2,$(wildcard ufo/*.ufo))

all: ${ALL_OTFS} ${ALL_WOFFS} ${ALL_WOFF2S}

otf: ${ALL_OTFS}
woff: ${ALL_WOFFS}
woff2: ${ALL_WOFF2S}

clean:
	rm -rf build/

build:
	mkdir build
build/otf: | build
	mkdir build/otf
build/woff: | build
	mkdir build/woff
build/woff2: | build
	mkdir build/woff2

build/otf/%.otf: ufo/%.ufo | build/otf
	makeotf -r -f $< -o build/otf/

build/woff/%.woff: build/otf/%.otf | build/woff
	ttf2woff $< $@

build/woff2/%.woff2: build/otf/%.otf | build/woff2
	woff2_compress $< && mv build/otf/$*.woff2 build/woff2/
