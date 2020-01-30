# Source Code Linting Analysis

## Objective

The aim of this section is to perform linting checks on the source code of `DVNA`  and generate a code quality report to provide a solution to the 1st point of the problem statement under `Task 3`.

## Source Code Linting

Linting is a process in which a tool analyzes the source code of an application to identify the presence of programmatic and stylistic errors. Running a _Linter_ (a tool which can perform linting analysis) can help a developer to adhere to standard coding conventions and best practices. Linting tools are language-specific and thus, the tool that can be used depends on the application being tested.

These tools can also be used to generate reports about the code quality by either invoking a built-in functionality or writing a reporting wrapper around the tool to aid the ease of resolving identified issues.

## Linting tools for DVNA

DVNA is a Nodejs application and hence, I used [`jshint`](https://jshint.com/install/) as the linter. I primarily chose `jshint` as it is available as a command-line utility and hence, I could easily integrate it into my CI pipeline with Jenkins. I used the official documentation for using `jshint` that is available [here](https://jshint.com/docs/cli/).

Along with `jshint`, I also found `eslint` and used it as well, again, by following the official documentation for the CLI interface for  `eslint` which can be found [here](https://eslint.org/docs/2.13.1/user-guide/command-line-interface).

## Integrating `Jshint` with Jenkins Pipeline

To start off, I installed Jshint with NPM with the following command:

```bash
npm install -g jshint
```

To try out `jshint`, I ran the a scan with the command below, as mentioned by the documentation:

```bash
jshint $(ls ./**/*.js ./**/*.ejs | grep -v node | grep js) *.js
```

**Note**: I wrote this one-liner:`$(ls ./**/*.js ./**/*.ejs | grep -v node | grep js)` to exclude the `node_modules/` directory and also exclude any files which do not have a `.js` or `.ejs` extension.

Since `Jshint` gave a non-zero status code, when it found issues, I had to write a bash script to run the scan in a sub-shell and prevent the build from failing. The contents of the script, `jshint-script.sh`, are below:

```bash
#!/bin/bash

cd /{JENKINS HOME DIRECTORY}/workspace/node-lint-pipeline

jshint $(ls ./**/*.js ./**/*.ejs | grep -v node | grep js) *.js > /{JENKINS HOME DIRECTORY}/reports/jshint-report

echo $? > /dev/null
```

Lastly, I added a stage in the pipeline to execute the script after making it executable with `chmod +x`. The stage structure I added was as follows:

```jenkins
stage ('Lint Analysis with Jshint') {
    steps {
        sh '/{PATH TO SCRIPT}/jshint-script.sh'
    }
}
```

## Integrating `Eslint` with Jenkins Pipeline

To install `Eslint`, I used NPM again to run the following command, following the [official documentation](https://eslint.org/docs/user-guide/command-line-interface):

```bash
npm install -g eslint
```

Now, `Eslint` requires the project being scanned to have a `.eslintrc` file which specifies what Eslint should expect in the project and a few other configurations. It can be made by running `eslint --init` in the project's root folder. When I ran this, it generated a file, `.eslintrc.json`. I took note that I'll need to place this file every time I'll run a scan on the project with Eslint so, it doesn't prompt for running initialization each time. The contents of `.eslintrc.json` are:

```eslintrc.json
{
    "env": {
        "es6": true,
        "node": true
    },
    "extends": "eslint:recommended",
    "globals": {
        "Atomics": "readonly",
        "SharedArrayBuffer": "readonly"
    },
    "parserOptions": {
        "ecmaVersion": 2018,
        "sourceType": "module"
    },
    "rules": {
    }
}
```

After initializing Eslint, I ran the scan on DVNA with the following command, to scan all files within the current folder and its sub-folder with `.ejs` and `.js` extensions (because under the `/views` directory there were `.ejs` files) and lastly, write the report to a file in JSON format:

```bash
eslint --format json --ext .ejs,.js --output-file /{JENKINS HOME DIRECTORY}/reports/eslint-report ./
```

Like Jshint, Eslint also gave a non-zero status code if it identified issues with linting. So, I wrapped the required command in a bash script, `eslint-script.sh` whose contents are below:

```bash
#!/bin/bash

cd /{JENKINS HOME DIRECTORY}/workspace/node-lint-pipeline

eslint --no-color --format json --ext .ejs,.js --output-file /{JENKINS HOME DIRECTORY}/reports/eslint-report ./

echo $? > /dev/null
```

**Note**: I added the `--no-color` flag to avoid color formatting (for Linux terminals) as otherwise, it would have appended additional syntactical text to provide formatting which made the report difficult to read.

Finally, I added a stage in the pipeline to run the script after I made it executable with `chmod +x`. The stage that I added was as follows:

```jenkins
stage ('Lint Analysis with Jshint') {
    steps {
        sh '/{PATH TO SCRIPT}/eslint-script.sh'
    }
}
```

## Code Quality Report

This section contains a brief about the quality report that the tools used above generated based on the default linting rules they had.

### Jshint

Jshint found a total of 247 linting issues with DVNA. The report mostly comprised of errors stating a 'Missing Semicolon' and a few other errors that included 'Missing Identifier', 'Expected an Assignment', etc. Some of the bugs were logical issues within the codebase of DVNA but the vast majority referred to stylistic issues.

The complete report generated by Jshint can be found [here]().

### Eslint

Eslint proved to be a better linting tool than Jshint as it found a total of 549 issues with DVNA. It identified a wider range of issues within DVNA's codebase. Along with stylistic issues, it also found logical errors such as 'Undefined Elements', 'Unused Variables', 'Empty Blocks', 'Using Prototype Builtins', 'Redeclaration of Elements', etc.

The complete report generated by Eslint can be found [here]().
