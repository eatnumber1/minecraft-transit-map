.PHONY: all clean

all: map.svg map.png

map_body.svg: map_body.gv
	neato -Tsvg map_body.gv -o map_body.svg

legend.svg: legend.gv
	dot -Tsvg legend.gv -o legend.svg

map.svg size.txt: map_body.svg legend.svg combine_svg.py
	python3 combine_svg.py > size.txt

map.png: map.svg size.txt
	convert -size $$(cat size.txt) map.svg map.png

clean:
	rm -f map_body.svg legend.svg map.svg map.png size.txt
