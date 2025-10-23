#!/bin/bash

echo "🚀 开始部署海上风电巡检风险评估系统到 ECS Fargate + ALB"

# 检查必要的工具
command -v npm >/dev/null 2>&1 || { echo "❌ 需要安装 Node.js 和 npm"; exit 1; }
command -v docker >/dev/null 2>&1 || { echo "❌ 需要安装 Docker"; exit 1; }

# 进入CDK目录
cd cdk-deployment

echo "📦 安装 CDK 依赖..."
npm install

echo "🏗️ 编译 TypeScript..."
npm run build

echo "🔧 Bootstrap CDK (如果需要)..."
npx cdk bootstrap

echo "🚀 部署到 AWS..."
npx cdk deploy --require-approval never

echo "✅ 部署完成！"
echo ""
echo "📋 获取服务URL:"
echo "前端 URL: $(aws cloudformation describe-stacks --stack-name OffshoreWindInspectionStack --query "Stacks[0].Outputs[?ExportName=='OffshoreWindFrontendEndpoint'].OutputValue" --output text)"
echo "后端 URL: $(aws cloudformation describe-stacks --stack-name OffshoreWindInspectionStack --query "Stacks[0].Outputs[?ExportName=='OffshoreWindBackendEndpoint'].OutputValue" --output text)"
