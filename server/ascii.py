#coding: utf-8
hello = """
-----------------------------
Welcome to MP&PA quest v.01!
try "help" to view commands
-----------------------------
"""

help = """
 Register:
    reg [UserName] [UserKey]
 FlagPost:
    flag [flag] [task] [user] [userkey]
 Scoreboard:
    scoreboard | users
 Tasks:
    tasks
 Task:
    task [taskname]
 Profile:
    user [username]
 Close:
    close
"""

# SCOREBOARD
scoreboard_title = """
-----------------------------------------------------------------
N| TeamName           | Solved Tasks       | Total Score        | Bonus
-----------------------------------------------------------------
"""
scoreboard_user ="""
{place}|{name}|{solved}|{score}|{bonus}|
"""
# SCOREBOARD

# PROFILE
profile_body = """
------------------------------------------------------------------------------
 USER: {name} | PLACE: {place}
    | Solved tasks:
        {tasks}
    | score: {score}
    | bonus: {bonus}
------------------------------------------------------------------------------
"""
# PROFILE

# tasks
tasks_title = """
------------------------------------------------------------------
ID| TaskName           | Link               | Price              |
------------------------------------------------------------------
"""
tasks_body = """
{id} |{name}|{link}|{price}|
"""
# tasks

# task
task_body = """
------------------------------------------------------------------------------
 Name: {name}
    | Description:
        {info}
    | {link}
------------------------------------------------------------------------------
"""
#task


cowsay = """
 _______________________
<{str}>
 ----------------------
        \   ^__^
         \  (..)\_______
            (__)\       )\/\.
                ||----w |
                ||     ||
"""
cowsay_p= """
 ______________________
<{str}>
 ----------------------
        \   ^__^
         \  ($$)\_______
            (__)\       )\/\.
             U  ||----w |
                ||     ||
"""
cowsay_m = """
 ______________________
<{str}>
 ----------------------
        \   ^__^
         \  (00)\_______
            (__)\       )\/\.
                ||----w |
                ||     ||
"""
