import importlib
import sys
import unittest
from pathlib import Path

import src


def discover_test_modules() -> list[str]:
    # Search for unit test directories
    root_path = Path(src.__file__).parent
    matched_dirs = [directory for directory in root_path.glob('**') if directory.name == 'unittests']

    # Convert the matched directories to relative paths
    matched_modules = [directory.relative_to(root_path.parent) for directory in matched_dirs]

    # Turn the paths into import strings
    return ['.'.join(path.parts) for path in matched_modules]


def main() -> bool:
    # Discover all unit tests
    ut_module_names = discover_test_modules()

    # Build up our test suite
    suite = unittest.TestSuite()
    for module_path in ut_module_names:
        # Import the module
        module = importlib.import_module(module_path, module_path)

        # Add tests discovered in the module
        discovered_suite = unittest.defaultTestLoader.loadTestsFromModule(module)
        suite.addTest(discovered_suite)

    # Run the tests
    return unittest.TextTestRunner(verbosity=5).run(suite).wasSuccessful()


if __name__ == '__main__':
    result = main()
    sys.exit(0 if result else 1)
