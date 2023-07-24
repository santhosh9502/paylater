from unittest import TestCase, main
import json
import requests

class TestCases(TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    
    def test_new_user(self):

        url = "http://127.0.0.1:8000/newUser"

        payload = json.dumps({
        "name": "satya",
        "email": "satya@gmail.com",
        "balance": 1800
        })
        headers = {
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        
        self.assertEqual(response["status"], "success")
    
    def test_new_merchant(self):
        

        url = "http://127.0.0.1:8000/newMerchant"

        payload = json.dumps({
        "name": "swiggy",
        "email": "swiggy@gmail.com",
        "fee": 3
        })
        headers = {
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        self.assertEqual(response["status"], "success")


    def test_new_transact(self):    
        
        url = "http://127.0.0.1:8000/transact"

        payload = json.dumps({
        "u_id": 5,
        "m_id": 5,
        "amount": 1000
        })
        headers = {
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        self.assertEqual(response["status"], "success")


    def test_new_getmerchant(self):

        url = "http://127.0.0.1:8000/getMerchant/5"

        payload = json.dumps({})
        headers = {
        'Content-Type': 'application/json'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        self.assertEqual(response["status"], "success")

    def test_new_updatefree(self):
        
        url = "http://127.0.0.1:8000/updateFee?mid=4&fee=6"

        payload = ""
        headers = {}

        response = requests.request("POST", url, headers=headers, data=payload)
        self.assertEqual(response["status"], "success")

    def test_new_repay(self):
    
        url = "http://127.0.0.1:8000/repay?name=santhosh&amount=500"

        payload = {}
        headers = {}

        response = requests.request("POST", url, headers=headers, data=payload)
        self.assertEqual(response["status"], "success")

    def test_new_fee(self):
       url = "self.assertEqual(response[\"status\"], \"success\")"

       payload = "{\r\n    \"status\":\"pizahurt\",\r\n    \"data\":\r\n}"
       headers = {
      'Content-Type': 'text/plain'
       }

       response = requests.request("GET", url, headers=headers, data=payload)
       self.assertEqual(response["status"], "success")

    def test_new_dues(self):
        url = "http://127.0.0.1:8000/getMerchant/2"

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)
        self.assertEqual(response["status"], "success")

    def test_new_usersAtlimit(self):
        url = "http://127.0.0.1:8000/getMerchant/3"

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)
        self.assertEqual(response["status"], "success")

    def test_new_totaldues(self):
            url = "http://127.0.0.1:8000/getMerchant/4"

            payload = {}
            headers = {}

            response = requests.request("GET", url, headers=headers, data=payload)
            self.assertEqual(response["status"], "success")







   

   



    

    def test_some_test_Case(self):
        pass
        """
        1. When user limit exceedds should "Return insuffcient funds!" as messasge
        """
    