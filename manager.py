from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from zhiliaoqa import app
from exts import db
# 导入自定义的用户模型
from models import User, Question, Answer


manager = Manager(app)

# 要使用flask_migrate，必须绑定app和db
# 使用Migrate绑定app和db
migrate = Migrate(app, db)

# 添加迁移脚本的命令到manager中
# MigrateCommand 会将上面导入的模型映射到数据库中
manager.add_command('db', MigrateCommand)


if __name__ == "__main__":
    manager.run()
