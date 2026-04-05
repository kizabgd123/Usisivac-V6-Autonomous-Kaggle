"""Cloudflare Python Worker - Usisivač V6 System."""
from js import Response

async def on_fetch(request, env):
    """
    Handle incoming fetch requests.
    Args:
        request: The incoming request object.
        env: The environment variables.
    Returns:
        Response: Operational status message.
    """
    _ = (request, env) # Use the variables to avoid unused parameter warnings
    return Response.new("Usisivač V6 Autonomous Intelligence System - Operational")
