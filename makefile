.PHONY: all clean test doc

TARGET      := gdoc

# directories
SRCDIR 		:= gdoc
SPECDIR     := spec
TESTDIR     := tests
DOXYGENDIR  := doxy
DOXYOUTDIR  := html

# flags
PYTESTFLAGS 	:=
DOXYGENFLAGS	:=


all: test doc

doc:
	@$(RM) -rf $(DOXYGENDIR)/$(DOXYOUTDIR)
	@cd doxy/; doxygen $(DOXYGENFLAGS)

clean:
	@$(RM) -rf $(DOXYGENDIR)/$(DOXYOUTDIR)
	@py3clean .

test:
	@pytest $(PYTESTFLAGS)
