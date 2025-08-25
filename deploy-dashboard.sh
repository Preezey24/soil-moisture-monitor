#!/bin/bash

# Deploy IoT Rules + CloudWatch Dashboard using CloudFormation
# This creates persistent IoT Rules and dashboard that don't need to be recreated

echo "🚀 Deploying IoT Rules + CloudWatch Dashboard with CloudFormation"
echo "=================================================================="

# Check if AWS CLI is available
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI is required but not installed."
    exit 1
fi

# Check AWS credentials
echo "🔐 Checking AWS credentials..."
aws sts get-caller-identity > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "❌ Admin AWS credentials not configured. Please run 'aws configure'"
    exit 1
fi
echo "✅ Admin AWS credentials verified"

# Get AWS region from config or use default
AWS_REGION=$(aws configure get region)
if [ -z "$AWS_REGION" ]; then
    AWS_REGION="us-east-1"
    echo "⚠️  No region configured for default profile, using default: $AWS_REGION"
else
    echo "📍 Using region: $AWS_REGION"
fi

# Stack name
STACK_NAME="soil-moisture-iot-rules-dashboard"
TEMPLATE_FILE="cloudformation-dashboard.yaml"

echo
echo "📊 Deploying IoT Rules + CloudWatch dashboard..."

# Validate template first (skip if no permissions)
echo "🔍 Validating CloudFormation template..."
aws cloudformation validate-template \
    --template-body file://"$TEMPLATE_FILE" \
    --region "$AWS_REGION" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✅ Template validation successful"
else
    echo "⚠️  Template validation skipped (insufficient permissions - this is OK)"
fi

echo
echo "🚀 Starting CloudFormation deployment..."

# Deploy CloudFormation stack with verbose output
aws cloudformation deploy \
    --template-file "$TEMPLATE_FILE" \
    --stack-name "$STACK_NAME" \
    --parameter-overrides \
        DashboardName="SoilMoistureDashboard" \
        IoTTopicName="soil-moisture/data" \
        AWSRegion="$AWS_REGION" \
    --capabilities CAPABILITY_NAMED_IAM \
    --region "$AWS_REGION" \
    --no-fail-on-empty-changeset

DEPLOY_EXIT_CODE=$?

if [ $DEPLOY_EXIT_CODE -eq 0 ]; then
    echo "✅ CloudFormation deployment successful!"
    echo
    
    # Get dashboard URL from stack outputs
    DASHBOARD_URL=$(aws cloudformation describe-stacks \
        --stack-name "$STACK_NAME" \
        --region "$AWS_REGION" \
        --query 'Stacks[0].Outputs[?OutputKey==`DashboardURL`].OutputValue' \
        --output text)
    
    echo "🎉 Your IoT Rules + CloudWatch dashboard are ready!"
    echo "📊 Dashboard URL: $DASHBOARD_URL"
    echo
    echo "ℹ️  What was created:"
    echo "   ✅ IoT Rules to route sensor data to CloudWatch"
    echo "   ✅ CloudWatch Dashboard for visualization"
    echo "   ✅ IAM Role for IoT Rules to write to CloudWatch"
    echo
    echo "ℹ️  This infrastructure will persist and doesn't need to be recreated."
    echo "ℹ️  Your Python app now only needs to send data to IoT Core!"
    echo
    echo "Next steps:"
    echo "1. Run 'python3 main.py' to start sending data via IoT Core"
    echo "2. IoT Rules will automatically route data to CloudWatch"
    echo "3. View your dashboard at the URL above"
    
else
    echo "❌ CloudFormation deployment failed!"
    echo
    echo "� Check the AWS CloudFormation console for detailed error information:"
    echo "   https://$AWS_REGION.console.aws.amazon.com/cloudformation/home?region=$AWS_REGION#/stacks"
    echo
    echo "🚨 To clean up the failed stack:"
    echo "   aws cloudformation delete-stack --stack-name $STACK_NAME --region $AWS_REGION"
    echo
    exit 1
fi
