import requests
import os 
import logging
import datetime 




class Service:
    def __init__(self,login,password):
        self.login = login
        self.password = password
        self.token = ""
        self.service_id = ""
        logging.basicConfig(filename=self.login, format='%(asctime)s - %(message)s', level=logging.INFO)
        

    def get_service_id(self):
        headers = {"Accept":"application/json", "Authorization":self.token}
        url = "https://integration.iboxapp.az/api/v1/services"
        post = requests.get(url,headers=headers)
        data = post.json()
        service_uuid = data['data'][0]
        self.service_id = service_uuid['service_uuid']
        return data
    

    def auth(self):
        headers = {"Accept":"application/json"}
        url = "https://integration.iboxapp.az/api/v1/auth"
        data = {"email":self.login,
                "password": self.password}
        post = requests.post(url,headers=headers, json=data)
        data = post.json()
        self.token = "Bearer {}".format(data['data'])
        service_id = self.get_service_id()
        logging.info("Login" + post.text)
        return data


    def bulk_create(self,path):
        self.auth()
        myfile = open(path)
        headers = {"Accept":"application/json", "Authorization":self.token}
        url = "https://integration.iboxapp.az/api/v1/services/bulkImport/create/{}".format(self.service_id)
        post = requests.post(url,files={"file":myfile},headers=headers)
        logging.info("bulk create" + post.text)
        return post
    
    def bulk_update(self,path):
        self.auth()
        myfile = open(path)
        headers = {"Accept":"application/json", "Authorization":self.token}
        url = "https://integration.iboxapp.az/api/v1/services/bulkImport/update/{}".format(self.service_id)
        post = requests.post(url,files={"file":myfile},headers=headers)
        logging.info("bulk update" + post.text)
        return post.json()
        

    def get_all_operations(self):
        self.auth()
        url = "https://integration.iboxapp.az/api/v1/operations"
        headers = {"Accept":"application/json", "Authorization":self.token}
        post = requests.get(url,headers=headers)
        logging.info({"All operations": post.json()})
        return post.json()


    def get_operation(self,id_operations):
        self.auth()
        headers = {"Accept":"application/json", "Authorization":self.token}
        url = "https://integration.iboxapp.az/api/v1/operation/{}".format(self.service_id)
        post = requests.get(url,headers=headers)
        logging.info(post.content)
        return post.json()







