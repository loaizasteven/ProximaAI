# Terraform Infrastructure for ProximaAI

Terraform configuration for AWS Amplify deployment.

## Step 1: Initial Deployment

```bash
cd terraform
terraform init
export TF_VAR_github_access_token="your_token"
terraform apply
```

## Step 2: Migrate to GitHub App

**Warning**: AWS now recommends GitHub Apps over Personal Access Tokens.

1. Go to Amplify Console → Your App → App Settings → Repository
2. Click "Disconnect repository"
3. Reconnect using "GitHub" → Authorize GitHub App
4. Select repository: `loaizasteven/ProximaAI`

## Configuration

- **Region**: us-east-1
- **App**: ProximaAI Application
- **Repository**: loaizasteven/ProximaAI
- **Build**: react-ui directory

## Cleanup

```bash
terraform destroy
``` 