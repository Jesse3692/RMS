import unittest

from flask_jwt_extended import create_access_token
from your_application.models import Role, User
from your_flask_app import create_app, db


class AdminAreaTestCase(unittest.TestCase):
    def setUp(self):
        # 创建 Flask 应用和数据库
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db.init_app(self.app)
        
        # 创建一个 admin 用户和一个普通用户
        with self.app.app_context():
            db.create_all()
            admin_role = Role(name='admin')
            normal_role = Role(name='user')
            db.session.add(admin_role)
            db.session.add(normal_role)
            
            admin_user = User(username='admin_user', roles=[admin_role])
            normal_user = User(username='normal_user', roles=[normal_role])
            db.session.add(admin_user)
            db.session.add(normal_user)
            db.session.commit()
            
            # 登录 admin 用户并获取 token
            with self.app.test_client() as client:
                login_response = client.post('/login', json={
                    'username': 'admin_user',
                    'password': 'password'  # 假设密码是 'password'
                })
                self.admin_token = login_response.json['access_token']

    def tearDown(self):
        # 清理数据库
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_admin_area_access(self):
        # 使用 admin 用户的 token 访问 admin 区域
        with self.app.test_client() as client:
            headers = {
                'Authorization': f'Bearer {self.admin_token}'
            }
            response = client.get('/admin', headers=headers)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Welcome Admin!', response.json['message'])

    def test_normal_user_access(self):
        # 使用普通用户尝试访问 admin 区域
        with self.app.test_client() as client:
            headers = {
                'Authorization': f'Bearer {self.admin_token}'  # 这里应该使用普通用户的 token
            }
            response = client.get('/admin', headers=headers)
            self.assertEqual(response.status_code, 403)
            self.assertIn('Insufficient permissions', response.json['message'])

    def test_role_required_decorator(self):
        # 测试 role_required 装饰器
        with self.app.test_client() as client:
            # 获取普通用户的 token
            normal_user_token = create_access_token(identity='normal_user')
            
            headers = {
                'Authorization': f'Bearer {normal_user_token}'
            }
            response = client.get('/admin', headers=headers)
            self.assertEqual(response.status_code, 403)
            self.assertIn('Insufficient permissions', response.json['message'])

if __name__ == '__main__':
    unittest.main()if __name__ == '__main__':
    unittest.main()