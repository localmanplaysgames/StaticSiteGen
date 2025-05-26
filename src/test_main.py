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

    def test_extract_markdown_images_basic(self):
        text = "Here is an image: ![alt text](image.png)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("alt text", "image.png")])

    def test_extract_markdown_images_multiple(self):
        text = "![one](1.png) and ![two](2.jpg)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("one", "1.png"), ("two", "2.jpg")])

    def test_extract_markdown_images_empty_alt(self):
        text = "![](img.png)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("", "img.png")])

    def test_extract_markdown_images_empty_url(self):
        text = "![alt]()"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("alt", "")])

    def test_extract_markdown_images_no_match(self):
        text = "No images here!"
        result = extract_markdown_images(text)
        self.assertEqual(result, [])

    def test_extract_markdown_images_special_chars(self):
        text = "![a!@#](b$%^.png)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("a!@#", "b$%^.png")])

    def test_extract_markdown_links_basic(self):
        text = "Here is a [link](https://example.com)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("link", "https://example.com")])

    def test_extract_markdown_links_multiple(self):
        text = "[one](1.com) and [two](2.com)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("one", "1.com"), ("two", "2.com")])

    def test_extract_markdown_links_empty_text(self):
        text = "[](/empty)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("", "/empty")])

    def test_extract_markdown_links_empty_url(self):
        text = "[no url]()"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("no url", "")])

    def test_extract_markdown_links_no_match(self):
        text = "No links here!"
        result = extract_markdown_links(text)
        self.assertEqual(result, [])

    def test_extract_markdown_links_not_image(self):
        text = "![not a link](img.png)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [])

    def test_extract_markdown_links_special_chars(self):
        text = "[a!@#](b$%^.com)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("a!@#", "b$%^.com")])

    def test_split_nodes_image_basic(self):
        nodes = [TextNode("Here is ![alt](img.png) image.", TextType.TEXT)]
        result = split_nodes_image(nodes)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "Here is ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "alt")
        self.assertEqual(result[1].text_type, TextType.IMAGE)
        self.assertEqual(result[1].url, "img.png")
        self.assertEqual(result[2].text, " image.")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_split_nodes_image_multiple(self):
        nodes = [TextNode("A ![x](1.png) B ![y](2.jpg) C", TextType.TEXT)]
        result = split_nodes_image(nodes)
        self.assertEqual([n.text for n in result], ["A ", "x", " B ", "y", " C"])
        self.assertEqual([n.text_type for n in result],
                         [TextType.TEXT, TextType.IMAGE, TextType.TEXT, TextType.IMAGE, TextType.TEXT])
        self.assertEqual(result[1].url, "1.png")
        self.assertEqual(result[3].url, "2.jpg")
        
    def test_split_nodes_image_no_image(self):
        nodes = [TextNode("No images here.", TextType.TEXT)]
        result = split_nodes_image(nodes)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "No images here.")
        self.assertEqual(result[0].text_type, TextType.TEXT)

    def test_split_nodes_image_non_text_node(self):
        nodes = [TextNode("![alt](img.png)", TextType.IMAGE, "img.png")]
        result = split_nodes_image(nodes)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "![alt](img.png)")
        self.assertEqual(result[0].text_type, TextType.IMAGE)

    def test_split_nodes_image_empty_string(self):
        nodes = [TextNode("", TextType.TEXT)]
        result = split_nodes_image(nodes)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "")
        self.assertEqual(result[0].text_type, TextType.TEXT)

    def test_split_nodes_link_basic(self):
        nodes = [TextNode("Go to [site](url.com) now.", TextType.TEXT)]
        result = split_nodes_link(nodes)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "Go to ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "site")
        self.assertEqual(result[1].text_type, TextType.LINK)
        self.assertEqual(result[1].url, "url.com")
        self.assertEqual(result[2].text, " now.")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_split_nodes_link_no_link(self):
        nodes = [TextNode("No links here.", TextType.TEXT)]
        result = split_nodes_link(nodes)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "No links here.")
        self.assertEqual(result[0].text_type, TextType.TEXT)

    def test_split_nodes_link_non_text_node(self):
        nodes = [TextNode("[a](b.com)", TextType.LINK, "b.com")]
        result = split_nodes_link(nodes)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "[a](b.com)")
        self.assertEqual(result[0].text_type, TextType.LINK)

    def test_split_nodes_link_empty_string(self):
        nodes = [TextNode("", TextType.TEXT)]
        result = split_nodes_link(nodes)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "")
        self.assertEqual(result[0].text_type, TextType.TEXT)   

if __name__ == '__main__':
    unittest.main()