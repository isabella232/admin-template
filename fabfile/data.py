#!/usr/bin/env python

"""
Commands that update or process the application data.
"""
import app_config

from fabric.api import execute, hide, local, task, settings, shell_env
from fabric.state import env
from models import models

@task
def bootstrap_db():
    """
    Build the database.
    """
    create_db()
    create_tables()
    load_stub_data()


@task
def create_db():
    with settings(warn_only=True), hide('output', 'running'):
        if env.get('settings'):
            execute('servers.stop_service', 'uwsgi')
            execute('servers.stop_service', 'deploy')

        with shell_env(**app_config.DATABASE):
            local('dropdb --if-exists %s' % app_config.DATABASE['PGDATABASE'])

        if not env.get('settings'):
            local('psql -c "DROP USER IF EXISTS %s;"' % app_config.DATABASE['PGUSER'])
            local('psql -c "CREATE USER %s WITH SUPERUSER PASSWORD \'%s\';"' % (app_config.DATABASE['PGUSER'], app_config.DATABASE['PGPASSWORD']))

        with shell_env(**app_config.DATABASE):
            local('createdb %s' % app_config.DATABASE['PGDATABASE'])

        if env.get('settings'):
            execute('servers.start_service', 'uwsgi')
            execute('servers.start_service', 'deploy')

@task
def create_tables():
    models.TestModel.create_table()

@task
def load_stub_data():
    with shell_env(**app_config.DATABASE):
        local('psql %s -c "COPY testmodel from \'`pwd`/data/test.csv\' DELIMITER\',\' CSV HEADER"' % app_config.DATABASE['PGDATABASE'])