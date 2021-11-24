#!/bin/bash

BASHRC=~/.bashrc
if [ -f "$BASHRC" ]; then
    echo "$BASHRC exists."
    echo 'alias git-context="python3 $HOME/.git_context/git_context.py $pwd"' >> ~/.bashrc
    echo "$BASHRC appended with launch alias"
else 
    echo "$BASHRC does not exist. Skipping."
fi

ZSHRC=~/.zshrc
if [ -f "$ZSHRC" ]; then
    echo "$ZSHRC exists."
    echo 'alias git-context="python3 $HOME/.git_context/git_context.py $pwd"' >> ~/.zshrc
    echo "$ZSHRC appended with launch alias"
else 
    echo "$ZSHRC does not exist. Skipping"
fi

exit 0