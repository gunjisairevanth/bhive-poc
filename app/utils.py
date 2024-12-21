from app.database import create_ttl_index
async def startup_tasks():
    print("Starting up...")
    await create_ttl_index()


async def shutdown_tasks():
    print("Shutting down...")