# Contribution Guidelines:

## Branch Naming

### Feature: `feat/<description>`

### Example: `feat/user-sign-up`
<br>

### Bug Fix: `fix/<description>`

### Example: `fix/sign-up-crash`
<br>
  

### Hotfix: `hotfix/<description>`

### Example: `hotfix/sign-up-security-issue`

  <br>

### Other: `chore/<description>`

### Example: `chore/update-contributing.md`

<br>
  

## Commit Message Guidelines

### Template: `<type>: <short description> <optional longer description>`
### Commit Message Example:
```
feat: Update to display file upload button on frontend

Updated read_establishments_as_list function to process frontend upload as BytesIO. 

Frontend upload is handled by the Streamlit frontend. Conversion of the excel(.xlsx) file to CSV function is \
also present when not handling upload as BytesIO, mainly present for testing and handling backend operarations \
where the file is located within the disk and is local. When considering memry constraints, reading in files as \
BytesIO is more efficient as the file upload is treated as an in-memory binary stream - thus there is no need to \
write to the disk.
```


### Types:
```
- feat: new feature

- fix: bug fix

- docs: documentation changes

- style: code style changes, formatting, missing in-line comments, etc.

- test: Adding or updating tests

- chore: Dependency updates or changes
```

### Example: `feat: add user login function`
### Example: `fix: properly logs the logs the document`
### Example: `docs: fixing the branch names`
<br>

## Pull Request (PR) Guidelines
1. Create PR against the `main` branch
2. Provide clear title and description of the changes:
	   - Address the problem in PR
	   - Include steps to verify changes changes if needed
3. All tests must pass before submitting PR.
4. Tag reviewers if needed
5. Follow branch naming and commit message guidelines

### PR Example:
Title: `fix: resolve error on login`
Description:
```
- Fix null pointer on logging in
- Fix password input errors
```
## PR/Code Review
- Make sure `style_guide.md` is being followed when writing code
- Check for clear and descriptive commit messages
- Make sure no print or debug statements are present in final version.
- Verify all new functionality is tested and documented if necessary

	