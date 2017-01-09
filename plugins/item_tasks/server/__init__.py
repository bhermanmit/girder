from girder import events
from girder.constants import registerAccessFlag, AccessType, TokenScope
from girder.plugins.jobs.constants import JobStatus
from girder.utility.model_importer import ModelImporter
from . import constants
from .rest import ItemTask


def _onJobSave(event):
    """
    If a job is finalized (i.e. success or failure status) and contains
    a temp token, we remove the token.
    """
    job = event.info

    if 'itemTaskTempToken' in job and job['status'] in (JobStatus.ERROR, JobStatus.SUCCESS):
        token = ModelImporter.model('token').load(
            job['itemTaskTempToken'], objectId=False, force=True)
        if token:
            ModelImporter.model('token').remove(token)

        # Remove the itemTaskTempToken field from the job
        ModelImporter.model('job', 'jobs').update({'_id': job['_id']}, update={
            '$unset': {'itemTaskTempToken': True}
        }, multi=False)


def load(info):
    registerAccessFlag(constants.ACCESS_FLAG_EXECUTE_TASK, name='Execute analyses', admin=True)
    TokenScope.describeScope(
        constants.TOKEN_SCOPE_EXECUTE_TASK, name='Execute tasks', description='Execute item tasks.')
    TokenScope.describeScope(
        constants.TOKEN_SCOPE_AUTO_CREATE_CLI, 'Item task auto-creation',
        'Create new CLIs via automatic introspection.', admin=True)

    ModelImporter.model('item').ensureIndex('meta.itemTaskSpec')
    ModelImporter.model('job', 'jobs').exposeFields(level=AccessType.READ, fields={
        'itemTaskId', 'itemTaskBindings'})

    events.bind('model.job.save.after', info['name'], _onJobSave)

    info['apiRoot'].item_task = ItemTask()
