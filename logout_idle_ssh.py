# coding: utf-8

from __future__ import unicode_literals, print_function

import os
import sys
import re
import subprocess

# set switch to daily or weekly, default = daily
kill_sessions = "daily"


class IdleKiller(object):
    
    def __init__(self):
        self.tty_to_kill = []
    
    def _isIdleWeek(self, idle):
        if re.search("\d{1,}weeks?", idle, re.IGNORECASE):
            return True
        return False
    
    def _isIdleDay(self, idle):
        if re.search("\d{1,}days?", idle, re.IGNORECASE):
            return True
        return False
    
    def getIdleSesions(self):
        proc = subprocess.Popen("w", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.wait()
        stdout, stderr = proc.communicate()
        cnt = 0
        for line in stdout.lstrip().rstrip().split("\n"):
            cnt += 1
            if cnt < 3:
                continue
            line = re.split("\s{1,}", line)
            user = line[0]
            tty = line[1]
            idle = line[4]
            if idle == "-":
                continue
            if kill_sessions == "weekly" and self._isIdleWeek(idle):
                self.tty_to_kill.append([tty, user])
            else:
                if self._isIdleDay(idle):
                    self.tty_to_kill.append([tty, user])
    
    def killSessions(self):
        for tty in self.tty_to_kill:
            proc = subprocess.Popen(
                "ps aux | grep %s | grep \"@%s\" | grep -v grep" % (tty[1], tty[0]),
                shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            proc.wait()
            stdout, stderr = proc.communicate()
            pid = re.split("\s{1,}", stdout.rstrip().lstrip(), re.IGNORECASE)[1]
            proc = subprocess.Popen("kill %s" % pid, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            proc.wait()
    
    def run(self):
        self.getIdleSesions()
        self.killSessions()


if __name__ == "__main__":
    try:
        IdleKiller().run()
        sys.exit(0)
    except Exception as e:
        raise
