from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///user_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserTestCase(TestCase):
    """Tests views for Users"""

    def setUp(self):
        """Add sample user"""
        
        User.query.delete()

        user = User(first_name="Test",last_name="Usertest", image_url= "https://png.pngitem.com/pimgs/s/508-5087236_tab-profile-f-user-icon-white-fill-hd.png")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user = user

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(self.user.first_name, html)

    def test_add_user(self):
        with app.test_client() as client:
            data = {"first_name":"Test2", "last_name": "User2", "image_url": "https://png.pngitem.com/pimgs/s/508-5087236_tab-profile-f-user-icon-white-fill-hd.png"}
            resp = client.post("/users/new", data=data, follow_redirects=True)
            
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<a href="/2">Test2 User2</a>', html)

    def test_delete_user(self):
        with app.test_client() as client:
            resp = self.client.delete(f"/delete/{test_user.id}")
            html = resp.get_data(as_text=True)

            self.asserEqual

    # def test_edit_user(self):
    #     with app.test_client() as client:
    #         test_user = {"id": 5, "first_name":"Test2", "last_name": "User2", "image_url": "https://png.pngitem.com/pimgs/s/508-5087236_tab-profile-f-user-icon-white-fill-hd.png"}
            
    #         resp = client.post(f"/edit/5", data = {
    #             "first_name": "UpdatedTest2", 
    #             "last_name": "UpdatedUser2",
    #             "image_url": "https://i.pinimg.com/originals/92/a4/e5/92a4e59a4c255e455c530f2aa24148d0.jpg"
    #         })

    #         self.assertEqual(resp.status_code,404)
            
    #         updated_user =User.query.get(5)

    #         self.assertEqual(updated_user.first_name, 'UpdatedTest2')
    #         self.assertEqual(updated_user.last_name, 'UpdatedUser2')
    #         self.assetEqual(updated_user.image_url, 'https://i.pinimg.com/originals/92/a4/e5/92a4e59a4c255e455c530f2aa24148d0.jpg')


