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

    def test(self):
        self._gettoken()
        self._testview()
