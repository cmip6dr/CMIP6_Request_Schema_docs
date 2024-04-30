# CMIP6r Request Schema docs

Documents and code used to maintain the CMIP6 Data Request Schema


Spreadsheets dreq2.xls and dreqSupp.xls are used.

A python script (ptxt.py) parses these and generates XML documents (dreq2Defn.xml, dreq2Sample.xml ..)

* dreq2Defn.xml is a document with a simple structure defining the tables of the data request. It is used to generate classes in the python library.
* dreq2Sample.xml is a sample file conformimg to te schema. Used to text the schema for consistency and as a starting point for new XML database.

An XSLT script is then used to generate the schema documents (dreq2.xsd,  ...):

> xsltproc ../../docs/xlst_xdsSchemaGen.xml out/$(targ)Defn.xml > out/$(targ)Schema.xsd 

The Makefile has commands to combine above into workflows.
