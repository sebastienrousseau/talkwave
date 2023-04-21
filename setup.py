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

from setuptools import setup

with open('README.md', 'r') as fh:
    LONG_DESCRIPTION = fh.read().strip()

SHORT_DESCRIPTION = (
    "TalkWave is an AI chatbot for developers written in Python."
)

DEPENDENCIES = [
    'Flask==2.2.3',
    'openai==0.27.2',
    'python-dotenv==1.0.0',
    'requests==2.28.2',
    'tabulate==0.9.0'
]

TEST_DEPENDENCIES = [
    "coverage>=7.2.3",
    "pytest-cov>=4.0.0",
    "pytest>=7.3.0",
]

VERSION = '0.0.6'
URL = 'https://github.com/sebastienrousseau/talkwave'

setup(
    name='talkwave',
    version=VERSION,
    description=SHORT_DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url=URL,
    author='Sebastien Rousseau',
    author_email='sebastian.rousseau@gmail.com',
    license='Apache License 2.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],
    keywords=(
        'talkwave, chatbot, AI, machine learning'
        'natural language processing '
        'OpenAI GPT-3 GPT3 GPT python'
    ),
    packages=[

    ],
    install_requires=DEPENDENCIES,
    tests_require=TEST_DEPENDENCIES,
    python_requires='>=3.9',
)
