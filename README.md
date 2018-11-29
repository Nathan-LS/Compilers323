# Compilers 323 group project
## Getting started
Running our application through [Docker](https://hub.docker.com/r/nathanls/compilers323/) is easy! Create a text file in your current working directory that you wish to parse and run via Docker: 

```docker run --rm -v ${PWD}:/app nathanls/compilers323 -i TestFile.txt```

This will take the 'TestFile.txt' input file and run it through the compiler. The preprocessor, lexical analysis, and syntax analysis files will be generated in the current directory.

To see all available arguments, run:

```docker run --rm -v ${PWD}:/app nathanls/compilers323 --help```
