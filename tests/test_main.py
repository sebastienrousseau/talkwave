import unittest
from argparse import Namespace
from __main__ import parse_args


class TestMain(unittest.TestCase):
    def test_parse_args(self):
        args = parse_args([
            '-p', 'test',
            '-t', '10',
            '-T', '0.5',
            '-m', '1',
            '-u', 'example_user',
            '-r', '5',
            '-s',
            '-o', 'csv'
        ])
        self.assertEqual(args, Namespace(
            prompt='test',
            tokens=10,
            temperature=0.5,
            model=1,
            user_id='example_user',
            rate_limit_seconds=5,
            stop=True,
            output='csv'
        ))

        args = parse_args(['-p', 'test'])
        self.assertEqual(args, Namespace(
            model=1,
            prompt='test',
            tokens=50,
            temperature=0.5,
            user_id='example_user',
            rate_limit_seconds=5,
            stop=None,
            output='json'
        ))
