#!/bin/sh
# Pre-commit hook: runs the test suite before allowing a commit.
# Install: make install-hooks

echo "Running tests before commit..."
python manage.py test --settings=config.settings.test

if [ $? -ne 0 ]; then
    echo ""
    echo "Tests failed. Commit aborted."
    echo "Fix the failing tests or use 'git commit --no-verify' to skip this check."
    exit 1
fi

echo "All tests passed."
