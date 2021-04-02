.PHONY: all clean test psautohint otf woff woff2
ALL_PSAUTOHINTS = $(patsubst ufo/%.ufo,build/psautohint/%.ufo,$(wildcard ufo/*.ufo))
ALL_OTFS = $(patsubst ufo/%.ufo,build/otf/%.otf,$(wildcard ufo/*.ufo))
ALL_WOFFS = $(patsubst ufo/%.ufo,build/woff/%.woff,$(wildcard ufo/*.ufo))
ALL_WOFF2S = $(patsubst ufo/%.ufo,build/woff2/%.woff2,$(wildcard ufo/*.ufo))

all: ${ALL_OTFS} ${ALL_WOFFS} ${ALL_WOFF2S}

psautohint: ${ALL_PSAUTOHINTS}
otf: ${ALL_OTFS}
woff: ${ALL_WOFFS}
woff2: ${ALL_WOFF2S}

clean:
	rm -rf build/ tests/

build:
	mkdir build
build/psautohint: | build
	mkdir build/psautohint
build/otf: | build
	mkdir build/otf
build/woff: | build
	mkdir build/woff
build/woff2: | build
	mkdir build/woff2

build/psautohint/%.ufo: ufo/%.ufo ufo/%.ufo/* | build/psautohint
	psautohint -o $@ $<

build/otf/%.otf: build/psautohint/%.ufo | build/otf
	makeotf -r -f $< -o build/otf/

build/woff/%.woff: build/otf/%.otf | build/woff
	ttf2woff $< $@

build/woff2/%.woff2: build/otf/%.otf | build/woff2
	woff2_compress $< && mv build/otf/$*.woff2 build/woff2/


ALL_OTF_HINTING_TESTS = tests/otf-hinting/Roman-14.png tests/otf-hinting/Roman-15.png tests/otf-hinting/Roman-16.png tests/otf-hinting/Roman-17.png tests/otf-hinting/Roman-18.png tests/otf-hinting/Roman-19.png tests/otf-hinting/Roman-20.png tests/otf-hinting/Roman-21.png

test: ${ALL_OTF_HINTING_TESTS}

tests:
	mkdir tests
tests/otf-hinting: | tests
	mkdir tests/otf-hinting

tests/otf-hinting/Roman-%.png: build/otf/ETBook-Roman.otf | tests/otf-hinting
	convert -background white -fill black -font build/otf/ETBook-Roman.otf -pointsize $* label:'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ß' $@
