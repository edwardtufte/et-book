.PHONY: all clean test psautohint otf ttf woff woff2
ALL_PSAUTOHINTS = $(patsubst ufo/%.ufo,build/psautohint/%.ufo,$(wildcard ufo/*.ufo))
ALL_OTFS = $(patsubst ufo/%.ufo,build/otf/%.otf,$(wildcard ufo/*.ufo))
ALL_TTFS = $(patsubst ufo/%.ufo,build/ttf/%.ttf,$(wildcard ufo/*.ufo))
ALL_WOFFS = $(patsubst ufo/%.ufo,build/woff/%.woff,$(wildcard ufo/*.ufo))
ALL_WOFF2S = $(patsubst ufo/%.ufo,build/woff2/%.woff2,$(wildcard ufo/*.ufo))

all: ${ALL_OTFS} ${ALL_TTFS} ${ALL_WOFFS} ${ALL_WOFF2S}

psautohint: ${ALL_PSAUTOHINTS}
otf: ${ALL_OTFS}
woff: ${ALL_WOFFS}
woff2: ${ALL_WOFF2S}

clean:
	rm -rf build/ tests/

build:
	mkdir -p build
build/psautohint: | build
	mkdir -p build/psautohint
build/otf: | build
	mkdir -p build/otf
build/ttf: | build
	mkdir -p build/ttf
build/woff: | build
	mkdir -p build/woff
build/woff2: | build
	mkdir -p build/woff2

build/psautohint/%.ufo: ufo/%.ufo ufo/%.ufo/* | build/psautohint
	psautohint -o $@ $<

build/otf/%.otf: build/psautohint/%.ufo | build/otf
	makeotf -r -f $< -o build/otf/

build/ttf/%.ttf: build/otf/%.otf | build/ttf
	otf2ttf -o /dev/stdout $< | ttfautohint /dev/stdin $@

build/woff/%.woff: build/otf/%.otf | build/woff
	ttf2woff $< $@

build/woff2/%.woff2: build/otf/%.otf | build/woff2
	woff2_compress $< && mv build/otf/$*.woff2 build/woff2/


ALL_OTF_HINTING_TESTS = tests/otf-hinting/Roman-14.png tests/otf-hinting/Roman-15.png tests/otf-hinting/Roman-16.png tests/otf-hinting/Roman-17.png tests/otf-hinting/Roman-18.png tests/otf-hinting/Roman-19.png tests/otf-hinting/Roman-20.png tests/otf-hinting/Roman-21.png
ALL_TTF_HINTING_TESTS = tests/ttf-hinting/Roman-14.png tests/ttf-hinting/Roman-15.png tests/ttf-hinting/Roman-16.png tests/ttf-hinting/Roman-17.png tests/ttf-hinting/Roman-18.png tests/ttf-hinting/Roman-19.png tests/ttf-hinting/Roman-20.png tests/ttf-hinting/Roman-21.png

test: ${ALL_OTF_HINTING_TESTS}  ${ALL_TTF_HINTING_TESTS}

tests:
	mkdir -p tests
tests/otf-hinting: | tests
	mkdir -p tests/otf-hinting
tests/ttf-hinting: | tests
	mkdir -p tests/ttf-hinting

tests/otf-hinting/Roman-%.png: build/otf/ETBook-Roman.otf | tests/otf-hinting
	convert -background white -fill black -font build/otf/ETBook-Roman.otf -pointsize $* label:'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ß' $@

tests/ttf-hinting/Roman-%.png: build/ttf/ETBook-Roman.ttf | tests/ttf-hinting
	convert -background white -fill black -font build/ttf/ETBook-Roman.ttf -pointsize $* label:'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ß' $@
