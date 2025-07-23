from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time
import uuid
from telemetry import create_telemetry_logger
#from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# Initialize telemetry
telemetry = create_telemetry_logger("division-service")
logger = telemetry.get_logger()

# Response model for API documentation
class DivisionResult(BaseModel):
    result: float
    operation: str = "division"
    first_number: float
    second_number: float

class HealthCheck(BaseModel):
    status: str
    service: str

def division(firstNumber: float, secondNumber: float) -> float:
    """Perform division of two numbers with error handling."""
    # Start trace
    trace_id = str(uuid.uuid4())
    span_id = str(uuid.uuid4())
    start_time = time.time()
    
    try:
        if secondNumber == 0:
            logger.error(f"Division by zero attempted: {firstNumber} / {secondNumber}")
            # Log metrics for error
            telemetry.log_metrics({
                "operation": "division",
                "error_type": "division_by_zero",
                "first_number": firstNumber,
                "second_number": secondNumber
            })
            raise ValueError("Cannot divide by zero")
        
        result = firstNumber / secondNumber
        duration_ms = (time.time() - start_time) * 1000
        
        # Log successful operation
        logger.info(f"Division performed: {firstNumber} / {secondNumber} = {result}")
        
        # Log trace
        telemetry.log_trace(
            trace_id=trace_id,
            span_id=span_id,
            operation="division",
            duration_ms=duration_ms,
            metadata={
                "first_number": firstNumber,
                "second_number": secondNumber,
                "result": result
            }
        )
        
        # Log metrics
        telemetry.log_metrics({
            "operation": "division",
            "success": True,
            "response_time_ms": duration_ms
        })
        
        return result
    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        telemetry.log_error_with_trace(e, {
            "operation": "division",
            "first_number": firstNumber,
            "second_number": secondNumber,
            "duration_ms": duration_ms
        })
        raise


app = FastAPI(
    title="Division Service",
    description="Microservice for performing division operations",
    version="1.0.0"
)
#FastAPIInstrumentor().instrument_app(app)

@app.get("/health", response_model=HealthCheck, tags=["health"])
async def health_check():
    """Health check endpoint to verify service is running."""
    logger.info("Health check requested")
    telemetry.log_metrics({
        "health_check": 1,
        "service": "division-service",
        "status": "healthy"
    })
    return {"status": "healthy", "service": "division-service"}

@app.get("/", response_model=DivisionResult, tags=["operations"])
async def divide_numbers(
    first_number: float = 0, 
    second_number: float = 0
) -> DivisionResult:
    """
    Divide two numbers.
    
    - **first_number**: The dividend (number to be divided)
    - **second_number**: The divisor (number to divide by)
    
    Returns the quotient of the division.
    """
    try:
        result = division(first_number, second_number)
        return DivisionResult(
            result=result,
            first_number=first_number,
            second_number=second_number
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
