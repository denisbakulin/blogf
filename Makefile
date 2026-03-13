PORT=8000
DC = docker compose


.PHONY
api:
	uvicorn main:app --reload --host localhost --port  $(PORT)

.PHONY
bot:
	python -m interfaces.bot.main
