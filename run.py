from flask import Flask,render_template
from flask_login import UserMixin, LoginManager, login_user, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = "mrsoft"  # 配置通用密钥
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # 是否跟踪数据库的变化
app.config['SQLALCHEMY_DATABASE_URI'] = (
        'mysql+pymysql://root:123456@localhost/house-price'
        ) # 数据库基本配置信息

# 初始化LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

db = SQLAlchemy(app)

# 定义用户加载回调函数
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 用户模型类
class User(db.Model,UserMixin):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(125), nullable=False)
    email = db.Column(db.String(125), nullable=False)
    password = db.Column(db.String(255), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    # 往数据库添加数据
    # with app.app_context():
    #     pwd = generate_password_hash('mrsoft')  # 将密码mrsoft转换为哈希密码
    #     user = User(username='cjy', email='11111111@qq.com', password=pwd)
    #     db.session.add(user)
    #     db.session.commit()
    app.run(debug=True)