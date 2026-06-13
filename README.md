# Watchlist API

A serverless REST API for tracking movies and TV shows across streaming platforms. Built with AWS Lambda, API Gateway, and DynamoDB, deployed via AWS SAM.

## Tech Stack

- **AWS Lambda** — Python 3.14 function handling all API logic
- **AWS API Gateway** — exposes REST endpoints publicly
- **AWS DynamoDB** — NoSQL database storing watchlist items
- **AWS SAM** — infrastructure as code for deployment
- **GitHub Actions** — CI/CD pipeline (coming soon)

## Endpoints

| Method | Path        | Description                          |
| ------ | ----------- | ------------------------------------ |
| POST   | /items      | Add a movie or show to the watchlist |
| GET    | /items      | Get all items in the watchlist       |
| GET    | /items/{id} | Get a single item by ID              |
| PATCH  | /items/{id} | Update the status of an item         |
| DELETE | /items/{id} | Remove an item from the watchlist    |

## Data Model

Each watchlist item stored in DynamoDB contains:

```json
{
  "item_id": "uuid",
  "title": "Breaking Bad",
  "type": "show",
  "platform": "Netflix",
  "status": "want to watch",
  "added_at": "2026-06-12T23:49:07.615462+00:00"
}
```

## Deploy Your Own

### Prerequisites

- AWS account with CLI configured (`aws configure`)
- AWS SAM CLI installed
- Python 3.14

### Steps

```bash
# Clone the repo
git clone https://github.com/dsubnaik/watchlist-api.git
cd watchlist-api/sam-app

# Build
sam build

# Deploy
sam deploy --guided
```

Follow the prompts. Once deployed, SAM will output your API Gateway URL.

## Example Requests

**Add an item**

```bash
curl -X POST https://<your-api-id>.execute-api.us-east-1.amazonaws.com/Prod/items \
  -H "Content-Type: application/json" \
  -d '{"title": "Breaking Bad", "type": "show", "platform": "Netflix", "status": "want to watch"}'
```

**Get all items**

```bash
curl https://<your-api-id>.execute-api.us-east-1.amazonaws.com/Prod/items
```

**Update status**

```bash
curl -X PATCH https://<your-api-id>.execute-api.us-east-1.amazonaws.com/Prod/items/{id} \
  -H "Content-Type: application/json" \
  -d '{"status": "watched"}'
```

## Author

Derrick Subnaik — [github.com/dsubnaik](https://github.com/dsubnaik)
