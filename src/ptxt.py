''' Generate vocabulary definition document and sample vocabulary document.
USAGE
.....
ptxt.py [-f srcFile] [samp|defn]


NB:
Schema namespace implemented partially -- need to work through for update and vocabs. 
'''
import re, collections, sys, uuid, utils_wb
import time, datetime, xlrd, codecs
from utils_wb import uniCleanFunc

sys.path.append('dreqPy' )
import packageConfig

t = time.gmtime()
d = datetime.date(t.tm_year, t.tm_mon, t.tm_mday)

version = packageConfig.__version__

##
## for definitions of dublin core elements see:
## see http://dublincore.org/documents/usageguide/elements.shtml
##
samplePrologue="""<prologue>
<dc:title>Draft CMIP6 Data Request [%s]</dc:title>
<dc:description>The CMIP6 Data Request will specify the variables requested for the CMIP6 archive, and the detail the experiments and time slices for which they are required.</dc:description>
<dc:creator>Martin Juckes</dc:creator>
<dc:date>%s</dc:date>
<dc:source>CF Standard Name table; CMIP6 Controlled Vocabularies; ESDOC CMIP6 Experiment Documentation</dc:source>
<pav:version>%s</pav:version>
</prologue>
""" %  (version,d.isoformat(),version )

samplePrologueVocab="""<prologue>
<dc:title>Draft CMIP6 Vocabularies [%s]</dc:title>
<dc:description>The CMIP6 Vocabularies will specify the controlled vocabularies for the CMIP6 archive.</dc:description>
<dc:creator>Martin Juckes</dc:creator>
<dc:date>%s</dc:date>
<pav:version>%s</pav:version>
</prologue>
""" %  (version,d.isoformat(), version )

re_it = re.compile( '{(.*)}' )
re_is = re.compile( '\[(.*)\]' )
re_atdef = re.compile( '^(?P<n>\S+)\s*(((?P<b>\[.*?])|(?P<a>\{.*?\})|(?P<c>\<.*?\>))\s*){0,3}$' )
re_atdef = re.compile( '^(?P<n>\S+)\s*((\[(?P<b>.*?)\]|\{(?P<a>.*?)\}|\<(?P<c>.*?)\>|desc:(?P<desc>.*?)::)\s*){0,3}$' )

### tuble to define attributes of an item
nt__itematt = collections.namedtuple( 'itematt', ['name','type','title','clss','techn','uid','description','superclass','usage','required'] )

vocab_elTmpl = '''<%(elementname)s label="%(label)s" uid="%(uid)s" title="%(title)s" id="%(id)s" itemLabelMode="%(ilm)s" level="%(sectLevel)s" maxOccurs="%(mxo)s" labUnique="%(labu)s" description="%(desc)s">
%(itemAttrList)s
</%(elementname)s>
'''
ial_elTmpl = '  <rowAttribute label="%(label)s"%(wrappedType)s%(wrappedTitle)s%(wrappedClass)s%(wrappedTechn)s%(wrappedDescription)s%(wrappedUid)s%(wrappedSuperclass)s%(wrappedUsage)s%(wrappedReq)s/>'

expl_Tmpl = '''<%(label)s label="%(label)s" uid="%(uid)s" useClass="vocab" title="%(title)s" id="%(id)s">
<!-- <info srcType="dummy" srcRef="ptxt.py">Dummy entries</info> -->
%(exampleItem)s
</%(label)s>
'''
item_Tmpl = '<item id="%(id)s" label="%(label)s" title="%(title)s"%(extras)s/>'

def wrap( x,y):
  if y == None:
    return ''
  else:
    return x % y

