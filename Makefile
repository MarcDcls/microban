.PHONY: sync setup run stop battery

HOST ?= microban

sync:
	rsync -avz \
		--exclude='.git' \
		--exclude='.venv' \
		--exclude='__pycache__' \
		--exclude='cad' \
		--exclude='docs' \
		./ $(HOST):microban

setup: sync
	ssh $(HOST) "bash -l -c 'cd microban && uv sync'"

run: sync
	ssh -tt $(HOST) "bash -l -c 'cd microban && uv run src/main.py'"

stop:
	ssh -tt $(HOST) "bash -l -c 'cd microban && uv run src/stop.py'"

battery: sync
	ssh $(HOST) "bash -l -c 'cd microban && uv run src/battery.py'"