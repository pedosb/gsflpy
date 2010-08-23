from distutils.core import setup, Extension

gsflc = Extension('gsflc',
      sources = ['busca.c'])

setup (name = 'gsflc',
      version = '0.01',
      description = 'That is a package that implements ' + \
	    'the search for sentences in the lattice',
      author = 'Pedro Batista',
      author_email = 'edokdz@gmail.com',
      ext_modules = [gsflc])
