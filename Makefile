.PHONY: all clean

all: map.svg map.png

map_body.svg: map.gv
	neato -Tsvg map.gv -o map_body.svg

legend.svg: legend.gv
	dot -Tsvg legend.gv -o legend.svg

map.svg: map_body.svg legend.svg combine_svg.py
	~/venv/bin/python3 combine_svg.py > /dev/null

map.png: map.svg
	convert -size $$(~/venv/bin/python3 combine_svg.py 2>&1 >/dev/null) map.svg map.png

clean:
	rm -f map_body.svg legend.svg map.svg map.png
