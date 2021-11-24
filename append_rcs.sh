#!/bin/bash

BASHRC=~/.bashrc
if [ -f "$BASHRC" ]; then
    echo "$BASHRC exists."
    echo 'alias git-context=python3 $HOME/.git_context/git_context.py $pwd"' >> ~/.bashrc
else 
    echo "$BASHRC does not exist."
fi

ZSHRC=~/.zshrc
if [ -f "$ZSHRC" ]; then
    echo "$ZSHRC exists."
    echo 'alias git-context=python3 $HOME/.git_context/git_context.py $pwd"' >> ~/.zshrc
else 
    echo "$ZSHRC does not exist."
fi

exit 0