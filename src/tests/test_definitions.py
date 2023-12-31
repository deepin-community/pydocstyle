"""Old parser tests."""

import os
import re
import pytest
from pydocstyle.violations import Error, ErrorRegistry
from pydocstyle.checker import check
from pydocstyle.config import ConfigurationParser

DEFAULT_PROPERTY_DECORATORS = ConfigurationParser.DEFAULT_PROPERTY_DECORATORS


@pytest.mark.parametrize('test_case', [
    'test',
    'unicode_literals',
    'nested_class',
    'capitalization',
    'comment_after_def_bug',
    'multi_line_summary_start',
    'all_import',
    'all_import_as',
    'superfluous_quotes',
    'noqa',
    'sections',
    'functions',
    'canonical_google_examples',
    'canonical_numpy_examples',
    'canonical_pep257_examples',
])
def test_complex_file(test_case):
    """Run domain-specific tests from test.py file."""
    case_module = __import__(f'test_cases.{test_case}',
                             globals=globals(),
                             locals=locals(),
                             fromlist=['expectation'],
                             level=1)
    test_case_dir = os.path.normcase(os.path.dirname(__file__))
    test_case_file = os.path.join(test_case_dir,
                                  'test_cases',
                                  test_case + '.py')
    results = list(
        check(
            [test_case_file],
            select=set(ErrorRegistry.get_error_codes()),
            ignore_decorators=re.compile('wraps|ignored_decorator'),
            property_decorators=DEFAULT_PROPERTY_DECORATORS,
        )
    )
    for error in results:
        assert isinstance(error, Error)
    results = {(e.definition.name, e.message) for e in results}
    assert case_module.expectation.expected == results
