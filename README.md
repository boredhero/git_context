# git_context

I was driven into a great rage in the process of trying to manage multiple ssh keys with git. This is the solution.

## What is it?

So, it's a real pain in the ass to manage multiple git accounts and ssh keys. This is a wrapper to try and make life easier.

## What is a Git Context?

A git context is an idea that came to mind for the purposes of this wrapper. TL;DR, a context is a username, name, and set of git settings. There is a global one and a repo one, but this tool aims to simplify [this entire hellscape](https://gist.github.com/oanhnn/80a89405ab9023894df7) down to like, one single short command.

## Why are you doing this?

Out of the kindness of my heart

## What does it do? (Currently just a planned feature set)

| Command Syntax | Function |
| :-: | :-: |
| `git-context help` | Displays this list of commands |
| `git-context list` | Returns a list of git contexts |
| `git-context add [git_username] [email] [key_type "ed25519" or "rsa"] ["/path/to/ssh_file.pub"]` | Adds a git context from username and file |
| `git-context create [git_username] [email] [key_type "ed25519" or "rsa"]` | This generates a key via ssh-keygen, names it, and adds it to this system |
| `git-context delete [git_username]` | Self explanatory |
| `git-context get` | Returns git_username of current global or local git context |
| `git-context set [git_username]` | If in a git repo, change local config to use the correct git context, else set the global defaults |
| `git-context clone [git_username] [remote_https_or_ssh_url] [optional recurse:true]` | Clones a git repository using the current context returned by `git-context get` |

## What OS does this support?

Linux. Tested on Arch Linux, your distro may vary. PRs accepted.

### Can you port it to Mac OS/Windows/Temple OS/etc

No. But if you do it I'll accept the PR

### Can you port it to [Insert Language Here]

No. Make your own.

## Dependencies?

```pip install -r requirements.txt```

## Install

An install script is coming. Note that in order to know file directory, the arg after python3 git_context.py should be $(pwd)
This will go in your .bashrc or .zshrc so that when you use the alias git-context by typing `git-context get` the actual command issued to the program via your rc file is python3 git_context.py $(pwd) [your other args here, ex 'get']
