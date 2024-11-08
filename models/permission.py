from datetime import datetime, timezone

from models import db


class Permission(db.Model):
    __tablename__ = "permissions"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    route = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))  # noqa:E501
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self):
        return f"<Permission {self.name}, {self.route}>"


class RolePermissions(db.Model):
    __tablename__ = "role_permissions"
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), primary_key=True)  # noqa:E501
    permission_id = db.Column(
        db.Integer, db.ForeignKey("permissions.id"), primary_key=True
    )
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))  # noqa:E501
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )


def init_permissions():
    permissions = [
        {
            "name": "view_user_list",
            "description": "查看用户列表",
            "route": "/users/view",
        },
        {"name": "create_user", "description": "创建用户", "route": "/users/create"},
        {"name": "edit_user", "description": "编辑用户", "route": "/users/edit"},
        {
            "name": "toggle_user_status",
            "description": "禁用/启用用户",
            "route": "/users/toggle",
        },
        {
            "name": "assign_role_and_permission",
            "description": "分配角色与权限",
            "route": "/users/assign-role-permission",
        },
        {
            "name": "view_department_structure",
            "description": "查看组织结构",
            "route": "/departments/view",
        },
        {
            "name": "create_department",
            "description": "创建部门",
            "route": "/departments/create",
        },
        {
            "name": "edit_department",
            "description": "编辑部门信息",
            "route": "/departments/edit",
        },
        {
            "name": "delete_department",
            "description": "删除部门",
            "route": "/departments/delete",
        },
        {
            "name": "manage_cross_department_permission",
            "description": "跨部门权限管理",
            "route": "/departments/manage-cross-department",
        },
        {
            "name": "create_role",
            "description": "创建角色",
            "route": "/roles/create",
        },
        {
            "name": "edit_role",
            "description": "编辑角色",
            "route": "/roles/edit",
        },
        {
            "name": "assign_role_permissions",
            "description": "分配角色权限",
            "route": "/roles/assign-permission",
        },
        {
            "name": "delete_role",
            "description": "删除角色",
            "route": "/roles/delete",
        },
        {
            "name": "create_workflow_template",
            "description": "创建流程模板",
            "route": "/workflow/create-template",
        },
        {
            "name": "edit_workflow_template",
            "description": "编辑流程模板",
            "route": "/workflow/edit-template",
        },
        {
            "name": "start_workflow_instance",
            "description": "启动流程实例",
            "route": "/workflow/start-instance",
        },
        {
            "name": "approve",
            "description": "审批权限",
            "route": "/workflow/approve",
        },
        {
            "name": "view_workflow_status",
            "description": "查看流程状态",
            "route": "/workflow/view-status",
        },
        {
            "name": "view_documents",
            "description": "查看文档",
            "route": "/documents/view",
        },
        {
            "name": "upload_documents",
            "description": "上传文档",
            "route": "/documents/upload",
        },
        {
            "name": "edit_documents",
            "description": "编辑文档",
            "route": "/documents/edit",
        },
        {
            "name": "delete_documents",
            "description": "删除文档",
            "route": "/documents/delete",
        },
        {
            "name": "download_documents",
            "description": "下载文档",
            "route": "/documents/download",
        },
        {
            "name": "system_config",
            "description": "系统配置",
            "route": "/settings/system-config",
        },
        {
            "name": "user_log_management",
            "description": "用户日志管理",
            "route": "/settings/user-logs",
        },
        {
            "name": "data_backup_and_restore",
            "description": "数据备份和恢复",
            "route": "/settings/backup-restore",
        },
        {
            "name": "access_control_management",
            "description": "访问控制管理",
            "route": "/settings/access-control",
        },
        {
            "name": "secutity_and_permission_settings",
            "description": "安全与权限设置",
            "route": "/settings/security-permissions",
        },
    ]
    for permission in permissions:
        if not Permission.query.filter_by(
            name=permission["name"], route=permission["route"]
        ).first():
            new_permission = Permission(
                name=permission["name"],
                description=permission["description"],
                route=permission["route"],
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            )
            db.session.add(new_permission)
    db.session.commit()
