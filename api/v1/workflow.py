from flask import blueprints, jsonify

from tools import check_permission

workflow_blueprint = blueprints.Blueprint("workflow", __name__)


@workflow_blueprint.route("/template/create", methods=["POST"])
@check_permission("CREATE_WORKFLOW_TEMPLATE")
def create_workflow_template():
    # 逻辑：创建流程模板
    return jsonify({"message": "Workflow template created successfully"})


@workflow_blueprint.route("/template/edit/<int:id>", methods=["PUT"])
@check_permission("EDIT_WORKFLOW_TEMPLATE")
def edit_workflow_template(id):
    # 逻辑：编辑流程模板
    return jsonify({"message": f"Workflow template {id} edited successfully"})


@workflow_blueprint.route("/instance/start", methods=["POST"])
@check_permission("START_WORKFLOW_INSTANCE")
def start_workflow_instance():
    # 逻辑：启动流程实例
    return jsonify({"message": "Workflow instance started successfully"})


@workflow_blueprint.route("/approve", methods=["POST"])
@check_permission("APPROVE")
def approve_workflow():
    # 逻辑：审批
    return jsonify({"message": "Workflow approved"})


@workflow_blueprint.route("/status/view", methods=["GET"])
@check_permission("VIEW_WORKFLOW_STATUS")
def view_workflow_status():
    # 逻辑：查看流程状态
    return jsonify({"status": "Workflow status information"})
