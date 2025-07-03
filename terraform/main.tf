provider "aws" {
    region = "us-west-2"  # Set your desired region
}

# Create a minimal IAM role with essential permissions
resource "aws_iam_role" "terraform_role" {
    name = "aws-amplify-terraform-role"
    assume_role_policy = jsonencode({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "cloudformation.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    })
}

# Attach managed policies instead of inline policies
resource "aws_iam_role_policy_attachment" "terraform_cloudformation" {
    role       = aws_iam_role.terraform_role.name
    policy_arn = "arn:aws:iam::aws:policy/AWSCloudFormationFullAccess"
}

resource "aws_iam_role_policy_attachment" "terraform_amplify" {
    role       = aws_iam_role.terraform_role.name
    policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess-Amplify"
}

# Minimal inline policy for specific permissions not covered by managed policies
resource "aws_iam_role_policy" "terraform_minimal" {
    name = "terraform-minimal-policy"
    role = aws_iam_role.terraform_role.id

    policy = jsonencode({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "iam:CreateRole",
                    "iam:DeleteRole",
                    "iam:PassRole",
                    "iam:AttachRolePolicy",
                    "iam:DetachRolePolicy",
                    "iam:PutRolePolicy",
                    "iam:DeleteRolePolicy"
                ],
                "Resource": "*"
            },
            {
                "Effect": "Allow",
                "Action": [
                    "s3:CreateBucket",
                    "s3:DeleteBucket",
                    "s3:PutBucketPolicy",
                    "s3:PutObject",
                    "s3:GetObject",
                    "s3:ListBucket"
                ],
                "Resource": "*"
            },
            {
                "Effect": "Allow",
                "Action": [
                    "lambda:CreateFunction",
                    "lambda:DeleteFunction",
                    "lambda:UpdateFunctionCode",
                    "lambda:AddPermission"
                ],
                "Resource": "*"
            },
            {
                "Effect": "Allow",
                "Action": [
                    "cognito-idp:CreateUserPool",
                    "cognito-idp:DeleteUserPool",
                    "cognito-idp:CreateUserPoolClient",
                    "cognito-idp:DeleteUserPoolClient"
                ],
                "Resource": "*"
            }
        ]
    })
}