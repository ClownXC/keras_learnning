from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test import Client


# Create your tests here.

# def setUp(self):
#     print("初始化逻辑...")
#     User = get_user_model()
#     User.objects.create_user(
#         username=self.username,
#         password=self.password
#     ).save()
#
#
# # def test_testview(self):
# #     path = "/test/"
# #     res = Client().get(path=path)
# #     # print(res.status_code)
# #     self.assertEqual(res.status_code, 200)
# #     self.assertEqual(res.data['detail'], 'test')
#
# def test_gettoken(self):
#     path = "/api/token/"
#     res = Client().post(
#         path=path,
#         data={
#             'username': self.username,
#             'password': self.password
#         },
#         content_type="application/json"
#     )
#     print(res)
#     # self.assertEqual(res.status_code, 200)
#     token = res.data['access']
#     print(token)
#     # self.assertNotEqual(token, None)
#     self.token = token


class BaseTest(TestCase):
    username = "chen"
    password = 3494269

    def setUp(self):
        """
        :return:
        """
        print('初始化逻辑')
        User = get_user_model()
        User.objects.create_user(
            username=self.username,
            password=self.password
        ).save()

    def _testview(self):
        """
        :return:
        """
        path = '/test/'
        res = Client().get(path=path, HTTP_AUTHORIZATION="Bearer  " + self.token)
        print(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['detail'], 'test')

    def _gettoken(self):
        """
        :return:
        """
        path = "/api/token/"
        res = Client().post(
            path=path,
            data={
                'username': self.username,
                'password': self.password
            },
            content_type="application/json"
        )
        self.assertEqual(res.status_code, 200)
        token = res.data['access']
        self.assertNotEqual(token, None)
        self.token = token

    def _k8s_apiserver(self):
        """
        测试集成 k8s
        :return:
        """
        from kubernetes import client
        host = "https://k8s-master:6443"
        with open("./k8s_config/token", "r") as f:
            token = f.read()

        ssl_ca_cert = "./k8s_config/ca.crt"
        configuration = client.Configuration()
        configuration.host = host
        configuration.api_key = {
            'authorization': "Bearer " + token
        }
        configuration.ssl_ca_cert = ssl_ca_cert
        configuration.verify_ssl = True
        client.Configuration.set_default(configuration)
        v1 = client.CoreV1Api()
        print("Listing pods with their IPs: ")
        ret = v1.list_pod_for_all_namespaces(watch=False)
        for i in ret.items:
            print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))

    def test(self):
        # self._gettoken()
        # self._testview()
        self._k8s_apiserver()
