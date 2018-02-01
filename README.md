# WALL-E
## Using openCV version 3.3 and python 2.7
Make sure you are working on your own branch.

- Create a new branch: `git checkout -b branchname`
- Then after commiting your code, push to your branch instead of master: `git push origin branchname`
- When you are finished with your code, submit a pull request to merge your branch into the master branch


## Using stereorectification
1)  Run stereorectification.py and it'll save the camera values to a .yml file.
2)  Call apply_stereo_rectify.py on two videos and it will read from the .yml file and generate the rectification maps. The map is applied to each frame of both videos