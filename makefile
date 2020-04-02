create-sub-data:
	docker-compose run fido python manage.py migrate
	docker-compose run fido python manage.py create_stub_data All
	docker-compose run fido python manage.py create_stub_forecast_data
	docker-compose run fido python manage.py create_test_user

setup-new-test-env:
	docker-compose down
	docker-compose run fido python manage.py migrate
	docker-compose run fido python manage.py create_stub_data All
	docker-compose run fido python manage.py create_stub_forecast_data
	docker-compose run fido python manage.py create_test_user
	docker-compose run fido python manage.py create_test_user --email=finance-admin@test.com --group="Finance Administrator"
	docker-compose run fido python manage.py create_test_user --email=finance-bp@test.com --group="Finance Business Partner/BSCE"

makemigrations:
	docker-compose run fido python manage.py makemigrations

migrate:
	docker-compose run fido python manage.py migrate