class vocab(object):

  def __init__( self, line, kk=0, counter=None ):
     if type(line) in [type(''),type(u'')]:
       bits = [x.strip() for x in line.split( ';' )]
       assert len (bits) in [7,8], '[1] Cannot parse %s' % line
       assert bits[0][:5] == 'vocab', '[2] Cannot parse %s' % line
       self.label = bits[0].split( ' ')[1]
       self.title = bits[1]
       self.id = 'cmip.drv.%3.3i' % kk
       self.ilt = bits[3]
       self.level = int(bits[4] )
       self.kk = kk
       self.labu = bits[6]
       self.mxo = int(bits[5])
       self.description = '%s [%s]' % (self.title, self.label)
     else:
       self.label,self.title , self.id, self.ilt, self.level, self.kk, self.labu, self.mxo = tuple( line[1:9] )
       if len(line) == 10:
         self.description = line[9]
       else:
         self.description = ''
       self.level = int( self.level )
       self.mxo = int( self.mxo )
     self.header = (self.label,self.title , self.id, self.ilt, self.level, self.kk, self.labu, self.mxo )
     self.msg( '[%s] %s {%s:%s}' % (self.label, self.title, self.id, self.ilt) )
###nt__itematt = collections.namedtuple( 'itematt', ['name','type','title','clss','techn'] )
###nt__itematt = collections.namedtuple( 'itematt', ['name','type','title','clss','techn','uid','description','superclass','usage','required'] )
     self.itematts = [  nt__itematt( 'label','xs:string','Record Label',None,None,None,'Mnemonic label for record',None,None,True ),
                        nt__itematt( 'title','xs:string','Record Title',None,None,None,'Title of record',None,None,True ) ]
     self.counter = counter

  def tmpl(self,oo=None,mode="defn",cls='vocab'):
     """Write out a section definition or a sample record"""
     if mode in [ "defn","upd"]:
       ss = []
       for i in self.itematts:
         if i.title in ['',None]:
           print( 'ERROR.tmpl.0001: empty title in: ',i.name,self.label )
         if i.name in ['',None]:
           print( 'ERROR.tmpl.0002: empty label in: ',i.name,self.label )
         wrappedClass = wrap( ' useClass="%s"' , i.clss )
         wrappedTechn = wrap( ' techNote="%s"' , i.techn )
         wrappedTitle = wrap( ' title="%s"' , i.title )
         if i.name == 'uid':
           wrappedType = ' type="aa:st__uid"'
         else:
           wrappedType = wrap( ' type="%s"' , i.type )
         ##wrappedReq = wrap( ' required="%s"' , i.required )
         if i.required != '':
           wrappedReq = wrap( ' required="%s"' , i.required )
         else:
           wrappedReq = ' required="true"'

         if i.usage != '':
           wrappedUsage = wrap( ' usage="%s"' , i.usage )
         else:
           wrappedUsage = ''
         if i.uid in [None,'']:
           ##wrappedUid = wrap( ' uid="%s"' , str( uuid.uuid1() ) )
           wrappedUid = wrap( ' uid="%s"' , 'ATTRIBUTE::%s.%s' % (self.label,i.name) )
         else:
           wrappedUid = wrap( ' uid="%s"' , i.uid )

         wrappedDescription = wrap( ' description="%s"' , i.description )
         wrappedSuperclass = wrap( ' superclass="%s"' , i.superclass )

         label = i.name
         ss.append(ial_elTmpl % locals())
       sss = '\n'.join( ss )

       if mode in [ 'upd','updsamp']:
         label = '%sUpd' % self.label
       else:
         label = self.label
       title = self.title
       id = self.id
       ilm =  self.ilt
       sectLevel =  self.level
       itemAttrList = sss
       mxo = self.mxo
       labu = self.labu
       desc = self.description
       uid = "SECTION:%s" % label
       elementname = 'table'
       if cls != 'vocab':
         elementname = 'annextable'
         label = label[1:]
         id = id[1:]
       if self.mxo > 1:
         uid += '.xx'
       self.vocab = vocab_elTmpl % locals()
     else:
