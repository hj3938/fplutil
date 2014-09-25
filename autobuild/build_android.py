#!/usr/bin/python
# Copyright 2014 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Android automated build script.

This script may be used for turnkey android builds of fplutil.

Optional environment variables:

ANDROID_SDK_HOME = Path to the Android SDK. Required if it is not passed on the
command line.
NDK_HOME = Path to the Android NDK. Required if it is not in passed on the
command line.
MAKE_FLAGS = String to override the default make flags with for ndk-build.
ANT_PATH = Path to ant executable. Required if it is not in $PATH or passed on
the command line.
"""

import argparse
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
import buildutil.android
import buildutil.common

GOOGLETEST_DEFAULT_PATH = os.path.abspath('..')

def main():
  parser = argparse.ArgumentParser()
  buildutil.android.BuildEnvironment.add_arguments(parser)

  parser.add_argument('-G', '--gtest_path',
                        help='Path to Google Test', dest='gtest_path',
                        default=GOOGLETEST_DEFAULT_PATH)

  args = parser.parse_args()

  env = buildutil.android.BuildEnvironment(args)

  gtest_arg = 'GOOGLETEST_PATH="%s"' % args.gtest_path
  if env.make_flags:
    env.make_flags = '%s %s' % (env.make_flags, gtest_arg)
  else:
    env.make_flags = gtest_arg

  env.git_clean()
  (rc, errmsg) = env.build_all()
  if (rc == 0):
    env.make_archive(['libs', 'apks', 'libfplutil/include',
      'libfplutil/jni'], 'output.zip', exclude=['objs', 'objs-debug'])
  else:
    print >> sys.stderr, errmsg

  return rc

if __name__ == '__main__':
  sys.exit(main())
