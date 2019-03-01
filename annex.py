import os
import subprocess
import ranger.api
import ranger.core.runner
from ranger.api.commands import Command
from ranger.core.loader import CommandLoader


old_hook_init = ranger.api.hook_init


def call(cmds):
    return subprocess.Popen(cmds,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)


def remotes():
    try:
        proc = call(['git', 'remote'])
        stdout, stderr = proc.communicate()
        return stdout.split()
    except:
        return []


def annex_exists():
    try:
        proc = call(['git', 'annex', 'version'])
        proc.communicate()
        return proc.returncode == 0
    except OSError:
        return False


def annex_call(fm, cmds, fname):
    # git annex fails with absolute paths ...
    thisdir = fm.thisdir
    fname = os.path.basename(fname)
    loader = CommandLoader(['git', 'annex'] + cmds + [fname],
                           'annex:{}'.format(' '.join(cmds)))

    def reload_dir():
        thisdir.unload()
        thisdir.load_content()

    loader.signal_bind('after', reload_dir)
    fm.loader.add(loader)


def fnames(fm):
    return (str(fname) for fname in fm.thistab.get_selection())


class annex_add(Command):
    def execute(self):
        self.fm.loader.add(CommandLoader(['git', 'annex', 'add'], 'annex:add'))
        self.fm.loader.add(CommandLoader(['git', 'commit', '-m', '"add files"'], 'git:commit'))


class annex_get(Command):
    def execute(self):
        for fname in fnames(self.fm):
            if not os.path.exists(fname):
                annex_call(self.fm, ['get'], fname)


class annex_drop(Command):
    def execute(self):
        for fname in fnames(self.fm):
            if os.path.exists(fname):
                annex_call(self.fm, ['drop'], fname)


class annex_copy(Command):
    def tab(self):
        return ('annex_copy {}'.format(r) for r in remotes())

    def execute(self):
        remote = self.arg(1)

        if remote not in remotes():
            self.fm.notify("`{}' is not a remote".format(remote), bad=True)
            return

        for fname in fnames(self.fm):
            if os.path.exists(fname):
                annex_call(self.fm, ['copy', '-t', remote], fname)


class annex_sync(Command):
    def execute(self):
        cmd = 'git annex sync --fast --quiet'.split()
        self.fm.loader.add(CommandLoader(cmd, 'annex:sync'))


def hook_init(fm):
    if annex_exists():
        fm.commands.commands['annex_add'] = annex_add
        fm.commands.commands['annex_copy'] = annex_copy
        fm.commands.commands['annex_drop'] = annex_drop
        fm.commands.commands['annex_get'] = annex_get
        fm.commands.commands['annex_sync'] = annex_sync
    else:
        fm.notify('Could not find git-annex', bad=True)

    return old_hook_init(fm)


ranger.api.hook_init = hook_init
