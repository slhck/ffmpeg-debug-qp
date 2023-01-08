# Changelog


## v0.1.4 (2023-01-08)

* Formatting.

* Project structure.

* Docs: add @stg7 as a contributor.

* Docs: add @winking324 as a contributor.

* Docs: add @plebreton as a contributor.

* Docs: add @lars18th as a contributor.

* Docs: add @ndtreviv as a contributor.

* Docs: add @slhck as a contributor.

* Update README.

* Add new python versions.

* Add note on ffmpeg v5.

* Improve finding the tool from PATH.

* Update.

* Improve README.


## v0.1.3 (2021-03-10)

* Improve setup.py.

* Remove release script.


## v0.1.2 (2021-03-06)

* Format setup.py and switch to markdown.

* Improve README.


## v0.1.1 (2020-03-15)

* Python 3.8.


## v0.1.0 (2020-03-14)

* Update release script.


## v0.0.1 (2020-03-14)

* Fix log flushing and parsing (#29)

  fix callback log

  Use the av_log_set_callback to fix threading log

  This works on Linux and Windows

  Fixes not writing the log HEADER

  Remove duplicate flush because the rebase

  Use native av_log function to fix the problem

  Update README.md

  Get number of size after the pkt_size label

* Create python package and add basic tests (#23)

* Various improvements.

  - Rename options to be better human readable and consistent
  - Fix missing uuid import
  - Add ignore for .debug
  - Print messages in case user wants to use logfile but supplies a video

* Add support for PIPE input (#22)

  * Add support for PIPE input

  * Use unique name for the video.debug file

* Restore the option to use a pre-existing log-data file (#21)

  * Reuse existing logfile

  * Add a parameter to reuse existing log-data file

  * Change name of the parameter

  * Supporting to preserve the debug data-log file

  * Add a new command to preserve the data-log file

* Fixes frame_type printing (#19)

  * fixes frame_type printing

  Fixes the bug "frame_type:" message in the middle of a line.

  * More easy parsing format

* Add DLLs.

* Update README.md.

  clarify instructions, add badge

* Add appveyor config (#18)

* Cleanup: Remove unused vars (#20)

* Bug fixing (#17)

  * Resynched some code with ffmpeg

  * Attempt at resynching parts of the code with ffmpeg

* Update of the binary for windows (#15)

* Several improvements.

  - require "output" as mandatory argument, not an option
  - pass path correctly as global variable
  - formatting function has been improved
  - handle errors during CLI execution
  - always delete the debug file
  - write stderr directly to output file

* Fix examples.

* Merge conflict.

* Added mmpeg2 compatibility, and responded to feedback from PR.

* Example otuputs.

* Updated README.

* Output only averages if people want to keep the output to a minimum and are only itereste in averages.

* Hid functionality behind switches.

* Fixed issue with debug not containing entire output.

* Nicely format the file.

* Don't re-create the debug file if it already exists.

* Stop rushing.

* Corrected path.

* Treat the library as a tool.

* Merge loss.

* Added mmpeg2 compatibility, and responded to feedback from PR.

* Example otuputs.

* Updated README.

* Output only averages if people want to keep the output to a minimum and are only itereste in averages.

* Hid functionality behind switches.

* Fixed issue with debug not containing entire output.

* Nicely format the file.

* Don't re-create the debug file if it already exists.

* Stop rushing.

* Corrected path.

* Treat the library as a tool.

* Merge pull request #11 from lars18th/fix-mpeg2.

  Fix mpeg2 errors

* Fix mpeg2 errors.

  This change adds support for mpeg2 and fixes errors with unkown Frame Types.

* Add author to readme.

* Merge pull request #5 from plebreton/master.

  add information on how to build the tool on windows

* Add information on how to build the tool on windows.

* Add license info for FFmpeg libraries.

* Add license info for FFmpeg libraries.

* Merge pull request #4 from plebreton/master.

  Build ffmpeg_debug_qp on windows

* Add binaries.

  + add a compiled version (in the .7zip archive)
  + add missing library files

* Build for windows.

  + add the VS2015 sln and project files for building the application on
  windows
  + add the depending libraries (ffmpeg) so it can be directly compiled
  without extra lib

* Allow parsing from stdin, add CSV output support.

* Update python wrapper to allow calculating average, outputting to stdout.

  breaking changes: outputting to stdout by default; if an output file is needed,
  specify the -o option.

* Change output to LD-JSON, improve efficiency.

* Update build instructions.

* Merge pull request #2 from imagora/master.

  QP less than 10 problem

* Should add ffmpeg repository.

* Ignore debug files like txt,json,log.

* Fix parse qp less than 10 error.

* Update instructions for Ubuntu, fixes #1.

* Finally fix parsing bug.

* Fix parsing bug.

* Fix bug in extraction.

* Fix error and output to file.

* Parse frame size.

* Add parsing script.

* Clean up output and code.

* Switch to new api mode.

* Add license.

* Clean up makefile.

* Add executable to .gitignore.

* Add files.

* Initial commit.


