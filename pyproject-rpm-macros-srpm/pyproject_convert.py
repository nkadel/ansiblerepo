# Copyright 2019 Gordon Messmer <gordon.messmer@gmail.com>
#
# Upstream: https://github.com/gordonmessmer/pyreq2rpm
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from packaging.requirements import Requirement
from packaging.version import parse as parse_version

class RpmVersion():
    def __init__(self, version_id):
        version = parse_version(version_id)
        if isinstance(version._version, str):
            self.version = version._version
        else:
            self.epoch = version._version.epoch
            self.version = list(version._version.release)
            self.pre = version._version.pre
            self.dev = version._version.dev
            self.post = version._version.post

    def increment(self):
        self.version[-1] += 1
        self.pre = None
        self.dev = None
        self.post = None
        return self

    def __str__(self):
        if isinstance(self.version, str):
            return self.version
        if self.epoch:
            rpm_epoch = str(self.epoch) + ':'
        else:
            rpm_epoch = ''
        while len(self.version) > 1 and self.version[-1] == 0:
            self.version.pop()
        rpm_version = '.'.join(str(x) for x in self.version)
        if self.pre:
            rpm_suffix = '~{}'.format(''.join(str(x) for x in self.pre))
        elif self.dev:
            rpm_suffix = '~~{}'.format(''.join(str(x) for x in self.dev))
        elif self.post:
            rpm_suffix = '^post{}'.format(self.post[1])
        else:
            rpm_suffix = ''
        return '{}{}{}'.format(rpm_epoch, rpm_version, rpm_suffix)

def convert_compatible(name, operator, version_id):
    if version_id.endswith('.*'):
        return 'Invalid version'
    version = RpmVersion(version_id)
    if len(version.version) == 1:
        return 'Invalid version'
    upper_version = RpmVersion(version_id)
    upper_version.version.pop()
    upper_version.increment()
    return '({} >= {} with {} < {})'.format(
        name, version, name, upper_version)

def convert_equal(name, operator, version_id):
    if version_id.endswith('.*'):
        version_id = version_id[:-2] + '.0'
        return convert_compatible(name, '~=', version_id)
    version = RpmVersion(version_id)
    return '{} = {}'.format(name, version)

def convert_arbitrary_equal(name, operator, version_id):
    if version_id.endswith('.*'):
        return 'Invalid version'
    version = RpmVersion(version_id)
    return '{} = {}'.format(name, version)

def convert_not_equal(name, operator, version_id):
    if version_id.endswith('.*'):
        version_id = version_id[:-2]
        version = RpmVersion(version_id)
        lower_version = RpmVersion(version_id).increment()
    else:
        version = RpmVersion(version_id)
        lower_version = version
    return '({} < {} or {} > {})'.format(
        name, version, name, lower_version)

def convert_ordered(name, operator, version_id):
    if version_id.endswith('.*'):
        # PEP 440 does not define semantics for prefix matching
        # with ordered comparisons
        version_id = version_id[:-2]
        version = RpmVersion(version_id)
        if operator == '>':
            # distutils will allow a prefix match with '>'
            operator = '>='
        if operator == '<=':
            # distutils will not allow a prefix match with '<='
            operator = '<'
    else:
        version = RpmVersion(version_id)
    return '{} {} {}'.format(name, operator, version)

OPERATORS = {'~=': convert_compatible,
             '==': convert_equal,
             '===': convert_arbitrary_equal,
             '!=': convert_not_equal,
             '<=': convert_ordered,
             '<':  convert_ordered,
             '>=': convert_ordered,
             '>':  convert_ordered}

def convert(name, operator, version_id):
    return OPERATORS[operator](name, operator, version_id)

def convert_requirement(req):
    parsed_req = Requirement.parse(req)
    reqs = []
    for spec in parsed_req.specs:
        reqs.append(convert(parsed_req.project_name, spec[0], spec[1]))
    if len(reqs) == 0:
        return parsed_req.project_name
    if len(reqs) == 1:
        return reqs[0]
    else:
        reqs.sort()
        return '({})'.format(' with '.join(reqs))
