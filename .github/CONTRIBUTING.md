# Contributing to the project

To begin with, thank you very much for taking the time to contribute.\
It is of great value to the project as it is made substantially better.

The following are the guidelines for contributing to the project's repository.\
**They are not hard enforced rules, but a thorough guide to aid you when you want to contribute.**

## Proper Bug Reports

Please be aware of the following things when filing bug reports.

1. Do not open issues that have already been raised. Please, take the time to search whether the issue you're about to make has been already asked. Duplicate issues will be closed. This still applies, even if the duplicate issue has been closed.
1. When you are filling a bug report, it would be greatly appreciated if you could include the **complete** traceback. Without it, the bug might not be solvable, essentially meaning that you will be asked to re-submit the report but with even more information.
1. When submitting a report, ensure that you have given sufficient information to make the issue workable but also fixable. The issue template will thoroughly walk you through the complete and correct process, but they steps are also mentioned here:
    - **An overview of your bug report**: Nothing excessive, just a sentence or two to describe the issue in simple, human terms.
    - **A thorough guide on how to reproduce the issue**: Ideally, this should contain a small code snippet that, when ran, the issue will be presented for us to debug and eventually solve. **Please make sure that your API token is not displayed if it's part of the code!**
    - **Describe the expected result**: What were you expecting to receive as a result from the code? This is a major requirement, as it will guide us to fix the code in a way that it meets the given expectation.
    - **Describe the actual result**: What actually happened when you executed the code? Simply saying "The code just fails" or "The code doesn't work" is not helpful. Please make sure to describe how the code failed and include an exception, if you get any. If none, put up what's different from its expected output. That way, we can have a genuine understanding of where the code produces a different result, despite it working fine.
    - **Provide some information about your environment**: What version of the project are you using? What operating system are you running on? On what service was the code executed? This information is valuable to us. No, we will not steal your data but instead will use it to fix the given issue, if it's only applicable to certain services/operating systems/versions.

- If the report does not contain this information, we will require even more time to address and fix the issue. We most likely will ask for clarification and if no response is given then the issue will be closed.

## Proper PRs and Feature Requests

Submitting a pull request is very simple. However, make sure it focuses on a single aspect and it doesn't evolve around many things that are not distinct. For example, a great pull request would focus around adding a new function or method to the project without changing a lot of things other than the necessary. It would be greatly appreciated if the style is consistent to the one the project uses.

### Use of `type: ignore` comments
In any case, it may be necessary to ignore type checker warnings. That's understandable. 
If that's the case, it is **absolutely mandatory** that an additional comment is also made, explaining why the type checker warnings will be ignored.

## Licensing

By submitting a pull request, you agree that:
1) You hold the copyright on all the code inside the submitted pull request
2) You hereby agree to transfering all the rights to the owner of the repository
3) If you are found fault for any of the above, we -under no circumstance- will be held responsible after the merge of the pull request.

## Git Commit Styling

This guideline is of major importance.\
Not following it could potentially lead to a squash to your pull request, for cleaner commit history purposes.

- Some guides we would definitely recommend using when submitting a PR:

The [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) style is widely used and certainly a great style to start with.\
The [GitMoji](https://gitmoji.dev) style would make your pull look more attractive, lively and would certainly stand out from others.

We neither limit nor deny PRs when a different style is used; in fact, we greatly endorse it!
Your PR can be whatever style you find appropriate with some limitations:
- It has to be appropriate and make sense both in terms of readability and explanation.
- It has to fit with the project's design.
