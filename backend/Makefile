#set path=%path:git\bin=;%
#set path=%path:mingw64\bin=;%
#set path=%path:usr\bin=;%


build:
	docker-compose build

up:
	docker-compose up

req:
	pip install -r requirements.txt

mig:
	alembic revision --autogenerate -m "$(NAME)"

mig-up:
	alembic upgrade $(NAME)

mig-down:
	alembic downgrade $(NAME)