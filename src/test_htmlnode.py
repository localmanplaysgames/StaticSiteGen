import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(tag='a', value='Link', children=None, props={'href': 'http://example.com'})
        self.assertEqual(node.tag, 'a')
        self.assertEqual(node.value, 'Link')
        self.assertIsNone(node.children)
        self.assertEqual(node.props, {'href': 'http://example.com'})

    def test_repr(self):
        node = HTMLNode(tag='p', value='Hello', children=None, props=None)
        self.assertEqual(repr(node), 'HTMLNode(p, Hello, None, None)')

    def test_props_to_html(self):
        node = HTMLNode(tag='a', value='Link', props={'href': 'http://example.com', 'target': '_blank'})
        # The order of attributes in the string may vary, so check for both
        html = node.props_to_html()
        self.assertIn('href=http://example.com', html)
        self.assertIn('target=_blank', html)

    def test_props_to_html_missing_props(self):
        node = HTMLNode(tag='div', value='No props')
        with self.assertRaises(TypeError):
            node.props_to_html()

    def test_to_html_not_implemented(self):
        node = HTMLNode(tag='div', value='Test')
        with self.assertRaises(NotImplementedError):
            node.to_html()

if __name__ == '__main__':
    unittest.main()