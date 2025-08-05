shell:
	poetry shell

run:
	python main.py --collection collections.yaml

build:
	pyinstaller --onefile --name=hyr main.py
