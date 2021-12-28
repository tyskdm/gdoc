.PHONY: all doc puml_img puml_clean clean test

TARGET      := gdoc

# directories
SRCDIR 		:= gdoc
SPECDIR     := spec
TESTDIR     := tests
DOXYGENDIR  := doxy
DOXYOUTDIR  := html
DOXYXMLDIR  := xml

# flags
PYTESTFLAGS 	:=
DOXYGENFLAGS	:=

# PlantUML Settings
## directories
PUMLSRC     := .
## flags
PUMLFLAGS   :=


all: clean test puml_img doc

doc:
	@$(RM) -rf $(DOXYGENDIR)/$(DOXYOUTDIR)
	@cd doxy/; doxygen $(DOXYGENFLAGS)

puml_img:
	@find $(PUMLSRC) \( -name *.puml -or -name *.pu \) | while read line; \
    do \
		echo puml_img: $$line; \
	 	dir=$${line%.*}; \
		dir=$$(basename "$$dir"); \
		plantuml -o "./_puml_/$$dir" $$PUMLFLAGS "$$line"; \
	done

puml_clean:
	@find $(PUMLSRC) \( -name *.puml -or -name *.pu \) | while read line; \
    do \
	 	dir=$${line%.*}; \
		parent_dir=$$(dirname "$$dir"); \
		$(RM) -rf "$$parent_dir"/_puml_; \
	done

clean: puml_clean
	@$(RM) -rf $(DOXYGENDIR)/$(DOXYOUTDIR)
	@$(RM) -rf $(DOXYGENDIR)/$(DOXYXMLDIR)
	@py3clean .

test:
	@pytest $(PYTESTFLAGS)
