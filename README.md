# Plot user's Github activity

1. Retrieve commit messages of user and repositories with `retrieve_commits.py`
2. Get all collaborators from the user with `retrieve_contributors.py`
3. Plot word co-occurrence network with `word-cooccurrence-network.py`
4. Plot collaborator network with `plot-collaboration-network.py`
5. Convert plots with imagemagick and place them side-by-side
    - `convert -density 300 collaborator_network.pdf collaborator_network.jpg`
    - `convert -density 300 commits_words_coocurrence.pdf commits_words_coocurrence.jpg`
    - `montage collaborator_network.jpg commits_words_coocurrence.jpg -tile 2x1 -geometry +0+0 mug.jpg`
6. Print `mug.jpg`