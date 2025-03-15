provider "aws" {
  region = "us-west-2"
}

resource "aws_ecs_cluster" "fraud_detection_cluster" {
  name = "fraud-detection-cluster"
}

resource "aws_ecs_task_definition" "fraud_detection_task" {
  family                = "fraud-detection-task"
  execution_role_arn    = "arn:aws:iam::aws_account_id:role/ecsTaskExecutionRole"
  container_definitions = <<DEFINITION
[
  {
    "name": "fraud-detection-container",
    "image": "dockerhub_user/fraud-detection-app:latest",
    "memory": 512,
    "cpu": 256,
    "essential": true
  }
]
DEFINITION
}

resource "aws_ecs_service" "fraud_detection_service" {
  name            = "fraud-detection-service"
  cluster         = aws_ecs_cluster.fraud_detection_cluster.id
  task_definition = aws_ecs_task_definition.fraud_detection_task.arn
  desired_count   = 1
  launch_type     = "FARGATE"
}
