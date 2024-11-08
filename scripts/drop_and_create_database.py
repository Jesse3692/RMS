import pymysql


def create_database(connection, query):
    """创建数据库的函数"""
    with connection.cursor() as cursor:
        cursor.execute(query)
        print("Database created successfully.")


def delete_database(connection, query):
    """删除数据库的函数"""
    with connection.cursor() as cursor:
        cursor.execute(query)
        print("Database deleted successfully.")


def main():
    # 数据库配置信息
    config = {
        "host": "localhost",
        "user": "root",  # 替换为你的 MySQL 用户名
        "password": "123456",  # 替换为你的 MySQL 密码
        "charset": "utf8mb4",
    }

    # 创建数据库的 SQL 语句
    create_db_sql = "CREATE DATABASE IF NOT EXISTS rms CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
    # 删除数据库的 SQL 语句
    delete_db_sql = "DROP DATABASE IF EXISTS rms"

    # 连接到 MySQL 服务器
    connection = pymysql.connect(**config)

    try:
        # 删除数据库
        delete_database(connection, delete_db_sql)
    except pymysql.MySQLError as e:
        print(f"Error deleting database: {e}")

    try:
        # 创建数据库
        create_database(connection, create_db_sql)
    except pymysql.MySQLError as e:
        print(f"Error creating database: {e}")

    # 关闭数据库连接
    connection.close()


if __name__ == "__main__":
    main()
