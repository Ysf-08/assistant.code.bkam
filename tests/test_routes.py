import unittest
from app import app  # Assurez-vous que votre application Flask est importée correctement

class FlaskAppTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
        cls.client.testing = True

    def test_index(self):
        """Test que la route d'index retourne le template index.html."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<title>Index</title>', response.data)  # Vérifiez un élément de la page HTML

    def test_generate_tests_success(self):
        """Test la génération des tests unitaires."""
        code = "def add(a, b): return a + b"
        response = self.client.post('/generate-tests', data={'code': code})
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIn('tests', json_data)
        self.assertIsInstance(json_data['tests'], str)

    def test_generate_tests_no_code(self):
        """Test la génération des tests unitaires sans code."""
        response = self.client.post('/generate-tests', data={})
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertEqual(json_data['tests'], 'Erreur : aucun code fourni.')

    def test_generate_docs_success(self):
        """Test la génération de la documentation."""
        code = "def multiply(a, b): return a * b"
        response = self.client.post('/generate-docs', data={'code': code})
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIn('docs', json_data)
        self.assertIsInstance(json_data['docs'], str)

    def test_generate_docs_no_code(self):
        """Test la génération de la documentation sans code."""
        response = self.client.post('/generate-docs', data={})
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertEqual(json_data['docs'], 'Erreur : aucun code fourni.')

if __name__ == '__main__':
    unittest.main()