## construct sample item ##
       if self.ilt == 'an':
         label = 'example01'
       elif self.ilt == 'def':
         label = 'example-01'
       elif self.ilt == 'int':
         label = '1'
       elif self.ilt == 'und':
         label = 'example_03'
       title = 'dummy title string'

       extras = ''
       for i in self.itematts:
         if i.name not in ['label','title']:
           value = "noType"
           if i.type == "xs:string":
             if i.name == 'uid':
               value = str( uuid.uuid1() )
             else:
               value = 'dummyAt'
           elif i.type == "xs:integer":
             value = '25'
           elif i.type in ["aa:st__integerList","aa:st__integerListMonInc"]:
             value = '25 30'
           elif i.type in ["aa:st__stringList"]:
             value = 'alpha beta'
           elif i.type == "aa:st__floatList":
             value = '5. 10.'
           elif i.type == "aa:st__fortranType":
             value = 'integer'
           elif i.type == "aa:st__sliceType":
             value = 'yearList'
           elif i.type == "aa:st__configurationType":
             value = 'size'
           elif i.type == "xs:float":
             value = '5.'
           elif i.type == "xs:boolean":
             value = 'false'
           elif i.type == "xs:duration":
             value = 'P1Y'

           extras += ' %s="%s"' % (i.name,value)
       id = '001.%3.3i.%3.3i' % (self.kk,1)
       exampleItem = item_Tmpl % locals()
       label = self.label
       title = self.title
       id = self.id
       if cls != 'vocab':
         label = label[1:]
         id = id[1:]
       ilm =  self.ilt
       uid = "SECTION:%s" % label
       self.counter[label] += 1
       if self.mxo > 1:
         uid += '.%2.2i' % self.counter[label]
       self.vocab = expl_Tmpl % locals()
##
## print and write if needed
##
     if oo != None:
       try:
         oo.write( uniCleanFunc( self.vocab ) )
       except:
         print( 'Failed to write ...' )
         print( self.vocab )
         raise
     self.msg( vocab )

  def msg(self,txt):
     swallow=True
     if swallow:
       return
     print( text )

  def attr02(self,line):
         self.itematts.append( nt__itematt._make( line ) )
         self.msg( '%s, %s, %s, %s, %s' % (line[0], line[1], line[2], line[3], line[4]) )

  def attr(self,line):
     bits = [x.strip() for x in line[3:].split(';' ) ]
     for b in bits:
       if b.strip() != '':
         bn = b.split(' ')[0]
         x = self.pb(b)
##nt__itematt = collections.namedtuple( 'itematt', ['name','type','title','clss','techn','uid','description','superclass','usage','required'] )
         self.itematts.append( nt__itematt( bn, x[0], x[1], x[2], x[3], None,x[4], None, None, 'True' ) )
         self.msg( '%s, %s, %s, %s, %s' % (bn, x[0], x[1], x[2], x[3]) )

  def pb(self, b):
    x = re_it.findall(b)
    m = re_atdef.match( b )
    if m == None:
         print( 'COULD NOT SCAN: ',b )
         assert False
    else:
      ee = m.groupdict()
      for k in ['a','b','c','desc']:
        if type( ee[k] ) == type( 'x' ):
          assert ee[k].find( '"' ) == -1, 'unable to deal with quote in string: %s' % ee[k]
      itemTitle = ee['a']
      itemType = ee['b']
      itemClass = ee['c']
      itemDescription = ee['desc']
      itemTechNote = None
      if itemType == None:
         itemType = 'xs:string'
      if type(itemClass) == type('x'):
        if itemClass.find( '|' ) != -1:
          bits =  itemClass.split( '|' )
          assert len(bits) == 2, 'ERROR.001.0001: failed to parse attribute definition: %s' % b
          itemClass = bits[0]
          itemTechNote = bits[1]
        
    return [itemType, itemTitle,itemClass,itemTechNote, itemDescription] 

