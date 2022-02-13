#!/bin/bash

echo "Warning: this will reset the emoji, due-date, active-users branches."
read -r -p "Are you sure? [y/N] " response
if [[ ! "$response" =~ ^([yY][eE][sS]|[yY])$ ]]
then
    exit 1
fi

rebase_branch() {
    branch=$1
    git checkout "$branch"
    git reset --hard "origin/$branch"
    git rebase main "$branch"
    git push origin "$branch" -f
}

git checkout main
git pull -pr

rebase_branch emoji
rebase_branch due-date
rebase_branch active-users

git checkout main
