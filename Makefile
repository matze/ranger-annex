PLUGIN_DIR=$(if $(XDG_CONFIG_HOME),$(XDG_CONFIG_HOME),$(HOME)/.config)/ranger/plugins

install:
	install -Dm644 annex.py $(PLUGIN_DIR)/annex.py

uninstall:
	$(RM) $(PLUGIN_DIR)/annex.py
