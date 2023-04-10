# Copyright (C) 2023 Sebastien Rousseau.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
#
# See the License for the specific language governing permissions and
# limitations under the License.

"""The setup.py file for Python TalkWave."""

from setuptools import setup


LONG_DESCRIPTION = """
TalkWave is an AI chatbot for developers written in Python. It features a
simple HTML frontend and is designed to be accessible across various
browsers and devices.

TalkWave supports asynchronous operations and can handle multiple
requests simultaneously.
""".strip()

SHORT_DESCRIPTION = """
TalkWave is an AI chatbot for developers written in Python.
""".strip()

DEPENDENCIES = [

]

TEST_DEPENDENCIES = [

]

VERSION = '0.0.1'
URL = 'https://github.com/sebastienrousseau/talkwave'

setup(
    name='talkwave',
    version=VERSION,
    description=SHORT_DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url=URL,

    author='Sebastien Rousseau',
    author_email='sebastian.rousseau@gmail.com',
    license='Apache Software License',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
    ],

    keywords='talkwave, chatbot, artificial intelligence, machine learning, natural language processing, natural language processing, OpenAI, GPT-3, GPT3, GPT, 3, python',

    packages=['talkwave'],


    install_requires=DEPENDENCIES,
    tests_require=TEST_DEPENDENCIES,
)
