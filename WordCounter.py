text = """Also known as text template, text shortcut, text expansion tool."""


def WordCounter(text):
	cnt = text.count("text")
	print("That word appeared", cnt, "times.")


WordCounter(text)