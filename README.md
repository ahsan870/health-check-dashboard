{
  "base_urls": {
    "dev": "https://your-dev-url.com",
    "sit": "https://your-sit-url.com",
    "uat": "https://your-uat-url.com",
    "prod": "https://your-prod-url.com"
  },
  "env_urls": {
    "dev": [
      {"name": "User Service", "path": "/api/users/health"},
      {"name": "Payment Service", "path": "/api/payments/health"}
    ],
    "sit": [
      {"name": "User Service", "path": "/api/users/health"},
      {"name": "Order Service", "path": "/api/orders/health"}
    ],
    "uat": [
      {"name": "Reporting Service", "path": "/api/reports/health"}
    ],
    "prod": [
      {"name": "Auth Service", "path": "/api/auth/health"},
      {"name": "Payment Gateway", "path": "/api/gateway/health"}
    ]
  }
}
