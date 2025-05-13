# copilot generated 'cause lazy. learn how to do tests later.

import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode('This is a text node', TextType.BOLD)
        node2 = TextNode('This is a text node', TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_text(self):
        node1 = TextNode('Text A', TextType.NORMAL)
        node2 = TextNode('Text B', TextType.NORMAL)
        self.assertNotEqual(node1, node2)

    def test_not_eq_type(self):
        node1 = TextNode('Same text', TextType.BOLD)
        node2 = TextNode('Same text', TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_not_eq_url(self):
        node1 = TextNode('Link', TextType.LINK, url='http://a.com')
        node2 = TextNode('Link', TextType.LINK, url='http://b.com')
        self.assertNotEqual(node1, node2)

    def test_eq_with_url(self):
        node1 = TextNode('Image', TextType.IMAGE, url='img.png')
        node2 = TextNode('Image', TextType.IMAGE, url='img.png')
        self.assertEqual(node1, node2)

    def test_repr(self):
        node = TextNode('Hello', TextType.NORMAL)
        self.assertEqual(repr(node), 'TextNode(Hello, normal, None)')

    def test_accepts_str_texttype(self):
        node = TextNode('Hello', 'bold')
        self.assertEqual(node.text_type, TextType.BOLD)

if __name__ == '__main__':
    unittest.main()