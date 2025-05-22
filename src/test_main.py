import unittest
from main import *

class testMain(unittest.TestCase):
    def test_normal(self):
        node = TextNode("This is a text node", TextType.TEXT)
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

    def test_split_nodes_delimiter_basic(self):
        nodes = [TextNode("This is **bold** text", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(
            [n.text for n in result],
            ["This is ", "bold", " text"]
        )
        self.assertEqual(
            [n.text_type for n in result],
            [TextType.TEXT, TextType.BOLD, TextType.TEXT]
        )

    def test_split_nodes_delimiter_no_delimiter(self):
        nodes = [TextNode("No delimiter here", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "No delimiter here")
        self.assertEqual(result[0].text_type, TextType.TEXT)

    def test_split_nodes_delimiter_empty_string(self):
        nodes = [TextNode("", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "")
        self.assertEqual(result[0].text_type, TextType.TEXT)

    def test_split_nodes_delimiter_delimiter_at_start(self):
        nodes = [TextNode("**start** end", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual([n.text for n in result], ["", "start", " end"])
        self.assertEqual([n.text_type for n in result], [TextType.TEXT, TextType.BOLD, TextType.TEXT])

    def test_split_nodes_delimiter_delimiter_at_end(self):
        nodes = [TextNode("begin **end**", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual([n.text for n in result], ["begin ", "end", ""])
        self.assertEqual([n.text_type for n in result], [TextType.TEXT, TextType.BOLD, TextType.TEXT])

    def test_split_nodes_delimiter_odd_number_of_delimiters(self):
        nodes = [TextNode("A **B** C **", TextType.TEXT)]
        with self.assertRaises(Exception):
            split_nodes_delimiter(nodes, "**", TextType.BOLD)

    def test_split_nodes_delimiter_non_text_nodes(self):
        nodes = [
            TextNode("A", TextType.TEXT),
            TextNode("B", TextType.BOLD),
            TextNode("C **D** E", TextType.TEXT)
        ]
        result = split_nodes_delimiter(nodes, "**", TextType.ITALIC)
        self.assertEqual(result[0].text, "A")
        self.assertEqual(result[1].text, "B")
        self.assertEqual(result[2].text, "C ")
        self.assertEqual(result[3].text, "D")
        self.assertEqual(result[4].text, " E")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text_type, TextType.TEXT)
        self.assertEqual(result[3].text_type, TextType.ITALIC)
        self.assertEqual(result[4].text_type, TextType.TEXT)

if __name__ == '__main__':
    unittest.main()