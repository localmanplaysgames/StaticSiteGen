from textnode import TextNode

def main():
    print(TextNode('This is some anchor text', 'link', 'https://www.boot.dev').__repr__)

if __name__ == "__main__":
    main()