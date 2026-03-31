#!/usr/bin/env python3
"""Test WebSocket connection to nanobot."""

import asyncio
import json
import websockets


async def test_websocket():
    """Test WebSocket connection and get a response."""
    url = "ws://localhost:42002/ws/chat?access_key=msnk"
    
    try:
        async with websockets.connect(url) as ws:
            print("Connected to WebSocket")
            
            # Send a test message
            message = {"content": "Say hello"}
            await ws.send(json.dumps(message))
            print(f"Sent: {message}")
            
            # Wait for response
            response = await ws.recv()
            print(f"Received: {response[:200] if len(response) > 200 else response}")
            
            return True
    except Exception as e:
        print(f"Error: {e}")
        return False


if __name__ == "__main__":
    result = asyncio.run(test_websocket())
    print(f"Test {'passed' if result else 'failed'}")
