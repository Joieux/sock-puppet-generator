import unittest
from unittest.mock import patch, MagicMock
from puppet_creator import generate_sock_puppet, fetch_identity_from_randomuser

class TestPuppetCreator(unittest.TestCase):

    @patch('puppet_creator.get_fake_identity')
    @patch('puppet_creator.get_face_image')
    @patch('puppet_creator.create_fastmail_alias')
    @patch('puppet_creator.generate_bio')
    @patch('puppet_creator.save_puppet_to_db')
    def test_generate_sock_puppet(self, mock_save, mock_bio, mock_email, mock_image, mock_identity):
        mock_identity.return_value = {
            "name": "John Doe",
            "dob": "1990-01-01",
            "location": "New York, USA",
            "email": "johndoe@example.com",
            "interests": ["Reading", "Traveling", "Music"]
        }
        mock_image.return_value = MagicMock(getvalue=MagicMock(return_value=b'image_data'))
        mock_email.return_value = "johndoe@example.com"
        mock_bio.return_value = "A brief bio."

        puppet = generate_sock_puppet()

        self.assertIsNotNone(puppet)
        self.assertEqual(puppet["name"], "John Doe")
        mock_save.assert_called_once()

    @patch('puppet_creator.requests.get')
    def test_fetch_identity_from_randomuser(self, mock_get):
        mock_get.return_value = MagicMock(
            status_code=200,
            json=MagicMock(return_value={
                "results
::contentReference[oaicite:0]{index=0}
 
                "results": [{
                    "name": {"first": "Alice", "last": "Smith"},
                    "dob": {"date": "1985-06-15T00:00:00Z"},
                    "location": {"city": "Paris", "country": "France"},
                    "email": "alice@example.com"
                }]
            })
        )

        from puppet_creator import fetch_identity_from_randomuser
        identity = fetch_identity_from_randomuser()

        self.assertIsNotNone(identity)
        self.assertEqual(identity["name"], "Alice Smith")
        self.assertEqual(identity["dob"], "1985-06-15T00:00:00Z")
        self.assertEqual(identity["location"], "Paris, France")
        self.assertEqual(identity["email"], "alice@example.com")
        self.assertIn("Reading", identity["interests"])  # default stub

if __name__ == '__main__':
    unittest.main()
