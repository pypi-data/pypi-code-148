from html.parser import HTMLParser
import pathlib
import os

# a context manager for temperarily change the working directory.
class working_directory(object):
  def __init__(self,path):
    self.old_dir = os.getcwd()
    self.new_dir = path
  def __enter__(self):
    if self.new_dir is not None:
      os.chdir(self.new_dir)
  def __exit__(self,type,value,traceback):
    if self.new_dir is not None:
      os.chdir(self.old_dir)

class TagWithSourceParser(HTMLParser):
  def __init__(self,*args,**kwargs):
    super().__init__(*args,**kwargs)
    self.sources = list()

  def handle_starttag(self, tag, attrs):
    attrs = dict(attrs)
    if 'src' in attrs:
      self.sources.append(pathlib.Path(attrs["src"]))
