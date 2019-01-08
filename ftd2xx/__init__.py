import sys

from .ftd2xx import *


__all__ = ['call_ft', 'listDevices', 'getLibraryVersion',
           'createDeviceInfoList', 'getDeviceInfoDetail', 'open',
           'openEx', 'FTD2XX',  \
           'DeviceError', 'ft_program_data']

if sys.platform == 'win32':
    __all__ += ['w32CreateFile']
else:
    __all__ += ['getVIDPID', 'setVIDPID']