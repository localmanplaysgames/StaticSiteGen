import unittest
from main import *

class testMain(unittest.TestCase):
    def test_normal(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode('This is bold text', TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, 'This is bold text')
        self.assertEqual(html_node.to_html(), '<b>This is bold text</b>')

    def test_italic(self):
        node = TextNode('This is italic text', TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'i')
        self.assertEqual(html_node.value, 'This is italic text')
        self.assertEqual(html_node.to_html(), '<i>This is italic text</i>')

    def test_code(self):
        node = TextNode('This is code', TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'code')
        self.assertEqual(html_node.value, 'This is code')
        self.assertEqual(html_node.to_html(), '<code>This is code</code>')

if __name__ == '__main__':
    unittest.main()