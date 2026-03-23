.PHONY: install-hooks test coverage

install-hooks:
	chmod +x scripts/pre-commit.sh
	ln -sf ../../scripts/pre-commit.sh .git/hooks/pre-commit
	@echo "Pre-commit hook installed."

test:
	python manage.py test --settings=config.settings.test

coverage:
	coverage run manage.py test --settings=config.settings.test && coverage report --show-missing
