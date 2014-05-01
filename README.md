## ranger-annex

... is a plugin to integrate [git-annex][] calls within the [ranger][] file
manager. It adds three commands to work with currently selected files and
symlinks:

- `:annex_add` → `git annex add` + `git commit -a`
- `:annex_get` → `git annex get`
- `:annex_drop` → `git annex drop`
- `:annex_copy <remote>` → `git annex copy --to=<remote>`
- `:annex_sync` → `git annex sync --fast --quiet`

You can move the `annex.py` manually to `$CONFIG_DIR/plugins` or run `make
install`.


[git-annex]: https://git-annex.branchable.com/
[ranger]: http://ranger.nongnu.org/
