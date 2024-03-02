from fastapi import FastAPI, Request, Response
from fastapi.responses import StreamingResponse
import time
import asyncio

app = FastAPI()


# SSE endpoint
@app.get("/sse-endpoint")
async def sse_endpoint(request: Request):
    async def generate():
        while True:
            # Simulate sending updates every 1 second
            await asyncio.sleep(1)
            yield f"data: {str(time.time())}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


# HTML endpoint to render SSE updates
@app.get("/")
async def read_root(request: Request):
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SSE Example</title>
    </head>
    <body>
        <h1>Server-Sent Events (SSE) Example</h1>
        <div id="sse-data"></div>

        <script>
            const eventSource = new EventSource('/sse-endpoint');

            eventSource.onmessage = function(event) {
                // Handle incoming events
                const sseData = document.getElementById('sse-data');
                console.log(event.data)
                sseData.innerHTML = `Received event: ${event.data}`;
            };

            eventSource.onerror = function(error) {
                // Handle errors or connection issues
                console.error('Error occurred:', error);
            };
        </script>
    </body>
    </html>
    """
    return Response(content=html_content, media_type="text/html")
