import unittest

import redis


class TestRedisConnection(unittest.TestCase):
    def setUp(self):
        # 设置Redis连接参数
        self.host = "localhost"
        self.port = 63799
        self.db = 0
        self.password = "qweasd123"  # 密码
        self.redis_client = None

    def test_connection(self):
        # 尝试连接到Redis服务器
        try:
            self.redis_client = redis.Redis(
                host=self.host, port=self.port, db=self.db, password=self.password
            )
            response = self.redis_client.ping()
            self.assertTrue(response, "Redis连接测试失败，无法成功ping通Redis服务器。")
            print("成功连接到Redis服务器。")
        except redis.ConnectionError as e:
            self.fail(f"连接到Redis服务器失败：{e}")
        except Exception as e:
            self.fail(f"测试过程中发生错误：{e}")

    def tearDown(self):
        # 测试完成后关闭Redis连接
        if self.redis_client:
            self.redis_client.close()


if __name__ == "__main__":
    unittest.main()
