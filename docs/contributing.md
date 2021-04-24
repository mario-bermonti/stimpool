# Contributing

Thank you for your interest in improving this project.

All contributions are welcome and greatly appreciated! Every little bit improves the
project and helps its users.

The following sections detail a variety of ways to contribute and how to get started.

Credit will always be given to the people making contributions. :wink:

If you do decide to work on an issue, please indicate so in a comment to the issue
so it's assigned to you and other people don't work on it simultaneously.

Don't hesitate to write a comment in the issue you are interested in
if you have questions, would like to discuss some issue further, or you need help.


## Types of Contributions

### Spread the word
Tell others about your experience with stimpool. You can share it on social media and follow it on GitHub.

### Submit Feedback

The best way to send feedback is to file an issue at
 <https://github.com/mario-bermonti/stimpool/issues>.

Please let us know about your experience using stimpool. You can tell us about the things that you like, the things that can be improved, and the things that you would like stimpool to do.

If you are proposing a feature:

- How it would help you and other users (mainly researchers).
- Explain all the details of how it would work.
- Keep the scope as narrow as possible to make it easier to implement.
- Remember that this is a volunteer-driven project and for this reason it may not be feasible
  to implement the feature or it may take some time.

### Write Documentation

stimpool could always use more documentation. You can contribute to the documentation
by:
- Fixing typographical, grammatical, or spelling errors.
- Improving documentation that is unclear or incorrect.
- Creating or improving examples and tutorials.
- Writing blog posts, articles, and similar content that share how you are using this project and your best practices with us.

### Report Bugs
  You can report bugs at <https://github.com/mario-bermonti/stimpool/issues>.

  Please provide all the details that are asked when you create the issue to make sure
  it is understood correctly.

### Fix existing bugs

  Look through the GitHub issues for bugs. Anything tagged with \"bug\"
  and \"help wanted\" is open to whoever wants to implement it.

### Implement Features

Look through the GitHub issues for features. Anything tagged with
\"enhancement\" and \"help wanted\" is open to whoever wants to
implement it.

## Start contributing!

### Set up the development environment

Ready to contribute? Here\'s how to set up
stimpool in your local development environment.

You will need [Python 3.6+][download_python] installed.

1.  Fork the [stimpool repo][stimpool_gh] on GitHub.
2.  Clone your fork locally:

        git clone git@github.com:your_name_here/stimpool.git

3. We use `poetry` to manage dependencies. Install it with the following command.

        curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

4.  Install the project, its dependencies, and the virtualenv:

         poetry install

5. Make sure everything is working properly before making any changes by running `poetry run invoke dev-tasks`.

### Development tasks (important side note)
In order to run anything inside the virtual environment every command has to be prefixed with `poetry run <command>`.

For example, to run python inside the virtual environment you would run `poetry run python`.

We have most of our development tasks pre-configured to run automatically with invoke.  :grin:

The most important tasks are:

| Command       | Description                               |
|---------------|-------------------------------------------|
| dev-tasks     | Run all development tasks.                |
| format        | Format code.                              |
| tests         | Run tests.                                |
| coverage      | Create coverage report.                   |
| lint          | Run all linting.                          |
| mypy          | Run mypy.                                 |
| docs          | Build documentation.                      |
| clean         | Run all clean sub-tasks.                  |

You can find see all the development tasks that pre-configured by running `poetry run invoke --list`.

### Making changes

#### Workflow

We work by protecting `master` branch and only merging changes that don't break existing functionality and are tested.

How do we do it?:

1. We identify something that must change
2. We create an issue on GitHub, if it doesn't already exist
3. We create a new branch named after the issue we want "fix" (`issue-$TASKNUMBER`)
4. We make changes and test everything works
5. Style the code
6. We then create a pull request to `master` branch that is reviewed and if approved, it is merged
   into `master`

This way we achieve an easy and scalable development process that avoids merge
conflicts and long-living branches.

In this method, the `master` branch always has the latest version of the software, is stable,
and is working.


        $ git checkout -b name-of-your-bugfix-or-feature

    Now you can make your changes locally.

6.  When you\'re done making changes, check that your changes pass the
    tests, including testing other Python versions, with tox:

        $ tox

7.  Commit your changes and push your branch to GitHub:

        $ git add .
        $ git commit -m "Your detailed description of your changes."
        $ git push origin name-of-your-bugfix-or-feature

8.  Submit a pull request through the GitHub website.

# Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1.  The pull request should include tests.
2.  If the pull request adds functionality, the docs should be updated.
    Put your new functionality into a function with a docstring, and add
    the feature to the list in README.rst.
3.  The pull request should work for Python 3.5, 3.6, 3.7 and 3.8, and
    for PyPy. Check <https://travis-ci.com/>{{
    cookiecutter.github\_username }}/{{ cookiecutter.project\_slug
    }}/pull\_requests and make sure that the tests pass for all
    supported Python versions.

# Tips

To run a subset of tests:

    {% if cookiecutter.use_pytest == 'y' -%}

> \$ pytest [tests.test]()stimpool

{% else %}

:   \$ python -m unittest [tests.test]()stimpool

{%- endif %}

# Deploying

A reminder for the maintainers on how to deploy. Make sure all your
changes are committed (including an entry in HISTORY.rst). Then run:

    $ bump2version patch # possible: major / minor / patch
    $ git push
    $ git push --tags

Travis will then deploy to PyPI if tests pass.



<!-- Credits -->
<!-- This file was developed based extensively on the contributing guides of many great projects: -->
<!-- https://github.com/briggySmalls/cookiecutter-pypackage/blob/master/%7B%7Bcookiecutter.project_slug%7D%7D/CONTRIBUTING.rst -->
<!-- https://github.com/pyjanitor-devs/pyjanitor/blob/dev/docs/CONTRIBUTION_TYPES.rst -->
<!-- https://github.com/cjolowicz/cookiecutter-hypermodern-python/blob/main/%7B%7Bcookiecutter.project_name%7D%7D/CONTRIBUTING.rst -->
