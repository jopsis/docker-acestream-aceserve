# Copyright (C) 2009 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

__author__ = 'Damon Kohler <damonkohler@gmail.com>'

import collections
import json
import os
import socket
import sys
import hashlib
import platform

PORT = os.environ.get('AP_PORT')
HOST = os.environ.get('AP_HOST')
HANDSHAKE = os.environ.get('AP_HANDSHAKE')
Result = collections.namedtuple('Result', 'id,result,error')


class Android(object):

  def __init__(self, addr=None):
    self.use_fake_host = False

    if addr is None:
      if HOST is None:
        self.use_fake_host = True
      else:
        addr = HOST, PORT

    if not self.use_fake_host:
      self.conn = socket.create_connection(addr)
      self.client = self.conn.makefile(mode='rw')
      self.id = 0
      if HANDSHAKE is not None:
        self._authenticate(HANDSHAKE)

  def _rpc(self, method, *args):
    data = {'id': self.id,
            'method': method,
            'params': args}
    request = json.dumps(data)
    self.client.write(request+'\n')
    self.client.flush()
    response = self.client.readline()
    self.id += 1
    result = json.loads(response)
    if result['error'] is not None:
      print(result['error'])
    # namedtuple doesn't work with unicode keys.
    # return Result(id=result['id'], result=result['result'], error=result['error'], )
    return result['result']

  def _fake_rpc(self, method, *args):
    if method == "getAceStreamHome":
      return "/dev/shm"
    elif method == "makeToast":
      print(args[0] if args else "")
      return None
    elif method == "getDisplayLanguage":
      return "en"
    elif method == "getRAMSize":
      return 1024*1024*1024
    elif method == "getMaxMemory":
      return 1024*1024*1024
    elif method == "getDeviceId":
      return "d3efefe5-4ce4-345b-adb6-adfa3ba92eab"
    elif method == "getAppId":
      return "d3efefe5-4ce4-345b-adb6-adfa3ba92eab"
    elif method == "getDeviceManufacturer":
      return "Samsung"
    elif method == "getDeviceModel":
      return "Galaxy S3"
    elif method == "getDeviceName":
      return "Samsung Galaxy S3"
    elif method == "getDeviceProductName":
      return "Galaxy_S3"
    elif method == "getDeviceABI":
      return "arm64-v8a"
    elif method == "onSettingsUpdated":
      return None
    elif method == "onEvent":
      return None
    elif method == "getAppVersionCode":
      return "302131302"
    elif method == "getArch":
      arch = platform.machine()
      if arch == 'aarch64':
        return 'arm64-v8a'
      elif arch.startswith('arm'):
        return 'armeabi-v7a'
      else:
        return arch
    elif method == "getLocale":
      return "en-US"
    elif method == "isAndroidTv":
      return False
    elif method == "hasBrowser":
      return False
    elif method == "hasWebView":
      return False
    elif method == "getMemoryClass":
      return 64
    elif method == "publishFileReceiverState":
      return None
    elif method == "adjustCacheSettings":
      return None
    elif method == "getAppInfo":
      return json.dumps({
        "appId": "d3efefe5-4ce4-345b-adb6-adfa3ba92eab",
        "appVersionCode": "302131302",
        "deviceId": "d3efefe5-4ce4-345b-adb6-adfa3ba92eab",
        "arch": platform.machine(),
        "locale": "en-US",
        "isAndroidTv": False,
        "hasBrowser": False,
        "hasWebView": False
      })
    elif method == "onAuthUpdated":
      return None
    else:
      raise Exception("Unknown method: %s" % (method,))

  def __getattr__(self, name):
    def rpc_call(*args):
      if self.use_fake_host:
        return self._fake_rpc(name, *args)
      else:
        return self._rpc(name, *args)
    return rpc_call
