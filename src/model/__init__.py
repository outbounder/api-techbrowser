from google.appengine.ext import db

from Entry import Entry
from Entry import saveEntry
from Owner import Owner
from EntryTag import Tag
from EntryTag import TagProposal
from EntryTag import saveTag
from EntryNameTag import NameTag
from EntryNameTag import NameProposal
from EntryNameTag import saveNameTag

def getTagTerms(tagsLine):
    if len(tagsLine) > 0:
        return tagsLine.split(" ")
    else:
        return []