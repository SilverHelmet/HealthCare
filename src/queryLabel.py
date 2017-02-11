import urllib
import urllib2

if __name__ == "__main__":
    query = 'SELECT ?p \
WHERE \
{ \
 <http://dbpedia.org/resource/Cerebral_infarction> ?p ?o \
} \
'

    endpoint = "http://162.105.146.246:3093/sparql"
    query = urllib.quote(query)
    url = "%s?query=%s&format=csv" %(endpoint, query)
    # url = urllib.quote(url)
    req = urllib2.Request(url)
    # print req.get_full_url()
    res_data = urllib2.urlopen(req)
    res = res_data.read()
    print res