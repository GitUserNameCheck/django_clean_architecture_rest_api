
class DatabaseRouter:
    def db_for_read(self, model, **hints):
        if model._meta.model_name in ["client", "event", "serviceemployee"]:
            return 'mongo'
        return 'default'


    def db_for_write(self, model, **hints):
        if model._meta.model_name in ["client", "event", "serviceemployee"]:
            return 'mongo'
        return 'default'

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'clean_architecture':
            if model_name in ["client", "event", "serviceemployee"]:
                return db == 'mongo'
            return db == 'default'
        return None