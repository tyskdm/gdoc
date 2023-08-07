
TARGET      := gdoc

# directories
SRCDIR 		:= gdoc
SPECDIR     := spec
TESTDIR     := tests
DISTDIR     := dist
DOCSDIR     := docs
DOXYGENDIR  := doxy
DOXYOUTDIR  := html
DOXYXMLDIR  := xml
DOXYBOOKDIR := DetailedDesign
PYTESTDIR   := htmlcov
MKDOCSDIR   := site

.PHONY: all clean doc doc-clean puml-img puml-clean test test-cov cov cov-clean style \
        book book-clean

all: clean test puml-img doc

clean: puml-clean doc-clean book-clean cov-clean 
	@py3clean .
	@$(RM) -rf $(DISTDIR)
	@$(RM) -rf $(MKDOCSDIR)

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
# Doxybook2
#
DOXYBOOKFLAGS :=

book: book-clean doc-clean puml-clean puml-img doc
	@$(RM) -rf $(DOCSDIR)/$(DOXYBOOKDIR)
	@mkdir -p $(DOCSDIR)/$(DOXYBOOKDIR)
	@doxybook --input $(DOXYGENDIR)/$(DOXYXMLDIR) \
	          --output $(DOCSDIR)/$(DOXYBOOKDIR) \
			  --config $(DOXYGENDIR)/doxybook2cfg.json

book-clean:
	@$(RM) -rf $(DOCSDIR)/$(DOXYBOOKDIR)

book-serve: book
	@mkdocs serve

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

test: style
	@pytest $(PYTESTFLAGS)

test-cov:
	@pytest $(PYTESTFLAGS) --cov $(SRCDIR) --cov-branch

cov:
	@pytest $(SPECDIR) $(PYTESTFLAGS) --cov $(SRCDIR) --cov-branch --cov-report=xml

cov-report:
	@pytest $(SPECDIR) $(PYTESTFLAGS) --cov $(SRCDIR) --cov-branch --cov-report=html

cov-clean:
	@$(RM) -rf $(PYTESTDIR)
	@$(RM) ./.coverage ./coverage.xml

style:
	isort $(SRCDIR) $(SPECDIR) $(TESTDIR)
	black $(SRCDIR) $(SPECDIR) $(TESTDIR)
