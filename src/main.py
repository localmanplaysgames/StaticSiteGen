from textnode import *
from htmlnode import *

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {'href': text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        raise Exception('Not a valid text type.')
    
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            substrings = node.text.split(delimiter)
            if len(substrings) % 2 == 0:
                raise Exception('Invalid markdown text provided.')
            for i in range (0, len(substrings)):
                if i == 0 or i % 2 == 0:
                    new_nodes.append(TextNode(substrings[i], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(substrings[i], text_type))
    return new_nodes

def main():
    print(TextNode('This is some anchor text', 'link', 'https://www.boot.dev').__repr__)

if __name__ == '__main__':
    main()