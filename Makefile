.PHONY: install run web dev

install:
	@echo "Set up per-app environments inside apps/backend and apps/frontend"

run:
	@echo "Run your backend entrypoint when implemented (e.g., python apps/backend/ed_fox/runner/run_local.py)"

web:
	@echo "Start the frontend dev server when scaffolded (e.g., npm run dev in apps/frontend)"

dev:
	@echo "1) make run  # backend"
	@echo "2) make web  # frontend"