import unittest
import uuid
from uuid import UUID

class TestUrllib2Adapter(unittest.TestCase):

    def setUp(self):
        from Urllib2Adapter import Resource
        self.google = Resource("http://google.com")
        self.localhost = Resource("http://localhost:8080") # replace with RESTservice resource simulation (?) 
        
    def assertContains(self,src,sub):
        if src.find(sub) == -1:
            self.fail(sub+" not found in "+src[:100]+"...")
        
    def test_getInvalid(self):
        self.assertRaises(IOError, self.google.get, "invalidextension")
        
    def test_getNotFound(self):
        res = self.google.get("/",{'q':'something'})
        self.assertEqual(res.status,404)

    def test_get(self):
        res = self.google.get("/")
        self.assertContains(res.decodeBody(),"<html>")
    
    def test_getParams(self):
        res = self.localhost.get("/search.json",{'q':'nodejs'})
        self.assertEqual(res.decodeBody(),"[]")
        
    def test_postInvalid(self):
        res = self.google.post("/",{'q':'helloGoogle'})
        self.assertEqual(res.status,405)
        
    def test_post(self):
        res = self.localhost.post("/user/"+str(uuid.uuid1())+".json",{'source':'restclient'})
        self.assertContains(res.decodeBody(),"OK")
        
class TestHttplib2Adapter(unittest.TestCase):

    def setUp(self):
        from Httplib2Adapter import Resource
        self.google = Resource("http://google.com")
        self.localhost = Resource("http://localhost:8080") # replace with RESTservice resource simulation (?) 
        
    def assertContains(self,src,sub):
        if src.find(sub) == -1:
            self.fail(sub+" not found in "+src[:100]+"...")
        
    def test_getInvalid(self):
        self.assertRaises(IOError, self.google.get, "invalidextension")
        
    def test_getNotFound(self):
        res = self.google.get("/",{'q':'something'})
        self.assertEqual(res.status,404)

    def test_get(self):
        res = self.google.get("/")
        self.assertContains(res.decodeBody(),"<html>")
    
    def test_getParams(self):
        res = self.localhost.get("/search.json",{'q':'nodejs'})
        self.assertEqual(res.decodeBody(),"[]")
        
    def test_postInvalid(self):
        res = self.google.post("/",{'q':'helloGoogle'})
        self.assertEqual(res.status,405)
        
    def test_post(self):
        res = self.localhost.post("/user/"+str(uuid.uuid1())+".json",{'source':'restclient'})
        self.assertContains(res.decodeBody(),"OK")

if __name__ == '__main__':
    unittest.main()