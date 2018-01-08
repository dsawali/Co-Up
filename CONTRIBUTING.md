# Contributing

Two main shared branches are used in this repo:
- `master`
    - Contains tested, stable code from develop.
- `develop`
    - Integration of features from various developer branches.

## Process
A simple process is followed to get from idea to code in `master`:
1. Create or take an issue in gitlab. Ensure the issue is assigned to you.
2. Create your branch.
```
cd path_to_your_repo
git checkout develop
git pull
git checkout -b your_name/your_feature
git push -u origin your_name/your_feature
```
3. Implement your feature. Add and commit changes as you progress.
```
git add your_file_1 your_file_2
git commit -m 'your_commit_message'
git push
```
4. When your feature is ready, merge in any upstream changes.
```
git checkout develop
git pull
git checkout your_name/your_branch
git merge develop
```
5. If you have conflicts, resolve them.
6. Push your changes.
```
git push
```
7. Create a merge request in gitlab. Assign the merge request to another developer.
8. The assigned developer will review the code asking questions when needed.
9. When the code is deemed good, the assigned developer will merge and delete the branch.

## Code Review
I don't think we need crazy strict code review. We should however make sure to read code proposed for merge to ensure that it makes sense and will not introduce a bug. Some things to look for:
- Are the files committed appropriate? Are all the files source? Please do not commit personal or temporary files such as the entire \_\_pycache\_\_ directory, or db.sqlite3 (database files). A rule of thumb is to commit all *.py, *.json, and *.md
- Does the code make sense? Is it clear and readable?
- Is the feature complete? Does it work?

Happy contributing!
