# 使用 flask shell

```sh
flask run  # 启动 flask 应用
flask shell  # 启动 flask shell
```

查询模型中的数据

```python
from models.permission import Permission
permissions = Permission.query.all()
for permission in permissions:
    print(permission.name)
```
