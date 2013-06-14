# Licensed to Cloudera, Inc. under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  Cloudera, Inc. licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

try:
  import json
except ImportError:
  import simplejson as json

from django.utils.translation import ugettext as _

from desktop.lib.rest.resource import Resource


class SqoopResource(Resource):
  """
  Sqoop resources provide extra response headers.
  @see desktop.lib.rest.resource
  """

  def invoke(self, method, relpath=None, params=None, data=None, headers=None):
    """
    Invoke an API method.
    Look for sqoop-error-code and sqoop-error-message.
    @return: Raw body or JSON dictionary (if response content type is JSON).
    """
    path = self._join_uri(relpath)
    resp = self._client.execute(method,
                                path,
                                params=params,
                                data=data,
                                headers=headers)
    body = self._get_body(resp)

    if resp.getcode() == 200:
      self._client.logger.debug(
          "%(method)s Got response:\n%(headers)s\n%(body)s" % {
            'method': method,
            'headers': resp.headers,
            'body': body
      })
      # Sqoop always uses json
      return self._format_body(resp, body)
    else:
      # Body will probably be a JSON formatted stacktrace
      body = self._format_body(resp, body)
      msg_format = "%(method)s Sqoop Error (%s): %s\n\t%s"
      args = (resp.headers['sqoop-error-code'], resp.headers['sqoop-error-message'], body)
      self._client.logger.error(msg_format % args)
      raise IOError(_(msg_format) % args)

  def delete(self, relpath=None, params=None, headers=None):
    """
    Invoke the DELETE method on a resource.
    @param relpath: Optional. A relative path to this resource's path.
    @param params: Key-value data.

    @return: A dictionary of the JSON result.
    """
    return self.invoke("DELETE", relpath, params, None, headers)


  def post(self, relpath=None, params=None, data=None, headers=None):
    """
    Invoke the POST method on a resource.
    @param relpath: Optional. A relative path to this resource's path.
    @param params: Key-value data.
    @param data: Optional. Body of the request.
    @param contenttype: Optional.

    @return: A dictionary of the JSON result.
    """
    return self.invoke("POST", relpath, params, data, headers)


  def put(self, relpath=None, params=None, data=None, headers=None):
    """
    Invoke the PUT method on a resource.
    @param relpath: Optional. A relative path to this resource's path.
    @param params: Key-value data.
    @param data: Optional. Body of the request.
    @param contenttype: Optional.

    @return: A dictionary of the JSON result.
    """
    return self.invoke("PUT", relpath, params, data, headers)


  def _make_headers(self, contenttype=None):
    if contenttype:
      return { 'Content-Type': contenttype }
    return None