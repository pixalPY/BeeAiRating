@echo off
echo Initializing Git repository...
git init

echo Adding files to Git...
git add index.html

echo Creating initial commit...
git commit -m "Add simple HTML home page"

echo Setting up remote repository...
git branch -M main
git remote add origin https://github.com/pixalPY/BeeAiRating.git

echo Pushing to GitHub...
git push -u origin main

echo Done! Your files have been uploaded to GitHub.
pause 