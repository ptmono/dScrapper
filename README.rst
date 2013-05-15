Purpose
=======

I regularly visit some web sites to get information/fun. I want to see
these things in my mail client(gnus). Furthermore I want to filtering
duplication and uninteresting stuffs.


Requirements
============

 - python
 - lxml
 - BeautifulSoup
 - PyQt4
 - IMDbPY
 - jquery(included)


Using
=====

::

 $ python main.py

will scrap the sites. And the scraped information will be sent to your
local mail box such as /var/spool/mail/USER. reporter.Mailer will
determines that.

You need a "container" to add a site. The container directory contains the
samples and templates which helps to scrap target site. For instance I
have created ytn.YtnBreakingContainer class. The name of all container has
the suffix "Container" to recognize this container to the program. And
import this class into __init__.py.

reporter.py contains ReporterCommon class. Inherit this object to report
your container automatically. The name of class is your container name
except "Container" suffix. You can filtering and reform your container in
this class. reporter.py contains the samples.


Todo
====

See todo.muse
