# list the contents of a .zip file
import zipfile

# list contents of a zip file
def list_contents(filepath):
	# open zip file
	with zipfile.ZipFile(filepath) as f:
		# list contents
		for name in f.namelist():
			print(name)

# protect the entry point
if __name__ == '__main__':
	# path to the zip to check
	path = '...'
	# list the contents of the zip file
	list_contents(path)
