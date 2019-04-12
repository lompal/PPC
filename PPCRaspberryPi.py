# noinspection PyPackageRequirements
import cv2
from base64 import b64encode
from uuid import UUID, getnode
from requests import get, post
# noinspection PyPackageRequirements
from socketio import AsyncClient
from asyncio import get_event_loop
from subprocess import check_output

# Octoprint settings
ip_addr = check_output(["hostname", "-I"]).split().pop().decode('utf-8')
api_key = ''
# Server auth settings
auth_token = ''
auth_session = ''
auth_uuid = str(UUID(int=getnode()))

sio = AsyncClient(logger=True)
# noinspection PyUnresolvedReferences
camera = cv2.VideoCapture(0)
# noinspection PyUnresolvedReferences
camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)
if not camera.isOpened():
    exit(1)


# noinspection PyUnusedLocal
@sio.on('echo')
async def echo(sid, message):
    print(message)


# Connection settings - information regarding the available baudrates, serial ports and the current connection state
# noinspection PyUnusedLocal
@sio.on('ppc_hw_api_conn')
async def ppc_hw_api_conn(sid):
    r = get('http://' + ip_addr + '/api/connection', params={'apikey': api_key})
    await sio.emit('ppc_srv_api_conn', r.text)


# Information about the current job
# noinspection PyUnusedLocal
@sio.on('ppc_hw_api_job_info')
async def ppc_hw_api_job_info(sid):
    r = get('http://' + ip_addr + '/api/job', params={'apikey': api_key})
    await sio.emit('ppc_srv_api_job_info', r.text)


# State of the printer - temperature information, sd state, general printer state
# noinspection PyUnusedLocal
@sio.on('ppc_hw_api_printer')
async def ppc_hw_api_printer(sid):
    r = get('http://' + ip_addr + '/api/printer', params={'apikey': api_key})
    await sio.emit('ppc_srv_api_printer', r.text)


# Handler for connection and job operations
# noinspection PyUnusedLocal, PyIncorrectDocstring
@sio.on('ppc_hw_api_ops_handle')
async def ppc_hw_api_ops_handle(sid, handler, action):
    """
    :param handler - 'connection' or 'job'
    :type handler: str
    :param action - the command to the issue, either 'connect', 'disconnect' or 'fake_ack' for connection handling
    and 'start', 'cancel', 'restart' or 'pause' for job operations
    :type action: str
    """
    post('http://' + ip_addr + '/api/{0}'.format(handler), params={'apikey': api_key}, json={
        'command': action, action == 'pause' and 'action': 'toggle'})


# noinspection PyUnusedLocal
@sio.on('ppc_hw_streaming')
async def ppc_hw_streaming(sid):
    read, image = camera.read()
    # noinspection PyUnresolvedReferences
    read, buffer = cv2.imencode('.jpg', image)
    await sio.emit('ppc_srv_streaming', b64encode(buffer))


# Sends any command to the printer via the serial interface
# noinspection PyUnusedLocal, PyIncorrectDocstring
@sio.on('ppc_hw_api_printer_console')
async def ppc_hw_api_printer_console(sid, g_code):
    """
    :param g_code: - list of commands to send to the printer
    :type g_code: list
    """
    post('http://' + ip_addr + '/api/printer/command', params={'apikey': api_key}, json={'commands': g_code})


async def run():
    await sio.connect('https://gthb.in', transports='polling', headers={
        'token': auth_token,
        'session': auth_session,
        'uuid': auth_uuid,
    })
    await sio.wait()


if __name__ == '__main__':
    loop = get_event_loop()
    loop.run_until_complete(run())
