cd /usr/src/
python -m app.scripts
python -m app.scripts.db_migrate
python -m app.scripts.db_upgrade
