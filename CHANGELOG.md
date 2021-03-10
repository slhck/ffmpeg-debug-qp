Changelog
=========


(unreleased)
------------
- Bump version to 0.1.3. [Werner Robitza]
- Improve setup.py. [Werner Robitza]
- Remove release script. [Werner Robitza]
- Bump version to 0.1.2. [Werner Robitza]
- Format setup.py and switch to markdown. [Werner Robitza]
- Improve README. [Werner Robitza]
- Bump version to 0.1.1. [Werner Robitza]
- Python 3.8. [Werner Robitza]
- Bump version to 0.1.0. [Werner Robitza]
- Update release script. [Werner Robitza]
- Fix log flushing and parsing (#29) [Lars The, Werner Robitza]

  fix callback log

  Use the av_log_set_callback to fix threading log

  This works on Linux and Windows

  Fixes not writing the log HEADER

  Remove duplicate flush because the rebase

  Use native av_log function to fix the problem

  Update README.md

  Get number of size after the pkt_size label
- Create python package and add basic tests (#23) [Werner Robitza]
- Various improvements. [Werner Robitza]

  - Rename options to be better human readable and consistent
  - Fix missing uuid import
  - Add ignore for .debug
  - Print messages in case user wants to use logfile but supplies a video
- Add support for PIPE input (#22) [Lars The]

  * Add support for PIPE input

  * Use unique name for the video.debug file
- Restore the option to use a pre-existing log-data file (#21) [Lars
  The]

  * Reuse existing logfile

  * Add a parameter to reuse existing log-data file

  * Change name of the parameter

  * Supporting to preserve the debug data-log file

  * Add a new command to preserve the data-log file
- Fixes frame_type printing (#19) [Lars The]

  * fixes frame_type printing

  Fixes the bug "frame_type:" message in the middle of a line.

  * More easy parsing format
- Add DLLs. [Werner Robitza]
- Update README.md. [Werner Robitza]

  clarify instructions, add badge
- Add appveyor config (#18) [Werner Robitza]
- Cleanup: Remove unused vars (#20) [Lars The]
- Bug fixing (#17) [Werner Robitza, nathantrevivian]

  * Resynched some code with ffmpeg

  * Attempt at resynching parts of the code with ffmpeg
- Update of the binary for windows (#15) [plebreton]
- Several improvements. [Werner Robitza]

  - require "output" as mandatory argument, not an option
  - pass path correctly as global variable
  - formatting function has been improved
  - handle errors during CLI execution
  - always delete the debug file
  - write stderr directly to output file
- Fix examples. [Werner Robitza]
- Merge conflict. [nathantrevivian]
- Added mmpeg2 compatibility, and responded to feedback from PR.
  [nathantrevivian]
- Example otuputs. [nathantrevivian]
- Updated README. [nathantrevivian]
- Output only averages if people want to keep the output to a minimum
  and are only itereste in averages. [nathantrevivian]
- Hid functionality behind switches. [nathantrevivian]
- Fixed issue with debug not containing entire output. [nathantrevivian]
- Nicely format the file. [nathantrevivian]
- Don't re-create the debug file if it already exists. [nathantrevivian]
- Stop rushing. [nathantrevivian]
- Corrected path. [nathantrevivian]
- Treat the library as a tool. [nathantrevivian]
- Merge loss. [nathantrevivian]
- Added mmpeg2 compatibility, and responded to feedback from PR.
  [nathantrevivian]
- Example otuputs. [nathantrevivian]
- Updated README. [nathantrevivian]
- Output only averages if people want to keep the output to a minimum
  and are only itereste in averages. [nathantrevivian]
- Hid functionality behind switches. [nathantrevivian]
- Fixed issue with debug not containing entire output. [nathantrevivian]
- Nicely format the file. [nathantrevivian]
- Don't re-create the debug file if it already exists. [nathantrevivian]
- Stop rushing. [nathantrevivian]
- Corrected path. [nathantrevivian]
- Treat the library as a tool. [nathantrevivian]
- Merge pull request #11 from lars18th/fix-mpeg2. [Werner Robitza]

  Fix mpeg2 errors
- Fix mpeg2 errors. [Lars The]

  This change adds support for mpeg2 and fixes errors with unkown Frame Types.
- Add author to readme. [Werner Robitza]
- Merge pull request #5 from plebreton/master. [Werner Robitza]

  add information on how to build the tool on windows
- Add information on how to build the tool on windows. [Pierre Lebreton]
- Add license info for FFmpeg libraries. [Werner Robitza]
- Add license info for FFmpeg libraries. [Werner Robitza]
- Merge pull request #4 from plebreton/master. [Werner Robitza]

  Build ffmpeg_debug_qp on windows
- Add binaries. [Pierre Lebreton]

  + add a compiled version (in the .7zip archive)
  + add missing library files
- Build for windows. [Pierre Lebreton]

  + add the VS2015 sln and project files for building the application on
  windows
  + add the depending libraries (ffmpeg) so it can be directly compiled
  without extra lib
- Allow parsing from stdin, add CSV output support. [Werner Robitza]
- Update python wrapper to allow calculating average, outputting to
  stdout. [Werner Robitza]

  breaking changes: outputting to stdout by default; if an output file is needed,
  specify the -o option.
- Change output to LD-JSON, improve efficiency. [Werner Robitza]
- Update build instructions. [Werner Robitza]
- Merge pull request #2 from imagora/master. [Werner Robitza]

  QP less than 10 problem
- Should add ffmpeg repository. [ShanHui]
- Ignore debug files like txt,json,log. [ShanHui]
- Fix parse qp less than 10 error. [ShanHui]
- Update instructions for Ubuntu, fixes #1. [Werner Robitza]
- Finally fix parsing bug. [Steve]
- Fix parsing bug. [Steve]
- Fix bug in extraction. [Werner Robitza]
- Fix error and output to file. [Werner Robitza]
- Parse frame size. [Werner Robitza]
- Add parsing script. [Werner Robitza]
- Clean up output and code. [Werner Robitza]
- Switch to new api mode. [Werner Robitza]
- Add license. [Werner Robitza]
- Clean up makefile. [Werner Robitza]
- Add executable to .gitignore. [Werner Robitza]
- Add files. [Werner Robitza]
- Initial commit. [Werner Robitza]


