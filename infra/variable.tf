# variables.tf
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "eu-west-2"
}

variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "ai-adventure"
}

variable "environment" {
  description = "Environment (dev, staging, prod)"
  type        = string
  default     = "DEVELOPMENT"
}

# Add to your existing variables
variable "lambda_timeout" {
  description = "Lambda function timeout in seconds"
  type        = number
  default     = 30
}

variable "lambda_memory" {
  description = "Lambda function memory size in MB"
  type        = number
  default     = 256
}

variable "log_retention_days" {
  description = "Number of days to retain Lambda logs"
  type        = number
  default     = 14
}