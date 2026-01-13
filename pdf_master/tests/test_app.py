import unittest
from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index_get(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Upload PDF', response.data)

    def test_index_post_no_file(self):
        response = self.app.post('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Upload PDF', response.data)

    def test_index_post_invalid_file(self):
        response = self.app.post('/', data={'pdf': (None, 'invalid.pdf')})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Upload PDF', response.data)

    def test_index_post_word_conversion(self):
        with open('tests/test_file.pdf', 'rb') as f:
            response = self.app.post('/', data={'pdf': f, 'format': 'word'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.headers['Content-Type'], 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')

    def test_index_post_text_conversion(self):
        with open('tests/test_file.pdf', 'rb') as f:
            response = self.app.post('/', data={'pdf': f, 'format': 'text'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.headers['Content-Type'], 'text/plain')

    def test_index_post_images_conversion(self):
        with open('tests/test_file.pdf', 'rb') as f:
            response = self.app.post('/', data={'pdf': f, 'format': 'images'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.headers['Content-Type'], 'application/zip')

if __name__ == '__main__':
    unittest.main()