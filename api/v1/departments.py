from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required

from models.department import Department
from models import db

# 初始化蓝图
departments_blueprint = Blueprint("departments", __name__)


@departments_blueprint.route("/departments", methods=["POST"])
@jwt_required()
def create_department():
    department_name = request.json.get("name")

    # 检查是否已经存在该部门
    existing_department = Department.query.filter_by(name=department_name).first()
    if existing_department:
        return jsonify(message="Department already exists"), 400

    # 创建部门
    new_department = Department(name=department_name)
    db.session.add(new_department)
    db.session.commit()

    return jsonify(
        message="Department created successfully", department_id=new_department.id
    ), 201


@departments_blueprint.route("/departments", methods=["GET"])
@jwt_required()
def get_departments():
    departments = Department.query.all()
    department_list = [{"id": dept.id, "name": dept.name} for dept in departments]
    return jsonify(departments=department_list), 200


@departments_blueprint.route("/departments/<int:dept_id>", methods=["PUT"])
@jwt_required()
def edit_department(dept_id):
    department = Department.query.get_or_404(dept_id)
    department_name = request.json.get("name", department.name)
    department.name = department_name
    db.session.commit()
    return jsonify(message="Department updated successfully"), 200


@departments_blueprint.route("/departments/<int:dept_id>", methods=["DELETE"])
@jwt_required()
def delete_department(dept_id):
    department = Department.query.get_or_404(dept_id)
    db.session.delete(department)
    db.session.commit()
    return jsonify(message="Department deleted successfully"), 200
