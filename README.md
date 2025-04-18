# 🚀 SpaceX Launch Tracker (Technical Challenge - efrouting)

This project is a full-stack solution that monitors SpaceX launches using AWS Lambda, DynamoDB, API Gateway, ECS Fargate, and a Vue.js web application. It includes automated ingestion, storage, visualization, and deployment pipelines, following modern cloud-native and CI/CD best practices.
## 📁 Project Structure
```bash
SpacexBackend/               # Backend (Lambda functions + API Gateway + DynamoDB)
├── aws_lambda/
│   ├── fetch_launches/      # Lambda to ingest SpaceX launch data
│   └── get_launches/        # Lambda to expose launch data via API Gateway
├── tests/                   # Unit and integration tests
├── requirements.txt
├── .gitignore
└── README.md
```

## 🧠 Features
✅ Automatic ingestion of launch data from the SpaceX public API.

✅ Data stored in DynamoDB using upsert logic to avoid duplication.

✅ API Gateway exposes a REST endpoint for accessing the data.

✅ CI/CD pipeline using GitHub Actions handles tests and deployments.