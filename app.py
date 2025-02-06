import os
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

# .env ファイルから環境変数を読み込む
load_dotenv()
app = Flask(__name__)

# PostgreSQL データベースの設定
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#print("DB_HOST:", os.getenv("DB_HOST"))
#print("DB_USERNAME:", os.getenv("DB_USERNAME"))
#print("DB_PASSWORD:", os.getenv("DB_PASSWORD"))
#print("DB_NAME:", os.getenv("DB_NAME"))

# SQLAlchemy オブジェクトの初期化
db = SQLAlchemy(app)

# サンプルモデルの定義（テーブル名を 'users' に変更）
class Memberdb(db.Model):
    __tablename__ = '会員' # テーブル名を明示的に 'users' と指定
    会員id = db.Column(db.String(12), primary_key=True)
    氏名 = db.Column(db.String(80), unique=True, nullable=False)
    住所 = db.Column(db.String(80), unique=True, nullable=False)
    電話番号 = db.Column(db.String(13), unique=True, nullable=False)
    生年月日 = db.Column(db.Date, unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

class Goodsdb(db.Model):
    __tablename__ = '商品' # テーブル名を明示的に 'users' と指定
    商品id = db.Column(db.String(13), primary_key=True)
    タイトル = db.Column(db.String(80), unique=True, nullable=False)
    ジャンル = db.Column(db.String(40), unique=True, nullable=False)
    発売日 = db.Column(db.Date, unique=True, nullable=False)
    貸出・返却日 = db.Column(db.Date, unique=True, nullable=False)
    貸出会員 = db.Column(db.String(12), unique=True, nullable=False)
    貸出状況 = db.Column(db.Integer, unique=True, nullable=False)
    貸出回数 = db.Column(db.Integer, unique=True, nullable=False)
    保管場所 = db.Column(db.Integer, unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

@app.route('/')
def index():
    try:
        member = Memberdb.query.all()
        goods = Goodsdb.query.all()

        member_data = [{'memberid': m.会員id, 'name': m.氏名, 'address': m.住所, 'phone': m.電話番号, 'birthday': m.生年月日} for m in member]
        goods_data = [{'goodsid': g.商品id, 'title': g.タイトル, 'genre': g.ジャンル, 'release': g.発売日, 'lend_ret_day': g.貸出・返却日, 'lend_member': g.貸出会員, 'lend_status': g.貸出状況, 'number_of_lend': g.貸出回数, 'storage_location': g.保管場所} for g in goods]

        return jsonify({'members': member_data, 'goods': goods_data})
        print("Template path:",app.jinja_loader.get_source(app.jinja_env, 'index.html'))


    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
