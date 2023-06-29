from models import User, Post, db
from app import app

db.drop_all()
db.create_all()

Post.query.delete()

same = User(first_name='Same',last_name='Chan', image_url = 'https://i.redd.it/bk6dm7terlk51.jpg')
ei = User(first_name = 'Ei',last_name='Kun', image_url= 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi.pinimg.com%2Foriginals%2Fa9%2F34%2F80%2Fa93480e9c44e6acb205ed47c223a19f0.jpg&f=1&nofb=1&ipt=da35a0390ba1f062ca1e58f25a8307c5e3d0f22e3d395cdb95ae5f524b4e76c8&ipo=images')
tako = User(first_name = 'Tako',last_name='Kun', image_url= 'https://cdn.yamibuy.net//item/47d0b40f9a04bd1f3aa79b0f081a954b_750x750.webp')

db.session.add(same)
db.session.add(ei)
db.session.add(tako)

db.session.commit()

samepost = Post(title='I love Jihyo', content = 'I went to concert!', user_id = same.id)
eipost = Post(title='Mobulas are so cool', content = 'They can fly like birds', user_id = ei.id)

db.session.add(samepost)
db.session.add(eipost)

db.session.commit()