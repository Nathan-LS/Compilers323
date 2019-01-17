# Compilers 323 RAT18F group project
[![](https://img.shields.io/docker/pulls/nathanls/compilers323.svg)](https://hub.docker.com/r/nathanls/compilers323/)
[![](https://travis-ci.org/Nathan-LS/Compilers323.svg?branch=master)](https://travis-ci.org/Nathan-LS/Compilers323)
[![](https://img.shields.io/github/license/Nathan-LS/Compilers323.svg)](https://github.com/Nathan-LS/Compilers323/blob/master/LICENSE)
## Getting started
Running our application through [Docker](https://hub.docker.com/r/nathanls/compilers323/) is easy! Create a text file in your current working directory that you wish to parse and run via Docker: 

```docker run -it --rm -v ${PWD}:/app nathanls/compilers323 -i TestFile.txt```

This will take the 'TestFile.txt' input file and run it through the compiler. The preprocessor, lexical analysis, and syntax analysis files will be generated in the current directory.

To see all available arguments, run:

```docker run -it --rm -v ${PWD}:/app nathanls/compilers323 --help```
