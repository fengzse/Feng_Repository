import unittest
import time

from app.models import User, Role, Permission, AnonymousUser
from app import db, create_app


class TestUserModelCase(unittest.TestCase):  # 因为测试的时候不是用户发来请求，没有上下文，因此需要创建一个
    def setUp(self):  # app上下文环境，可以创建出 current_app等用以执行测试方法
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_setter(self):
        u = User(password='cat')
        self.assertTrue(u.password_hash is not None)

    def test_password_getter(self):
        u = User(password='cat')
        with self.assertRaises(AttributeError):
            u.password()

    def test_verification_password(self):
        u = User(password='cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

    def test_hash_random(self):
        u = User(password='cat')
        u2 = User(password='cat')
        self.assertTrue(u.password_hash != u2.password_hash)

    def test_confirmation_valid_token(self):
        u = User(password='cat')
        db.session.add(u)
        db.session.commit()  # 要写入数据库才会生成主键id
        token = u.generate_confirmation_token()
        self.assertTrue(u.confirm(token))

    def test_confirmation_invalid_token(self):
        u = User(password='cat')
        u2 = User(password='dog')
        db.session.add(u)
        db.session.add(u2)
        db.session.commit()
        token = u.generate_confirmation_token()
        self.assertFalse(u2.confirm(token))

    def test_expired_confirmation_token(self):
        u = User(password='cat')
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token(1)
        time.sleep(2)
        self.assertFalse(u.confirm(token))

    def test_reset_token(self):
        u = User(password='cat')
        db.session.add(u)
        db.session.commit()
        token = u.generate_reset_token()
        self.assertTrue(User.reset_password(token, 'dog'))
        self.assertTrue(u.verify_password('dog'))

    def test_invalid_reset_token(self):
        u = User(password='cat')
        db.session.add(u)
        db.session.commit()
        token = u.generate_reset_token()
        self.assertFalse(User.reset_password(token + 'ab', 'dog'))
        self.assertTrue(u.verify_password('cat'))

    def test_role_and_permission(self):
        Role.insert_roles()
        u = User(email='abc@example.com', password='cat')
        self.assertTrue(u.can(Permission.WRITE))
        self.assertFalse(u.can(Permission.ADMIN))

    def test_anonymoususers_permission(self):
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.COMMENT))
