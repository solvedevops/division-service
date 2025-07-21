# Division Service

A microservice that performs division operations as part of the [Useless Calculator](https://github.com/solvedevops/useless-calculator) project.

**⚠️ DEMO PROJECT WARNING**: This service is designed for demonstration and training purposes only. It should **NOT** be used in production environments. You have been warned!

## 🧮 Functionality

This service provides a simple REST API for dividing the first number by the second number.

### Endpoint

- **GET** `/` - Perform division operation
  - **Parameters:**
    - `first_number` (float, optional): Dividend (default: 0)
    - `second_number` (float, optional): Divisor (default: 0)
  - **Returns:** JSON object with operation result

- **GET** `/health` - Health check endpoint
  - **Returns:** Service health status

## 🛠️ Technology Stack

- **FastAPI** - Modern Python web framework
- **Python 3.7+** - Programming language
- **Pydantic** - Data validation and serialization
- **Docker** - Containerization

## 🚀 Quick Start

### Using Docker

```bash
# Build and run
docker build -t division-service .
docker run -p 5003:5003 \
  -e ENV_NAME=development \
  -e APP_NAME=division-service \
  -e TELEMETRY_MODE=console \
  division-service
```

### Manual Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables:**
   ```bash
   export ENV_NAME=development
   export APP_NAME=division-service
   export TELEMETRY_MODE=console
   ```

3. **Run the service:**
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 5003
   ```

## Container tags
In order to keep the containers small, the default tag :latest includes only local and console storage for logs, metrics and traces.
To demo cloud provide storage for logs, metrics and traces use the following tags. You still have to pass the TELEMETRY_MODE= env variable

- :latest for console and local storage
- :aws-logs for cloudwatch configuration (You need IAM for this to work)
- :azure-logs for Azure monitor (You need connection string for Azure monitor for this to work)


## ⚙️ Configuration

### Required Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `ENV_NAME` | Yes | `development` | Environment identifier |
| `APP_NAME` | Yes | `division-service` | Application identifier |

### Telemetry Configuration

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `TELEMETRY_MODE` | No | `console` | Logging destination |
| `AWS_DEFAULT_REGION` | CloudWatch | `us-east-1` | AWS region for CloudWatch |
| `APPLICATIONINSIGHTS_CONNECTION_STRING` | Azure | None | Azure Monitor connection |

#### Telemetry Modes

```bash
# Console output (default)
TELEMETRY_MODE=console

# Local file logging (structured: logs/env/app/service/)
TELEMETRY_MODE=local

# AWS CloudWatch (creates: /env/app/logs, /env/app/metrics, /env/app/traces)
TELEMETRY_MODE=aws_cloudwatch

# Azure Monitor (structured with env.app namespace)
TELEMETRY_MODE=azure_monitor

# Multiple outputs
TELEMETRY_MODE=console,local
```

## 📊 API Documentation

### Division Operation

**Request:**
```bash
GET /?first_number=10&second_number=2
```

**Response:**
```json
{
  "result": 5.0,
  "operation": "division",
  "first_number": 10.0,
  "second_number": 2.0
}
```

### Division by Zero Error

**Request:**
```bash
GET /?first_number=10&second_number=0
```

**Response (400 Bad Request):**
```json
{
  "detail": "Division by zero is not allowed"
}
```

### Health Check

**Request:**
```bash
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "division-service"
}
```

### Interactive API Documentation

When running the service, access:
- **Swagger UI**: http://localhost:5003/docs
- **ReDoc**: http://localhost:5003/redoc

## 📈 Monitoring & Observability

### Structured Telemetry

The service provides comprehensive observability:

- **Logs**: Operation events and errors
- **Metrics**: Performance metrics with response times
- **Traces**: Request tracing with operation details

#### Cloud Integration

**AWS CloudWatch:**
- Log Groups: `/{ENV_NAME}/{APP_NAME}/{logs|metrics|traces}`
- Log Streams: `division-service/{HOSTNAME}/{YYYY/MM/DD}`

**Azure Monitor:**
- Namespace: `{ENV_NAME}.{APP_NAME}`
- Service: `division-service`
- Types: logs, metrics, traces

### Example Telemetry Output

**Metrics:**
```json
{
  "operation": "division",
  "success": true,
  "response_time_ms": 15.3,
  "env_name": "production",
  "app_name": "division-service",
  "service_name": "division-service"
}
```

**Traces:**
```json
{
  "trace_id": "abc-123",
  "span_id": "def-456",
  "operation": "division",
  "duration_ms": 15.3,
  "metadata": {
    "first_number": 10.0,
    "second_number": 2.0,
    "result": 5.0
  }
}
```

## 🧪 Testing

### Running Tests

```bash
# Install test dependencies
pip install pytest httpx

# Run tests
pytest test_app.py -v
```

### Test Examples

```bash
# Test basic division
curl "http://localhost:5003/?first_number=10&second_number=2"
# Expected: {"result": 5.0, "operation": "division", ...}

# Test division by zero protection
curl "http://localhost:5003/?first_number=10&second_number=0"
# Expected: 400 Bad Request with {"detail": "Division by zero is not allowed"}

# Test health check
curl "http://localhost:5003/health"
# Expected: {"status": "healthy", "service": "division-service"}
```

## 🔧 Development

### Project Structure

```
division-service/
├── app.py              # FastAPI application
├── telemetry.py        # Telemetry and logging module
├── test_app.py         # Unit tests
├── requirements.txt    # Python dependencies
├── Dockerfile         # Container configuration
└── README.md          # This file
```

### Key Features

- ✅ Input validation and type conversion
- ✅ Comprehensive error handling
- ✅ Includes division by zero protection
- ✅ Health check endpoint
- ✅ Structured logging and telemetry
- ✅ API documentation
- ✅ Unit tests
- ✅ Docker support

## 🔐 Security Notes

- No sensitive data is processed or logged
- Input validation prevents basic injection attacks
- Telemetry follows secure logging practices
- Health checks don't expose sensitive information

## 📚 Related Services

- [Main Calculator](https://github.com/solvedevops/useless-calculator) - Web interface and orchestrator
- [Addition Service](https://github.com/solvedevops/addition-service) - Handles addition operations
- [Multiplication Service](https://github.com/solvedevops/multiplication-service) - Handles multiplication operations
- [Subtraction Service](https://github.com/solvedevops/subtraction-service) - Handles subtraction operations  


## ⚖️ License

This project is for educational and demonstration purposes. Use at your own risk in demo environments only.