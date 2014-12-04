Pylarion: Wannabe Python wrapper for Polarion

------------------------------------------------------------------------------
Intro
------------------------------------------------------------------------------

For a simple introduction and specification, see src/pylarionlib/interface.py.

As a task, this mini-project is tracked at [2].


------------------------------------------------------------------------------
Directory structure
------------------------------------------------------------------------------

README.txt - this file
src/ - sources
src/pylarionlib/ - sources of the Pylarion library
src/cli/ - sources for CLI tools above the Pylarion library
test/ - unittest sources; in general, they should follow the structure of
        src/
.* - various dot files in the root directory are metadata for Eclipse+PyDev


------------------------------------------------------------------------------
Status
------------------------------------------------------------------------------

- Low level internals of the Pylarion library should work, though they need
  more unittest code. Especially, the CRUD operations are ready.
- Some parts of the upper level (the public interface) of the Pylarion library
  are done, too, but again, more testing code needed.
- The rest of the public interface is not implemented but it should not be
  much tricky. More in TODO below.
- No CLI yet
- As of 2014-12-04, dormant. In other words:
  - Use this as a library of tricks and howtos, or:
  - DEVELOPER/MAINTAINER WANTED! Just clone and take the leadership! 


------------------------------------------------------------------------------
Problems
------------------------------------------------------------------------------

- Underdone, but I have no big plans for the nearest future (ENOTIME)
- In the code, you can find TODOs related to Polarion bugs or ambiguities,
  they need proper investigation and bug reporting.
- Our Polarion implementation is a moving target. Pylarion tries to be
  as simple as possible but some design choices had to be done in spite of
  being just provisional measures. More on that in interface.py.


------------------------------------------------------------------------------
TODO
------------------------------------------------------------------------------

- Tidy the test code (now, just horrible spaghetti, forgive me). It's not
  sustainable at all.
  
- Tidy the src/ code, too. Specifically:
  - Write docstrings
  - Split the source files (and maybe create subpackages), the sheer size
    of the files is not much user/hacker-friendly.

- Finish the public API. It is already drafted, see the the methods listed
  file interface.py: on Session and on some persistent objects. I think the 
  implementation should be pretty straight-forward, just by getting/setting
  attributes of the persistent objects and performing CRUD on them. In case
  a direct access to Polarion SOAP API would be needed, the existing code
  (including unittests) should provide guidance. As a last resort, see my
  simple demo code [1].

- Wrap the "upper" API to be easy-to-import-and-use. That's more or less
  Python-fu, a skilled Pythonist (not me now) should hack it easily. 

- Clean remaining TODOs scattered directly in the code.

- Add more test code (now it goes just through the most basic code paths).

- Design and write CLI; now there are just placeholders there. Anyway,
  the TCMS-related scripts provide excellent patterns. I hope we can start
  with the most often use cases and implement them by simple scripts above
  the Pylarion public API. Note: Some of the work may be avoided thanks
  to other automation tools in development.


------------------------------------------------------------------------------
References:
------------------------------------------------------------------------------

[1] http://wiki.test/vkadlcik/Polarion/SOAP_API_Notes/Python
[2] http://projects.engineering.redhat.com/browse/POLARION-28
