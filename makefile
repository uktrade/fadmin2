create-sub-data:
	docker-compose run fido python manage.py migrate
	docker-compose run fido python manage.py create_stub_data All
	docker-compose run fido python manage.py create_stub_forecast_data
	docker-compose run fido python manage.py create_test_user

setup-new_test_env:
	docker-compose down
	docker-compose run fido python manage.py migrate
	docker-compose run fido python manage.py create_stub_data All
	docker-compose run fido python manage.py create_stub_forecast_data
	docker-compose run fido python manage.py create_test_user

makemigrations:
	docker-compose run fido python manage.py makemigrations
