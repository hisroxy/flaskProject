from flask import Flask,render_template, request, redirect, url_for,flash
from forms import LoginForm,SettingForm
from werkzeug.security import check_password_hash
from flask_login import UserMixin,LoginManager,login_user,logout_user,current_user,login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash


app = Flask(__name__)
app.config["SECRET_KEY"] = "mrsoft"  # 配置通用密钥
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # 是否跟踪数据库的变化
app.config['SQLALCHEMY_DATABASE_URI'] = (
        'mysql+pymysql://root:123456@localhost/house-price'
        ) # 数据库基本配置信息

# 初始化LoginManager
login_manager = LoginManager(app)
#跳转的页面
login_manager.login_view = 'login'
# 登录提示信息
login_manager.login_message = '请先登录！'
#登录提示信息类别
login_manager.login_message_category = 'danger'

# 设置回调函数
@login_manager.user_loader
def load(user_id):
    return User.query.get(int(user_id))

db = SQLAlchemy(app)

# 用户模型类
class User(db.Model,UserMixin):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(125), nullable=False)
    email = db.Column(db.String(125), nullable=False)
    password = db.Column(db.String(255), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    登录
    '''
    if current_user.is_authenticated:  # 判断用户是否登录
        return redirect(url_for('index'))
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if not user:
            flash('邮箱不存在！','danger')
        elif check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page=request.args.get('next')
            if not next_page:
                next_page=url_for('index')
            return redirect(next_page)
        else:
            flash('用户名和密码不匹配！','danger')
    return render_template('login.html',form=form)

@app.route('/logout')
def logout():
    """
    退出登录
    """
    logout_user()
    return redirect(url_for('login'))


@app.route('/change_password',methods=['GET','POST'])
@login_required
def change_password():
    """
    修改密码
    """
    form = SettingForm()
    if form.validate_on_submit():   # 如果是提交操作，则修改密码
        if check_password_hash(current_user.password, form.password.data):
            # 根据当前用户id获取用户信息
            user = User.query.filter_by(id=current_user.id).first()
            # 获取新密码
            new_password = form.new_password.data
            # 对新密码加密
            user.password = generate_password_hash(new_password)
            # 提交到数据库
            db.session.commit()
            # 将成功消息存入闪存
            flash('修改成功', 'success')
            # 保存成功后，跳转到登录页面
            return redirect(url_for('change_password'))
        else:
            # 将失败消息存入闪存
            flash('原始密码错误', 'danger')
    return render_template("change_password.html",form=form)    # 显示修改密码页面

if __name__ == '__main__':
    # 往数据库添加数据
    # with app.app_context():
    #     pwd = generate_password_hash('mrsoft')  # 将密码mrsoft转换为哈希密码
    #     user = User(username='cjy', email='11111111@qq.com', password=pwd)
    #     db.session.add(user)
    #     db.session.commit()
    app.run(debug=True)