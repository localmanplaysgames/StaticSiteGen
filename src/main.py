from textnode import *
from htmlnode import *
import re

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
    
def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

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

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT and len(extract_markdown_images(node.text)) != 0:
            extract = extract_markdown_images(node.text)
            markdown = f"![{extract[0][0]}]({extract[0][1]})"
            split = node.text.split(markdown, 1)
            if split[0] != "":
                new_nodes.append(TextNode(split[0], TextType.TEXT))
            new_nodes.append(TextNode(extract[0][0], TextType.IMAGE, extract[0][1]))
            while len(extract_markdown_images(split[1])) != 0:
                string = split[1]
                extract = extract_markdown_images(string)
                markdown = f"![{extract[0][0]}]({extract[0][1]})"
                split = string.split(markdown, 1)
                if split[0] != "":
                    new_nodes.append(TextNode(split[0], TextType.TEXT))
                new_nodes.append(TextNode(extract[0][0], TextType.IMAGE, extract[0][1]))
                string = split[1]
            if split[1] != "":
                new_nodes.append(TextNode(split[1], TextType.TEXT))
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT and len(extract_markdown_links(node.text)) != 0:
            extract = extract_markdown_links(node.text)
            markdown = f"[{extract[0][0]}]({extract[0][1]})"
            split = node.text.split(markdown, 1)
            if split[0] != "":
                new_nodes.append(TextNode(split[0], TextType.TEXT))
            new_nodes.append(TextNode(extract[0][0], TextType.LINK, extract[0][1]))
            while len(extract_markdown_links(split[1])) != 0:
                string = split[1]
                extract = extract_markdown_links(string)
                markdown = f"[{extract[0][0]}]({extract[0][1]})"
                split = string.split(markdown, 1)
                if split[0] != "":
                    new_nodes.append(TextNode(split[0], TextType.TEXT))
                new_nodes.append(TextNode(extract[0][0], TextType.LINK, extract[0][1]))
                string = split[1]
            if split[1] != "":
                new_nodes.append(TextNode(split[1], TextType.TEXT))
        else:
            new_nodes.append(node)
    return new_nodes

def main():
    print(TextNode('This is some anchor text', 'link', 'https://www.boot.dev').__repr__)

if __name__ == '__main__':
    main()