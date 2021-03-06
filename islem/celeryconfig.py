## Broker settings.
broker_url = 'amqp://guest:guest@localhost:5672//'

# List of modules to import when the Celery worker starts.
imports = ('islem.tasks',)

## Using the database to store task state and results.
result_backend = 'db+postgresql://postgres:postgres@localhost:5432/denetim'

task_annotations = {'islem.tasks.add': {'rate_limit': '10/s'}}
