SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = ./docs
BUILDDIR      = ./docs/_build

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help lint clean Makefile


lint:
	@cd py_src/ && export MYPYPATH='./stubs' && mypy --config-file ../setup.cfg ../py_src
	@flake8 py_src/ && echo 'flake8: success'
	@docstr-coverage -m -f -F 80.0 py_src

clean:
	@rm -rf src/pkg1/__pycache__
	@rm -rf test/pkg1/__pycache__
	@rm -rf docs/_build/html/
	@rm -rf docs/_build/doctrees
	@rm -rf src/*.egg-info/
	@rm -rf src/logs/
	@rm -rf ./logs/
	@rm -rf ./build/
	@rm -rf .hypothesis/
	@rm -rf src/pkg1/.hypothesis/
	@rm -rf test/pkg1/.hypothesis/
	@rm -rf dist/

%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