class main(object):

  def __init__(self,fn,mode):
    if fn[-4:] == '.xls':
      oo = codecs.open( '/tmp/ptxt_records.txt', 'wb', encoding='ascii' )
      brec = []
      imode = 0
      ii = []
      self.isect = {}
      wb = utils_wb.workbook( '../../docs/%s' % fn )
      s0 = wb.book.sheet_by_name( 'SECTIONS' )
      ks = []
      for j in range(1,s0.nrows):
        rr = [x.value for x in s0.row(j) ]
        self.isect[str(rr[0]) ] = rr
        ks.append( str(rr[0]) )
      for k in ks:
        if k[0:2] != '__':
          if k[0] == '_':
            ii.append( ['annexVocab',] + self.isect[k] )
          else:
            ii.append( ['vocab',] + self.isect[k] )
          s = wb.book.sheet_by_name( k )
          for j in range(1,s.nrows):
            rr = [x.value for x in  s.row(j) ]
            rr[6] = uniCleanFunc( rr[6] )
            try:
              for x in rr:
                oo.write( x )
                oo.write( '\t' )
              oo.write( '\n' )
            except:
              brec.append((k,rr))
            ii.append(rr)
         
      oo.close()
      if len(brec) > 0:
        print( 'Un-printable records found in ../../docs/%s' % fn )
        for b in brec:
          print( brec )
        assert False, 'FATAL ERROR'
    else: 
      imode = 1
      ii = []
      for l in open('../../docs/%s' % fn).readlines():
        if l[0] != '#':
          ii.append(l)
    kk= 0
    this = None
    fstem =  fn.split( '.' )[0]
    fns = {'defn':'%sDefn' % fstem, 'samp':'%sSample' % fstem, 'upd':'%sUpdDefn' % fstem, 'updsamp':'%sUpdSampl' % fstem }
    fn = fns[mode]
    oo = open( 'out/%s.xml' % fn, 'w' )
    if mode in [ 'samp','updsamp']:
      mainEl = "document"
      mainElCont = '''
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:noNamespaceSchemaLocation="out/dreqSchema.xsd"
xmlns:dc="http://purl.org/dc/elements/1.1/"
xmlns:pav="http://purl.org/pav/2.3"
xmlns="urn:w3id.org:cmip6.dreq.dreq:a"'''
    else:
      mainEl = "defDoc"
      mainElCont = ''' 
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xmlns="urn:w3id.org:cmip6.dreq.framework:a"
xsi:schemaLocation="http://w3id.org/cmip6dr/ns vocabFrameworkSchema_v01beta.xsd"'''

    oo.write( '''<?xml version="1.0" ?>
<%s%s>\n''' % (mainEl,mainElCont) )
    updExtra = ''' - srcid {Record to be copied/modified} <internalLink>
 - updClass {Class of update: copy|change|delete|new}
 - updComment {Comment on the proposed change}
 - updDate {Date of update}
 - updProv {Proposer of update}'''

##    if l[:5] == 'vocab':
      ##prolo = samplePrologueVocab
    ##else:
      ##prolo = samplePrologue

    if mode in [ 'samp','updsamp']:
      oo.write( '%s<main>\n' % samplePrologue )
    annex = False
    counter = collections.defaultdict(int)
    self.sections = {}
    for l in ii:
      if (imode == 1 and l[:5] == 'vocab') or (imode == 0 and l[0] in ['vocab','annexVocab']):
        if this != None:
          this.tmpl(oo=oo,mode=mode,cls=cls)
          self.sections[this.label] = (this.header, this.itematts)
        if imode == 0:
          cls = l[0]
        else:
          cls = l[:5]
        if cls == 'annexVocab':
          if not annex:
             if mode in [ 'samp','updsamp']:
                 oo.write( '</main><annex>\n' )
          annex = True
        kk+=1
        this = vocab(l,kk=kk,counter=counter)
        if mode in ['upd','updsamp']:
          for l1 in updExtra.split( '\n' ):
            this.attr( l1 )
      else:
        if imode == 1:
          this.attr( l)
        else:
          while len(l) < 10:
            l.append( '' )
          this.attr02( l)

    this.tmpl(oo=oo,mode=mode,cls=cls)
    self.sections[this.label] = (this.header, this.itematts)
    if mode in [ 'samp','updsamp']:
      if annex:
        oo.write( '</annex>\n' )
      else:
        oo.write( '</main>\n' )
    oo.write( '</%s>\n' % mainEl )
    oo.close()

if __name__ == "__main__":
  if len(sys.argv) == 1:
    print( __doc__ )
    exit()

  args = sys.argv[1:]
  if args[0] == '-f':
    srcFn = args[1]
    args = args[2:]
  elif args[0] == '-v':
    srcFn = 'vocab.txt'
    args = args[1:]
  else:
    srcFn = 'dreq.txt'
  
  mode = args[0]

  assert mode in ["defn", "samp","upd","updsamp"]

  print( '###### srcFn : ',srcFn )
  m = main(srcFn,mode)
