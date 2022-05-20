
TARGET      := gdoc

# directories
SRCDIR 		:= gdoc
SPECDIR     := spec
TESTDIR     := tests
DOXYGENDIR  := doxy
DOXYOUTDIR  := html
DOXYXMLDIR  := xml
PYTESTDIR   := htmlcov

.PHONY: all clean doc doc-clean puml-img puml-clean test test-cov cov spec-clean

all: clean test puml-img doc

clean: puml-clean doc-clean spec-clean 
	@py3clean .

#
# Doxygen
#
DOXYGENFLAGS :=

doc:
	@$(RM) -rf $(DOXYGENDIR)/$(DOXYOUTDIR)
	@cd doxy/; doxygen $(DOXYGENFLAGS)

doc-clean:
	@$(RM) -rf $(DOXYGENDIR)/$(DOXYOUTDIR)
	@$(RM) -rf $(DOXYGENDIR)/$(DOXYXMLDIR)

#
# PlantUML
#
PUMLSRC   := .
PUMLFLAGS :=

puml-img:
	@find $(PUMLSRC) \( -name *.puml -or -name *.pu \) | while read line; \
    do \
		echo puml-img: $$line; \
	 	dir=$${line%.*}; \
		dir=$$(basename "$$dir"); \
		plantuml -o "./_puml_/$$dir" $$PUMLFLAGS "$$line"; \
	done

puml-clean:
	@find $(PUMLSRC) \( -name *.puml -or -name *.pu \) | while read line; \
    do \
	 	dir=$${line%.*}; \
		parent_dir=$$(dirname "$$dir"); \
		$(RM) -rf "$$parent_dir"/_puml_; \
	done

#
# pytest
#
PYTESTFLAGS :=

test:
	@pytest $(PYTESTFLAGS)

test-cov:
	@pytest $(PYTESTFLAGS) --cov $(SRCDIR) --cov-branch

cov:
	@pytest $(SPECDIR) $(PYTESTFLAGS) --cov $(SRCDIR) --cov-branch --cov-report=html

spec-clean:
	@$(RM) -rf $(PYTESTDIR)
