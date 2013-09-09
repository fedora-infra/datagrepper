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

import fedmsg.encoding
import os
import re
import shutil
import tarfile
import tempfile
import time
import urllib

try:
    import lzma
except ImportError:
    import backports.lzma as lzma

import datanommer.models as dm
import datagrepper.app
from datagrepper.util import assemble_timerange

OPTIONS = ('start', 'end', 'delta')
LIST_OPTIONS = ('user', 'package', 'category', 'topic', 'meta')


class DataQuery(object):
    """
    Handles parsing queries, saving them, and filtering objects based on the
    query.
    """

    @classmethod
    def from_request_args(cls, request_args):
        obj = cls()
        opts = dict()

        for arg in OPTIONS:
            opts[arg] = request_args.get(arg, None)

        for arg in LIST_OPTIONS:
            opts[arg] = request_args.getlist(arg)

        opts['start'], opts['end'], opts['delta'] = \
            assemble_timerange(opts['start'], opts['end'], opts['delta'])

        obj.options = opts
        return obj

    @classmethod
    def from_database(cls, job_obj):
        obj = cls()
        obj.options = job_obj.dataquery['options']
        return obj

    def database_repr(self):
        return {'options': self.options}

    def run_query(self, output_prefix):
        """
        Returns the location of the output file, which is either a .json.xz or
        a .tar.xz. The output filename will start with output_prefix.
        """
        def output_file(messages, dir):
            earliest = int(time.mktime(messages[0].timestamp.timetuple()))
            latest = int(time.mktime(messages[-1].timestamp.timetuple()))
            filename = 'messages_{0}_{1}.json'.format(earliest, latest)
            with open(os.path.join(dir, filename), 'w') as f:
                f.write(fedmsg.encoding.dumps(messages))
            return filename

        dir = tempfile.mkdtemp(prefix='datagrepper-tmp')
        total, pages, query = dm.Message.grep(
            start=(self.options['start'] and
                   datetime.fromtimestamp(self.options['start'])),
            end=(self.options['end'] and
                 datetime.fromtimestamp(self.options['end'])),
            rows_per_page=None,
            users=self.options['user'],
            packages=self.options['package'],
            categories=self.options['category'],
            topics=self.options['topic'],
            defer=True,
        )

        messages = []
        files = []
        for message in query.yield_per(10):
            messages.append(message)
            if len(messages) >= 10000:
                files.append(output_file(messages, dir))
                messages = []
        files.append(output_file(messages, dir))

        if len(files) > 1:
            extension = '.tar.xz'
            fname = os.path.join(datagrepper.app.app.config['JOB_OUTPUT_DIR'],
                                 output_prefix + extension)
            with lzma.open(fname, 'w') as lzmaobj:
                with tarfile.open(fileobj=lzmaobj, mode='w') as tar:
                    for filename in files:
                        tar.add(os.path.join(dir, filename), arcname=filename)
        else:
            extension = '.json.xz'
            fname = os.path.join(datagrepper.app.app.config['JOB_OUTPUT_DIR'],
                                 output_prefix + extension)
            with lzma.open(fname, 'w') as lzmaobj:
                with open(os.path.join(dir, files[0]), 'r') as f:
                    while True:
                        line = f.readline(int(10e6))  # limit to 10 MB per read
                        if not line:
                            break
                        lzmaobj.write(line)

        shutil.rmtree(dir, ignore_errors=True)
        return output_prefix + extension
