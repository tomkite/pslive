#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Tom Cai <1tomcai@gmail.com>'
__date__ = '2019-08-11'
__summary__ = 'Define an abstract lookup class.'

from collections.abc import MutableSet
import os

class Lookup(MutableSet):

    def __init__(self, homedir=os.getenv('HOME')+'/.lookup/', ):
        """Initialize a Lookup object
        """
        pass

    def __contains__(self, key):

    __contains__, __iter__, __len__, add, discard

    @abc.abstractmethod
    def fetch_entries(self):
        pass

    @abc.abstractmethod
    def fetch_entries(self):
        pass

    @abc.abstractmethod
    def fetch_entries(self):
        pass

    @abc.abstractmethod
    def fetch_entries(self):
        pass

