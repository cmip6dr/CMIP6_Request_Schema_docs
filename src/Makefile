

targ ?= dreq2
fmt ?= xls
version ?= version
www ?= /var/www/html/dreq
###wwwdata ?= /group_workspaces/jasmin2/cmip6_prep/cmip6_data_request/site
###wwwdata ?= /group_workspaces/jasmin4/cedaproc/mjuckes/site
wwwdata ?= /gws/nopw/j04/cmip6_prep_vol1/cmip6_data_request/site
ddir ?= /data/svn/exarch/CMIP6dreq/trunk
prevVersion ?= 01.00.24


.PHONY: config checkSamp schema checkSchema

build:
	make xsd targ=dreq2
	make xsd targ=dreqSupp

config: out/$(targ)Sample.xml out/$(targ)Defn.xml checkSamp 

configV: out/vocabSample.xml out/vocabDefn.xml checkVSamp 

configu: out/dreqUpdSample.xml out/dreqUpdDefn.xml checkSampU 

out/dreqUpdSample.xml: ../../docs/dreq.txt ptxt.py 
	python ptxt.py -f dreq.txt updsamp

out/dreqUpdDefn.xml: ../../docs/dreq.txt ptxt.py
	python ptxt.py -f dreq.txt upd

out/$(targ)Sample.xml: ../../docs/$(targ).$(fmt) ptxt.py   dreqPy/packageConfig.py
	python ptxt.py -f $(targ).$(fmt) samp

out/$(targ)Defn.xml: ../../docs/$(targ).$(fmt) ptxt.py
	python ptxt.py -f $(targ).$(fmt) defn

out/vocabSample.xml: ../../docs/vocab.txt ptxt.py 
	python ptxt.py -f vocab.txt samp

out/vocabDefn.xml: ../../docs/vocab.txt ptxt.py
	python ptxt.py -f vocab.txt defn

checkVSamp:
	xmllint --noout --schema out/vocabFrameworkSchema.xsd out/vocabDefn.xml

checkSamp:
	xmllint --noout --schema out/vocabFrameworkSchema.xsd out/$(targ)Defn.xml

checkSampU:
	xmllint --noout --schema out/vocabFrameworkSchema.xsd out/dreqUpdDefn.xml

schema: config out/$(targ)Schema.xsd checkSchema

schemaV: configV out/vocabSchema.xsd checkSchemaV

xsd: ../../docs/xlst_xdsSchemaGen.xml config  out/$(targ)Defn.xml
	xsltproc ../../docs/xlst_xdsSchemaGen.xml out/$(targ)Defn.xml > out/$(targ)Schema.xsd

out/vocabSchema.xsd: ../../docs/xlst_xdsSchemaGen.xml configV  out/vocabDefn.xml
	xsltproc ../../docs/xlst_xdsSchemaGen.xml out/vocabDefn.xml > out/vocabSchema.xsd

checkSchema:
	xmllint --noout --schema out/$(targ)Schema.xsd out/$(targ)Sample.xml

checkSchemaV:
	xmllint --noout --schema out/vocabSchema.xsd out/vocabSample.xml

