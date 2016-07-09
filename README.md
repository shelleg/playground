Shellg Playground
=================

**Have a stunning edition to [shellg](https://github.com/shelleg/) project and you are not sure how to
contrinute ? - this is the place to start !**

This repository aims to serve as a "Playground" of integrating a
"Partial" to shellg, a **Partial** is an atomic part of a system which need also to
be tested as Standalone.


Getting started / WIP ?
-----------------------
Use the ./site-roles/<your role> dir to develop your role, once you are done developing your role / ready to share `git init`, `git commit`, `git push` ...
See the seciotn below discribing how to use this repository with 1 exception using the site-roles ove the galaxy-roles dir.
If you already have a role / re-using one you can just follow the short howto below and be on your way.





**Please note:** The `master` branch represents the skellaton of the repo and can be used
as such to create a `named-branch` and put into demo your partial, 

An example workflow:

1. Get code:

    ``` shell
    git clone git@github.com:shelleg/playground.git
    git checkout -b "partial-name" 
    ```

2. Add your dependencies to requirements.yml as an example please consult the `requiierments.yml` in this repo, when ready execute:
    ``` shell
    ansible-galaxy -r requiremts.yml 
    ```

3. Edit `playbooks/default.yml`:
 
    ```yaml
    
    ---
    - hosts: all
      become: yes
      become_user: root
      #gather_facts: no
      roles:
        - { role: ../galaxy-roles/<role name> }
        #- { role: ../site-roles/<role name> }
    ```

4. Add/Edit supported platforms: 
    Out of the box there are the following platforms:
    - ubuntu14.04
    - ubuntu16.04
    - centos6
    - centos7
    - redhat6
    - redhat7

    So edit `servers.yml` and add/remove at will ...

5. run you playbook on all platforms ...
``` shell
Vagrant up ...
```





