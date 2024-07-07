all:
	make clean
	python setup.py build -f
	cp build/lib.linux*/subsets/*.so subsets/
	make test

.PHONY: test
test:
	python3 -m pytest tests/

clean:
	rm -f subsets/_subsets.*.so
	rm -f subsets/*_wrap.cpp*
	rm -f subsets/subsets.py
	rm -rf build/ dist/

upload:
	python -m build
	twine upload --repository subsets  dist/subsets-*.tar.gz