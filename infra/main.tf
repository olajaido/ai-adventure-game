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
# IAM policy for authenticated users to access API Gateway
resource "aws_iam_role_policy" "authenticated_policy" {
  name = "${var.project_name}-authenticated-policy-${var.environment}"
  role = aws_iam_role.authenticated.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "execute-api:Invoke"
        ]
        Resource = "${aws_api_gateway_rest_api.game_api.execution_arn}/*"
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
  filename         = data.archive_file.lambda_zip.output_path
  function_name    = "${var.project_name}-game-logic-${var.environment}"
  role             = aws_iam_role.lambda_role.arn
  handler          = "lambda_handler.handle_game_action"
  runtime          = "python3.9"
  timeout          = 30
  memory_size      = 256
  publish          = true # Enable versioning
  source_code_hash = base64sha256(filebase64(data.archive_file.lambda_zip.output_path))

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
resource "aws_api_gateway_rest_api" "game_api" {
  name        = "${var.project_name}-api-${var.environment}"
  description = "Game API Gateway"

  endpoint_configuration {
    types = ["REGIONAL"]
  }
}

# Lambda permission for API Gateway
resource "aws_lambda_permission" "api_gateway" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.game_logic.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.game_api.execution_arn}/*/*"
}

# API Gateway resource
resource "aws_api_gateway_resource" "game_proxy" {
  rest_api_id = aws_api_gateway_rest_api.game_api.id
  parent_id   = aws_api_gateway_rest_api.game_api.root_resource_id
  path_part   = "{proxy+}"
}

# API Gateway method
resource "aws_api_gateway_method" "game_proxy" {
  rest_api_id   = aws_api_gateway_rest_api.game_api.id
  resource_id   = aws_api_gateway_resource.game_proxy.id
  http_method   = "ANY"
  authorization = "COGNITO_USER_POOLS"
  authorizer_id = aws_api_gateway_authorizer.game_auth.id

  request_parameters = {
    "method.request.path.proxy" = true
  }
}

# Cognito Authorizer
resource "aws_api_gateway_authorizer" "game_auth" {
  name          = "game-cognito-authorizer"
  type          = "COGNITO_USER_POOLS"
  rest_api_id   = aws_api_gateway_rest_api.game_api.id
  provider_arns = [aws_cognito_user_pool.game_users.arn]
  identity_source = "method.request.header.Authorization"
}

# API Gateway integration
resource "aws_api_gateway_integration" "lambda_proxy" {
  rest_api_id = aws_api_gateway_rest_api.game_api.id
  resource_id = aws_api_gateway_resource.game_proxy.id
  http_method = aws_api_gateway_method.game_proxy.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.game_logic.invoke_arn
}

# CORS configuration
resource "aws_api_gateway_method" "options" {
  rest_api_id   = aws_api_gateway_rest_api.game_api.id
  resource_id   = aws_api_gateway_resource.game_proxy.id
  http_method   = "OPTIONS"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "options" {
  rest_api_id = aws_api_gateway_rest_api.game_api.id
  resource_id = aws_api_gateway_resource.game_proxy.id
  http_method = aws_api_gateway_method.options.http_method
  type        = "MOCK"

  request_templates = {
    "application/json" = "{\"statusCode\": 200}"
  }
}

resource "aws_api_gateway_method_response" "options" {
  rest_api_id = aws_api_gateway_rest_api.game_api.id
  resource_id = aws_api_gateway_resource.game_proxy.id
  http_method = aws_api_gateway_method.options.http_method
  status_code = "200"

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true,
    "method.response.header.Access-Control-Allow-Methods" = true,
    "method.response.header.Access-Control-Allow-Origin"  = true
  }

  response_models = {
    "application/json" = "Empty"
  }
}

resource "aws_api_gateway_integration_response" "options" {
  rest_api_id = aws_api_gateway_rest_api.game_api.id
  resource_id = aws_api_gateway_resource.game_proxy.id
  http_method = aws_api_gateway_method.options.http_method
  status_code = aws_api_gateway_method_response.options.status_code

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
    "method.response.header.Access-Control-Allow-Methods" = "'GET,POST,OPTIONS'",
    "method.response.header.Access-Control-Allow-Origin"  = "'https://dev.d18jzwlw8rkuyv.amplifyapp.com'"
  }
}

# API Gateway deployment
resource "aws_api_gateway_deployment" "game_api" {
  rest_api_id = aws_api_gateway_rest_api.game_api.id

  depends_on = [
    aws_api_gateway_integration.lambda_proxy,
    aws_api_gateway_integration.options,
    aws_api_gateway_integration_response.proxy,
    aws_api_gateway_method_response.proxy
  ]

  lifecycle {
    create_before_destroy = true
  }

  triggers = {
    redeployment = sha1(jsonencode([
      aws_api_gateway_resource.game_proxy.id,
      aws_api_gateway_method.game_proxy.id,
      aws_api_gateway_integration.lambda_proxy.id,
      aws_api_gateway_integration_response.proxy.id,
      aws_api_gateway_method_response.proxy.id
    ]))
  }
}

# Add these new Gateway Responses for CORS
resource "aws_api_gateway_gateway_response" "cors_4xx" {
  rest_api_id   = aws_api_gateway_rest_api.game_api.id
  response_type = "DEFAULT_4XX"

  response_parameters = {
    "gatewayresponse.header.Access-Control-Allow-Origin"  = "'https://dev.d18jzwlw8rkuyv.amplifyapp.com'",
    "gatewayresponse.header.Access-Control-Allow-Headers" = "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
    "gatewayresponse.header.Access-Control-Allow-Methods" = "'GET,POST,OPTIONS'"
  }
}

resource "aws_api_gateway_gateway_response" "cors_5xx" {
  rest_api_id   = aws_api_gateway_rest_api.game_api.id
  response_type = "DEFAULT_5XX"

  response_parameters = {
    "gatewayresponse.header.Access-Control-Allow-Origin"  = "'https://dev.d18jzwlw8rkuyv.amplifyapp.com'",
    "gatewayresponse.header.Access-Control-Allow-Headers" = "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
    "gatewayresponse.header.Access-Control-Allow-Methods" = "'GET,POST,OPTIONS'"
  }
}

# Add this Method Response for the proxy
resource "aws_api_gateway_method_response" "proxy" {
  rest_api_id = aws_api_gateway_rest_api.game_api.id
  resource_id = aws_api_gateway_resource.game_proxy.id
  http_method = aws_api_gateway_method.game_proxy.http_method
  status_code = "200"

  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin"  = true,
    "method.response.header.Access-Control-Allow-Methods" = true,
    "method.response.header.Access-Control-Allow-Headers" = true
  }
}

# Add this Integration Response for the proxy
resource "aws_api_gateway_integration_response" "proxy" {
  rest_api_id = aws_api_gateway_rest_api.game_api.id
  resource_id = aws_api_gateway_resource.game_proxy.id
  http_method = aws_api_gateway_method.game_proxy.http_method
  status_code = aws_api_gateway_method_response.proxy.status_code

  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin"  = "'https://dev.d18jzwlw8rkuyv.amplifyapp.com'",
    "method.response.header.Access-Control-Allow-Methods" = "'GET,POST,OPTIONS'",
    "method.response.header.Access-Control-Allow-Headers" = "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'"
  }

  depends_on = [
    aws_api_gateway_method.game_proxy,
    aws_api_gateway_integration.lambda_proxy
  ]
}

# API Gateway stage
resource "aws_api_gateway_stage" "game_api" {
  deployment_id = aws_api_gateway_deployment.game_api.id
  rest_api_id   = aws_api_gateway_rest_api.game_api.id
  stage_name    = var.environment
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

output "identity_pool_id" {
  value = aws_cognito_identity_pool.game_identity_pool.id
}
output "api_endpoint" {
  value       = aws_api_gateway_stage.game_api.invoke_url
  description = "API Gateway endpoint URL"
}