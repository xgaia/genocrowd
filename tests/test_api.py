from pkg_resources import get_distribution

from . import GenocrowdTestCase


class TestApi(GenocrowdTestCase):
    """Test Genocrowd API"""

    def test_hello(self, client):
        """Test /api/hello route"""
        response = client.client.get('/api/hello')

        assert response.status_code == 200
        assert response.json == {
            "error": False,
            "errorMessage": '',
            "message": "Welcome to Genocrowd"
        }

        # Log user
        client.log_user("jdoe")

        response = client.client.get('/api/hello')

        assert response.status_code == 200
        assert response.json == {
            "error": False,
            "errorMessage": '',
            "message": "Hello John Doe, Welcome to Genocrowd!"
        }

    def test_start(self, client):
        """Test /api/start route"""
        # Non logged
        expected_config_nouser = {
            'footerMessage': client.get_config('genocrowd', 'footer_message'),
            "version": get_distribution('genocrowd').version,
            "commit": None,
            "gitUrl": "https://github.com/annotons/genocrowd",
            "disableIntegration": client.get_config('genocrowd', 'disable_integration', boolean=True),
            "prefix": client.get_config('triplestore', 'prefix'),
            "namespace": client.get_config('triplestore', 'namespace'),
            "proxyPath": "/",
            "user": {},
            "logged": False
        }
        response = client.client.get('/api/start')
        assert response.status_code == 200
        assert response.json == {
            "error": False,
            "errorMessage": '',
            "config": expected_config_nouser
        }

        # Create database and user
        client.create_two_users()

        # Jdoe (admin) logged
        client.log_user("jdoe")

        expected_config_jdoe = expected_config_nouser
        expected_config_jdoe["logged"] = True
        expected_config_jdoe["user"] = {
            'id': 1,
            'ldap': False,
            'fname': "John",
            'lname': "Doe",
            'username': "jdoe",
            'email': "jdoe@genocrowd.org",
            'admin': True,
            'blocked': False,
            "quota": 0,
            'apikey': "0000000001",
            'galaxy': {"url": "http://localhost:8081", "apikey": "admin"}
        }
        response = client.client.get('/api/start')

        assert response.status_code == 200
        assert response.json == {
            "error": False,
            "errorMessage": '',
            "config": expected_config_jdoe
        }

        # jsmith (non admin) logged
        client.log_user("jsmith")

        expected_config_jsmith = expected_config_nouser
        expected_config_jsmith["logged"] = True
        expected_config_jsmith["user"] = {
            'id': 2,
            'ldap': False,
            'fname': "Jane",
            'lname': "Smith",
            'username': "jsmith",
            'email': "jsmith@genocrowd.org",
            'admin': False,
            'blocked': False,
            "quota": 0,
            'apikey': "0000000002",
            'galaxy': None
        }
        response = client.client.get('/api/start')

        assert response.status_code == 200
        assert response.json == {
            "error": False,
            "errorMessage": '',
            "config": expected_config_jsmith
        }
