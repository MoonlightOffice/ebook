import os

from ebooklib import epub

def create_epub(title: str, author: str, dir: str):
	book = epub.EpubBook()

	# set metadata
	book.set_title(title)
	book.add_author(author)

	# Get path list of html files

	files: list[str] = os.listdir(dir)
	files_count = len(files)

	for file in files:
		splitted_file_name = file.split('.')
		
		if len(splitted_file_name) != 2:
			files_count -= 1

		if splitted_file_name[-1] != 'html':
			files_count -= 1

	for i in range(0, files_count):
		# create chapter
		chapter = epub.EpubHtml(title=f'{i}', file_name=f'{i}.xhtml')
		with open(f"{dir}/{i}.html") as f:
			chapter.content = f.read()

		# add chapter
		book.add_item(chapter)

		# basic spine
		book.spine.append(chapter)

	# add default NCX and Nav file
	book.add_item(epub.EpubNcx())
	book.add_item(epub.EpubNav())


	# write to the file
	epub.write_epub(f'{title}.epub', book, {})

if __name__ == '__main__':
	create_epub(
		"TItle",
		"Author name",
		"./dir_to_html_files",
	)
