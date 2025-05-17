import unittest
from htmlnode import *

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

    def test_leaf_to_html_p(self):
        node = LeafNode('p', 'Hello, world!')
        self.assertEqual(node.to_html(), '<p>Hello, world!</p>')

    def test_leaf_to_html_no_value(self):
        node = LeafNode('b')
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, 'no tag')
        self.assertEqual(node.to_html(), 'no tag')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_leafnode_with_props(self):
        node = LeafNode('a', 'Click me', {'href': 'https://example.com', 'target': '_blank'})
        self.assertEqual(node.tag, 'a')
        self.assertEqual(node.value, 'Click me')
        self.assertEqual(node.props, {'href': 'https://example.com', 'target': '_blank'})

    def test_parentnode_with_multiple_children(self):
        child1 = LeafNode('span', 'One')
        child2 = LeafNode('span', 'Two')
        parent = ParentNode('div', [child1, child2])
        self.assertEqual(parent.to_html(), '<div><span>One</span><span>Two</span></div>')

    def test_parentnode_missing_tag(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode('span', 'oops')]).to_html()

    def test_parentnode_missing_children(self):
        with self.assertRaises(ValueError):
            ParentNode('div', None).to_html()

    def test_leafnode_empty_string_value(self):
        node = LeafNode('p', '')
        self.assertEqual(node.to_html(), '<p></p>')

    def test_repr_leafnode(self):
        node = LeafNode('em', 'italic', {'class': 'highlight'})
        self.assertEqual(repr(node), "HTMLNode(em, italic, None, {'class': 'highlight'})")

if __name__ == '__main__':
    unittest.main()