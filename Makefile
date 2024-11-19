dist:
	uv pip install .
	python -m build

install:
	httpie --debug plugins install .
