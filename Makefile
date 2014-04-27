PLUGIN_DIR=$(if $(XDG_CONFIG_HOME),$(XDG_CONFIG_HOME),$(HOME)/.config)/ranger/plugins

install:
	install -D annex.py $(PLUGIN_DIR)/annex.py
