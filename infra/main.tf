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

  # Primary attributes
  attribute {
    name = "userId"
    type = "S"
  }

  attribute {
    name = "gameId"
    type = "S"
  }

  # GSI attributes
  attribute {
    name = "type"
    type = "S"
  }

  attribute {
    name = "timestamp"
    type = "S"
  }

  # Global Secondary Index for analytics
  global_secondary_index {
    name            = "TypeIndex"
    hash_key        = "type"
    range_key       = "timestamp"
    projection_type = "ALL"
  }

  tags = {
    Environment = var.environment
    Project     = var.project_name
  }
}
resource "aws_amplify_app" "game_app" {
  name = "${var.project_name}-${var.environment}"

  # Platform = Web Compute
  platform = "WEB_COMPUTE"

  # Build settings
  build_spec               = file("${path.module}/../amplify.yml")
  enable_branch_auto_build = true

  # Environment variables
  environment_variables = {
    ENV           = var.environment
    _CUSTOM_IMAGE = "public.ecr.aws/docker/library/node:18"
  }

  # Custom rules
  custom_rule {
    source = "/<*>"
    status = "404"
    target = "/index.html"
  }
}

# Add Amplify branch
resource "aws_amplify_branch" "main" {
  app_id      = aws_amplify_app.game_app.id
  branch_name = "dev"

  framework = "React"
  stage     = "DEVELOPMENT"

  environment_variables = {
    REACT_APP_ENVIRONMENT = "DEVELOPMENT"
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
# Cognito Identity Pool
resource "aws_cognito_identity_pool" "game_identity_pool" {
  identity_pool_name               = "${var.project_name}-identity-pool-${var.environment}"
  allow_unauthenticated_identities = false

  cognito_identity_providers {
    client_id               = aws_cognito_user_pool_client.game_client.id
    provider_name           = aws_cognito_user_pool.game_users.endpoint
    server_side_token_check = false
  }
}

# IAM role for authenticated users
resource "aws_iam_role" "authenticated" {
  name = "${var.project_name}-cognito-authenticated-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Federated = "cognito-identity.amazonaws.com"
        }
        Action = "sts:AssumeRoleWithWebIdentity"
        Condition = {
          StringEquals = {
            "cognito-identity.amazonaws.com:aud" = aws_cognito_identity_pool.game_identity_pool.id
          }
          "ForAnyValue:StringLike" = {
            "cognito-identity.amazonaws.com:amr" : "authenticated"
          }
        }
      }
    ]
  })
}

# IAM policy for authenticated users to access Lambda URL
resource "aws_iam_role_policy" "authenticated_policy" {
  name = "${var.project_name}-authenticated-policy-${var.environment}"
  role = aws_iam_role.authenticated.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "lambda:InvokeFunctionUrl"
        ]
        Resource = aws_lambda_function.game_logic.arn
      }
    ]
  })
}

# Attach roles to Identity Pool
resource "aws_cognito_identity_pool_roles_attachment" "main" {
  identity_pool_id = aws_cognito_identity_pool.game_identity_pool.id

  roles = {
    authenticated = aws_iam_role.authenticated.arn
  }
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
# Add this IAM role policy attachment
resource "aws_iam_role_policy_attachment" "lambda_policy" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "lambda_xray" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/AWSXRayDaemonWriteAccess"
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
  publish       = true # Enable versioning

  environment {
    variables = {
      GAME_TABLE   = aws_dynamodb_table.game_data.name
      CONTENT_PATH = "/var/task/game_content.json"
      ENVIRONMENT  = var.environment
    }
  }

  tracing_config {
    mode = "Active" # Enable X-Ray tracing
  }

  layers = [aws_lambda_layer_version.dependencies.arn] # Add dependencies layer

  tags = {
    Environment = var.environment
    Project     = var.project_name
  }

  depends_on = [
    aws_iam_role_policy_attachment.lambda_policy,
    aws_cloudwatch_log_group.lambda_logs
  ]
}

# CloudWatch Log Group for Lambda
resource "aws_cloudwatch_log_group" "lambda_logs" {
  name              = "/aws/lambda/${var.project_name}-game-logic-${var.environment}"
  retention_in_days = 14

  tags = {
    Environment = var.environment
    Project     = var.project_name
  }
}

# Lambda Layer for dependencies
resource "aws_lambda_layer_version" "dependencies" {
  filename            = "lambda_layer.zip"
  layer_name          = "${var.project_name}-dependencies"
  compatible_runtimes = ["python3.9"]

  description = "Dependencies for game logic lambda function"
}

# Alias for Lambda function
resource "aws_lambda_alias" "game_logic" {
  name             = var.environment
  description      = "Environment alias for game logic function"
  function_name    = aws_lambda_function.game_logic.function_name
  function_version = "$LATEST"
}
# Lambda ZIP file
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/bedrock-code"
  output_path = "${path.module}/lambda.zip"
}
# Lambda Function URL
# resource "aws_lambda_function_url" "game_logic_url" {
#   function_name      = aws_lambda_function.game_logic.function_name
#   authorization_type = "AWS_IAM"

#   cors {
#     allow_credentials = true
#     allow_origins     = ["*"]
#     allow_methods     = ["*"]
#     allow_headers     = ["date", "keep-alive", "authorization"]
#     expose_headers    = ["keep-alive", "date"]
#     max_age           = 86400
#   }
# }
# resource "aws_lambda_function_url" "game_logic_url" {
#   function_name      = aws_lambda_function.game_logic.function_name
#   authorization_type = "AWS_IAM"

#   cors {
#     allow_credentials = true
#     allow_origins     = ["*"]
#     allow_methods     = ["*"]
#     allow_headers     = ["*"] # Changed to allow all headers
#     expose_headers    = ["*"] # Changed to expose all headers
#     max_age           = 86400
#   }
# }
resource "aws_lambda_function_url" "game_logic_url" {
  function_name      = aws_lambda_function.game_logic.function_name
  authorization_type = "NONE"

  cors {
    allow_credentials = true
    allow_origins     = ["https://dev.d18jzwlw8rkuyv.amplifyapp.com"]
    allow_methods     = ["*"] # Keep this as "*" for now
    allow_headers = [
      "Authorization",
      "Content-Type",
      "X-Amz-Date",
      "X-Api-Key",
      "X-Amz-Security-Token"
    ]
    expose_headers = ["*"]
    max_age        = 86400
  }
}

# Outputs
output "lambda_function_name" {
  value = aws_lambda_function.game_logic.function_name
}

output "cognito_user_pool_id" {
  value = aws_cognito_user_pool.game_users.id
}

output "cognito_client_id" {
  description = "Cognito User Pool Client ID"
  value       = aws_cognito_user_pool_client.game_client.id
  sensitive   = true
}

output "aws_region" {
  value = var.aws_region
}

output "amplify_app_id" {
  value = aws_amplify_app.game_app.id
}

output "api_endpoint" {
  value = aws_lambda_function_url.game_logic_url.function_url
}
output "lambda_endpoint" {
  value = aws_lambda_function_url.game_logic_url.function_url
}
output "identity_pool_id" {
  value = aws_cognito_identity_pool.game_identity_pool.id
}