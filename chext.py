#!/usr/bin/python
import getopt
import sys
import os

# TODO: add a follow linked directories option (-H)
# TODO: add options for changing linked file (-L --linked-only, -b --link-and-original)

def main():
	try:
		(opts, args) = getopt.getopt(sys.argv[1:], 'rdDHfpkLbi:nqvh', ['recursive', 'include-dirs', 'dirs-only', 'follow-links', 'force', 'prompt', 'skip-existing', 'linked-only', 'link-and-original', 'ignore=', 'dry-run', 'quiet', 'verbose', 'help'])
	except getopt.GetoptError, err:
		print str(err)
		sys.exit(2)
	
	recursive = False
	includeDirs = False
	dirsOnly = False
	followLinks = False
	
	targetExists = 'prompt'
	
	changeFile = True
	changeLinked = False
	
	ignoredNames = ['.DS_Store', '.localize']
	dryRun = False
	verbosity = 'normal'
	
	for o, a in opts: 
		if o in ("-r", '--recursive'):
			recursive = True 
		elif o in ('-d', '--include-dirs'):
			includeDirs = True
		elif o in ('-D', '--dirs-only'):
			dirsOnly = True
			includeDirs = True
		elif o in ('-H', '--follow-links'): #####################
			followLinks = True
		elif o in ('-f', '--no-prompt'):  #####################
			targetExists = 'force'
		elif o in ('-p', '--prompt'):  #####################
			targetExists = 'prompt'
		elif o in ('-k', '--skip-existing'):  #####################
			targetExists = 'skip'
		elif o in ('-L', '--linked-only'):  #####################
			changeLinked = True
			changeFile = False
		elif o in ('-b', '--link-and-original'):  #####################
			changeLinked = True
			changeFile = True
		elif o in ('-i', '--ignore'):
			ignoredNames.append(a)
		elif o in ('-n', '--dry-run'):
			dryRun = True
		elif o in ('-q', '--quiet') and not dryRun:
			verbosity = 'low'
		elif o in ('-v', '--verbose'):
			verbosity = 'high'
		elif o in ('-h', '--help'):
			usage()
			return
			
	if len(args) < 2:
		usage()
		return
	
	newExt = args[0]

	for path in args[1:]:
		path = os.path.expanduser(path)
		if os.path.isdir(path):
			if recursive == True:
				for (dirPath, dirNames, fileNames) in os.walk(path, topdown=False):
					targets = list()
					if not dirsOnly:
						targets = fileNames
					if includeDirs:
						targets = targets + dirNames
					for target in targets:
						rename(dirPath, target, newExt, dryRun, verbosity, ignoredNames, targetExists)
			elif includeDirs:
				# here path is a directory and recursive is false
				rename('', path, newExt, dryRun, verbosity, ignoredNames, targetExists)
		elif not dirsOnly: 
			# here path is a file
			rename('', path, newExt, dryRun, verbosity, ignoredNames, targetExists)

def rename(dirPath, fileName, newExt, dryRun, verbosity, ignoredNames, targetExists):
	(base, ext) = os.path.splitext(fileName)
	if fileName not in ignoredNames:
		oldPath = os.path.join(dirPath, fileName)
		newPath = os.path.join(dirPath, base) + '.' + newExt
		if not os.path.exists(newPath) or targetExists == 'force' or newPath != oldPath or targetExists != 'skip' and raw_input('Replace %s [y/n]:' % newPath).startswith('y'):
			if not dryRun:
				os.rename(oldPath, newPath)
			if verbosity == 'high':
				print '%s -> %s' % (oldPath, newPath)
			elif verbosity == 'normal':
				print newPath
	
def usage():
	print 'usage:  chext [-r] [-dD] [-fpk] [-ifilename] [-qv] [-n] newExtension paths ...'
	print '        chext -h'
	print ''
	print '  -r --recursive:  Include items in subdirectories'
	print '  -d --include-dirs:  Apply new extension to directories'
	print '  -D --dirs-only:  Apply new extension to directories but not files. Implies -d'
	print '  -f --no-prompt:  If a target file exists it will be overwritten. Replaces previous -p and -k'
	print '  -p --prompt:  If a target file exists an overwrite prompt is displayed. Replaces previous -f and -k. This is the default'
	print '  -k --skip:  If a target file exists the source file will not be moved. Replaces previous -f and -p'
	print '  -i --ignore:  Specifies a full filename to skip if encountered. .DS_Store and .localize are ignored by default.'
	print '  -q --quiet:  No output except error info. Replaces previous -v'
	print '  -v --verbose:  Verbose output. Replaces previous -q'
	print '  -n --dry-run:  No files are renamed. Note: behaves differently if more than one file maps to the same target'
	print '  -h --help:  Displays this information'
	
main()