# CMIP6r Requestr Schema docs

Documents and code used to maintain the CMIP6 Data Request Schema


Spreadsheets dreq2.xls and dreqSupp.xls are used.

A python script (ptxt.py) parses these and generates XML documents (dreq2Defn.xml, ..)

An XSLT script is then used to generate the schema documents (dreq2.xsd,  ...):

> xsltproc ../../docs/xlst_xdsSchemaGen.xml out/$(targ)Defn.xml > out/$(targ)Schema.xsd 
