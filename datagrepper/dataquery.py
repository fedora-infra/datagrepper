# datagrepper - HTTP API for datanommer and the fedmsg bus
# Copyright (C) 2013  Red Hat, Inc. and others
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import re
import urllib

from datagrepper.util import assemble_timerange

# In these functions, "a" is the value from the datanommer message, and "b" is
# the value from the query definition. All of these functions must return True
# or False.
OPERATORS = {
    '==': lambda a, b: a == b,
    '!=': lambda a, b: a != b,
    '<': lambda a, b: a < b,
    '<=': lambda a, b: a <= b,
    '>': lambda a, b: a > b,
    '>=': lambda a, b: a >= b,
    '=~': lambda a, b: re.search(b, a) is not None,
    '!~': lambda a, b: re.search(b, a) is None,
    '=*': lambda a, b: b in a,
    '!*': lambda a, b: b not in a,
}
OPTIONS = ('start', 'end', 'delta')
LIST_OPTIONS = ('user', 'package', 'category', 'topic', 'meta')


class DataQuery(object):
    """
    Handles parsing queries, saving them, and filtering objects based on the
    query.
    """

    @classmethod
    def parse_from_request(cls, request_args):
        obj = cls()
        args, opts = dict(), dict()

        for arg in OPTIONS:
            opts[arg] = request_args.get(arg, None)

        for arg in LIST_OPTIONS:
            opts[arg] = request_args.getlist(arg)

        opts['start'], opts['end'], opts['delta'] = \
            assemble_timerange(opts['start'], opts['end'], opts['delta'])

        #for arg in (urllib.unquote(x) for x in request_args):
        for arg in request_args:
            # skip if this is an option
            if arg in OPTIONS + LIST_OPTIONS:
                continue
            # this can throw an exception, should be handled by caller
            key, oper, value = cls.parse_request_arg(arg)
            args[key] = (oper, value)
        obj.args = args
        obj.options = opts
        return obj

    @classmethod
    def parse_from_database(cls, job_obj):
        obj = cls()
        obj.args = job_obj.query['args']
        obj.options = job_obj.query['options']
        return obj

    @staticmethod
    def parse_request_arg(arg):
        """This method expects a request argument that has already been
        unescaped once (such that the operator is unescaped)."""
        for i in range(len(arg) - 1):
            if arg[i:i + 2] in OPERATORS:
                key, value = (urllib.unquote(x).decode('utf-8') for x in
                              arg.split(arg[i:i + 2], 1))
                return (key, arg[i:i + 2], value)
        # we couldn't find an operator
        raise ValueError(arg)

    def database_repr(self):
        return {'args': self.args,
                'options': self.options}

    def run_query(self):
        raise NotImplementedError()