distrib: out/dreq2Defn.xml  out/dreq2Sample.xml  out/dreq2Schema.xsd
	cp  out/dreq2Defn.xml  out/dreq2Sample.xml  out/dreq2Schema.xsd  out/vocabFrameworkSchema.xsd $(ddir)/dreqPy/docs
	cp  out/vocabDefn.xml  out/vocabSample.xml  out/vocabSchema.xsd vocab.xml  $(ddir)/dreqPy/docs
	echo "docs copied to $(ddir)/dreqPy/docs"
	bash seddreq.sh annotated_20150731.xml dreq.xml dreqPy/dreq.py >  $(ddir)/dreqPy/dreq.py
	bash seddreq02.sh "\.\.\/out" "docs" dreqPy/packageConfig.py > $(ddir)/dreqPy/packageConfig.py
	cp htmlTemplates.py dreqPy/scope.py dreqPy/scope_utils.py dreqPy/utilities.py dreqPy/utilP3.py $(ddir)/dreqPy	
	cp dreqPy/utilP2/*.py $(ddir)/dreqPy/utilP2/
	cp dreqPy/dreqCmdl.py dreqPy/makeTables.py dreqPy/vrev.py dreqPy/fgrid.py dreqPy/overviewTabs.py dreqPy/volsum.py dreqPy/__init__.py dreqPy/simpleCheck.py $(ddir)/dreqPy
	cp dreqPy/extensions/collect.py dreqPy/extensions/versions.py dreqPy/extensions/__init__.py $(ddir)/dreqPy/extensions/
	cp dreqPy/misc_utils.py dreqPy/table_utils.py dreqPy/rvgExtraTable.py $(ddir)/dreqPy
	cp vocabDemo.py $(ddir)/dreqPy	
	cp compare.py $(ddir)/	
	cp out/annotated_20150731_chk.xml $(ddir)/dreqPy/docs/dreq.xml
	cp out/annotated_20150731.xml $(ddir)/dreqPy/docs/dreq_lt.xml
	### cp LICENSE README.txt setup.py setup.cfg $(ddir)/
	cp dreqPy/tables/test.xlsx $(ddir)/dreqPy/docs/CMIP6_MIP_tables.xlsx
	cp out/dc1.xsd out/xlink.xsd out/xml.xsd out/pav.xsd $(ddir)/dreqPy/docs/
	cp out/dreqSuppSchema.xsd out/dreqSuppDefn.xml $(ddir)/dreqPy/docs/
	cp out/supplement_20150731.xml $(ddir)/dreqPy/docs/dreqSupp.xml
	cp out/dreqManifest_dist.txt $(ddir)/dreqPy/docs/dreqManifest.txt
	cp out/md5Manifest.txt out/sfheadings.csv $(ddir)/dreqPy/docs/
	cp -r dreqPy/examples $(ddir)/dreqPy/
	cp out/BlockSchema.csv $(ddir)/dreqPy/docs/
	echo "source copied to $(ddir)/dreqPy"

dirs:
	(cd dreqPy; mkdir -p html html/index  html/t  html/u tab2 html/tabs03  html/tt; ln -s ../out )

localHtml:
	cp -r dreqPy/xls/* $(www)/data/tabs02/
	cp -r dreqPy/html/tabs03/* $(www)/tabs03/
	cp dreqPy/data3.js $(www)/data/mipVarsData.js
	cp dreqPy/data3ex.js $(www)/../js/exptData.js
	rsync -r dreqPy/html/u/ $(www)/u/
	cp -r dreqPy/html/t/* $(www)/t/
	cp -r dreqPy/html/index/* $(www)/index/
	cp -r dreqPy/html/index.html $(www)/
	cp dreqPy/tab01_1_1_dn.html dreqPy/tab01_1_1.html dreqPy/tab01_3_3.html $(www)/
	cp websiteExtras/dreq.css $(www)/css

siteDataShift:
	mv $(wwwdata)/latest $(wwwdata)/old
	##[[ $$? != 0 ]] && exit -1;
	##echo MOVED $(wwwdata)/latest to $(wwwdata)/$(prevVersion)
	mv $(wwwdata)/new $(wwwdata)/latest
	##[[ $$? != 0 ]] && exit -1;
	echo MOVED $(wwwdata)/new to $(wwwdata)/latest


createContent:
	cd dreqPy; python overviewTabs.py
	cd dreqPy; python makeTables.py
	cd dreqPy; python dreqCmdl.py --SF

prepNew:
	cd $(wwwdata); rm -fr new
	mkdir $(wwwdata)/new

siteDataNew:
	mkdir new new/data
	mv dreqPy/xls new/data/tabs02
	mv dreqPy/html/tabs03 new/
	mv dreqPy/html/u new/
	mv dreqPy/html/t new/
	cp dreqPy/data3.js new/data/mipVarsData.js
	cp dreqPy/data3ex.js new/data/exptData.js

siteData:
	if [ -e "$(wwwdata)/new" ]; then \
	  echo "Let's rock" >&2; \
	else \
	  echo "Base directory -- $(wwwdata)/new -- does not exist" >&2; \
	  exit 1; \
	fi
	mkdir -p $(wwwdata)/new/data/tabs02/  $(wwwdata)/new/tabs03/ $(wwwdata)/new/u/ $(wwwdata)/new/t/
	rsync -r dreqPy/xls/ $(wwwdata)/new/data/tabs02/
	rsync -r dreqPy/html/tabs03/ $(wwwdata)/new/tabs03/
	rsync -r dreqPy/html/u/ $(wwwdata)/new/u/
	rsync -r dreqPy/html/t/ $(wwwdata)/new/t/
	cp dreqPy/data3.js $(wwwdata)/new/data/mipVarsData.js
	cp dreqPy/data3ex.js $(wwwdata)/new/data/exptData.js

siteDataV2:
	cp dreqPy/tab01_1_1_dn.html dreqPy/tab01_1_1.html dreqPy/tab01_3_3.html $(wwwdata)/new/
	cp -r dreqPy/html/index $(wwwdata)/new/
	cp -r dreqPy/html/index.html $(wwwdata)/new/

betaHtml:
	mkdir -p $(www)/beta/ $(www)/beta/css/ $(www)/beta/index/
	(cd $(www)/beta; ln -s $(wwwdata)/new/data ; ln -s $(wwwdata)/new/tabs03 ;  ln -s $(wwwdata)/new/u ; ln -s $(wwwdata)/new/t)
	cp dreqPy/tab01_1_1_dn.html dreqPy/tab01_1_1.html dreqPy/tab01_3_3.html $(www)/beta/
	cp websiteExtras/dreq.css $(www)/beta/css/
	cp -r dreqPy/html/index/* $(www)/beta/index/
	cp -r dreqPy/html/index.html $(www)/beta/

betaHtmlV2:
	mkdir -p $(www)/beta/ $(www)/beta/css/ $(www)/beta/index/
	(cd $(www)/beta; ln -s $(wwwdata)/new/data ; ln -s $(wwwdata)/new/tabs03 ;  ln -s $(wwwdata)/new/u ; ln -s $(wwwdata)/new/t)
	(cd $(wwwdata)/new/; cp tab01_1_1_dn.html tab01_1_1.html tab01_3_3.html $(www)/beta/)
	cp websiteExtras/dreq.css $(www)/beta/css/
	cp -r $(wwwdata)/new/index/* $(www)/beta/index/
	cp -r $(wwwdata)/new/index.html $(www)/beta/

siteHtml:
	cp dreqPy/tab01_1_1_dn.html dreqPy/tab01_1_1.html dreqPy/tab01_3_3.html $(www)/
	mkdir -p $(www)/css; mkdir -p $(www)/index/
	cp websiteExtras/dreq.css $(www)/css
	cp -r dreqPy/html/index/* $(www)/index/
	cp -r dreqPy/html/index.html $(www)/

versionHtml:
	mkdir $(www)/$(version)  $(www)/$(version)/index $(www)/$(version)/css
	cp $(www)/tab01_1_1_dn.html dreqPy/tab01_1_1.html dreqPy/tab01_3_3.html $(www)/$(version)
	cp  $(www)/css/dreq.css  $(www)/$(version)/css/
	cp $(www)/index/* $(www)/$(version)/index/
	cp $(www)/index.html $(www)/experiments.html $(www)/mipVars.html  $(www)/$(version)

versionLinks:
	(cd $(www)/$(version); ln -s $(wwwdata)/$(version)/data)
	(cd $(www)/$(version); ln -s $(wwwdata)/$(version)/tabs03)
	(cd $(www)/$(version); ln -s $(wwwdata)/$(version)/u)
	(cd $(www)/$(version); ln -s $(wwwdata)/$(version)/t)

cleanLocalHtml:
	cp -r dreqPy/xls/* $(www)/data/tabs02/
	cp -r dreqPy/html/tabs03/* $(www)/tabs03/
	cp dreqPy/tab01_1_1.html dreqPy/tab01_3_3.html $(www)/
	cp dreqPy/data3.js $(www)/data/mipVarsData.js
	cp websiteExtras/dreq.css $(www)/css
	mv $(www)/u/ $(www)/u1
	cp -r dreqPy/html/u $(www)/
	mv $(www)/t/ $(www)/t1
	cp -r dreqPy/html/t $(www)/
	cp -r dreqPy/html/index/* $(www)/index/
	cp -r dreqPy/html/index.html $(www)/
	echo clearing up ... may take some time
	find  $(www)/u1 -name "*.html" -exec rm {} \;
	find  $(www)/t1 -name "*.html" -exec rm {} \;
	rmdir $(www)/u1
	rmdir $(www)/t1

cleanHtml:
	find dreqPy/html/u -type f -exec rm {} \;
	rm dreqPy/html/t/* dreqPy/html/tt/*
	find /var/www/f/u -type f -exec rm {} \;
	rm /var/www/f/t/* 

sHtml:
	zip -r html.zip data2.js html 

