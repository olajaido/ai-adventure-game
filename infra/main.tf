terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# DynamoDB Table
resource "aws_dynamodb_table" "game_data" {
  name         = "${var.project_name}-game-data"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "userId"
  range_key    = "gameId"

  attribute {
    name = "userId"
    type = "S"
  }

  attribute {
    name = "gameId"
    type = "S"
  }

  tags = {
    Environment = var.environment
    Project     = var.project_name
  }
}

# S3 Bucket for game assets
resource "aws_s3_bucket" "game_assets" {
  bucket = "${var.project_name}-game-assets-${var.environment}"

  tags = {
    Environment = var.environment
    Project     = var.project_name
  }
}

# S3 Bucket versioning
resource "aws_s3_bucket_versioning" "game_assets" {
  bucket = aws_s3_bucket.game_assets.id
  versioning_configuration {
    status = "Enabled"
  }
}

# S3 Bucket encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "game_assets" {
  bucket = aws_s3_bucket.game_assets.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "game_assets" {
  bucket = aws_s3_bucket.game_assets.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Cognito User Pool
resource "aws_cognito_user_pool" "game_users" {
  name = "${var.project_name}-users-${var.environment}"

  password_policy {
    minimum_length    = 8
    require_lowercase = true
    require_numbers   = true
    require_symbols   = true
    require_uppercase = true
  }

  username_attributes      = ["email"]
  auto_verified_attributes = ["email"]

  verification_message_template {
    default_email_option = "CONFIRM_WITH_CODE"
    email_subject        = "Your verification code"
    email_message        = "Your verification code is {####}"
  }

  tags = {
    Environment = var.environment
    Project     = var.project_name
  }
}

# Cognito User Pool Client
resource "aws_cognito_user_pool_client" "game_client" {
  name         = "${var.project_name}-client-${var.environment}"
  user_pool_id = aws_cognito_user_pool.game_users.id

  generate_secret = false
  explicit_auth_flows = [
    "ALLOW_USER_PASSWORD_AUTH",
    "ALLOW_USER_SRP_AUTH",
    "ALLOW_REFRESH_TOKEN_AUTH"
  ]
}

# IAM role for Lambda functions
resource "aws_iam_role" "lambda_role" {
  name = "${var.project_name}-lambda-role-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# IAM policy for Lambda role
resource "aws_iam_role_policy" "lambda_policy" {
  name = "${var.project_name}-lambda-policy-${var.environment}"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem",
          "dynamodb:Query",
          "dynamodb:Scan"
        ]
        Resource = [aws_dynamodb_table.game_data.arn]
      },
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.game_assets.arn,
          "${aws_s3_bucket.game_assets.arn}/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "bedrock:InvokeModel"
        ]
        Resource = ["*"]
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = ["arn:aws:logs:*:*:*"]
      }
    ]
  })
}

# Lambda Function
resource "aws_lambda_function" "game_logic" {
  filename      = data.archive_file.lambda_zip.output_path
  function_name = "${var.project_name}-game-logic-${var.environment}"
  role          = aws_iam_role.lambda_role.arn
  handler       = "lambda_handler.handle_game_action"
  runtime       = "python3.9"
  timeout       = 30
  memory_size   = 256

  environment {
    variables = {
      GAME_TABLE = aws_dynamodb_table.game_data.name
    }
  }
}

# Lambda ZIP file
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/bedrock-code"
  output_path = "${path.module}/lambda.zip"
}

# CloudWatch Log Group
resource "aws_cloudwatch_log_group" "lambda_logs" {
  name              = "/aws/lambda/${var.project_name}-game-logic-${var.environment}"
  retention_in_days = 14
}

# Outputs
output "lambda_function_name" {
  value = aws_lambda_function.game_logic.function_name
}

output "cognito_user_pool_id" {
  value = aws_cognito_user_pool.game_users.id
}

output "cognito_client_id" {
  value = aws_cognito_user_pool_client.game_client.id
}

output "aws_region" {
  value = var.aws_region
}