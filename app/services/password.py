import asyncio
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


hasher = PasswordHasher(
    time_cost=3,
    memory_cost=65536,
    parallelism=4,
    hash_len=32,
    salt_len=16,
)


async def hash(password: str) -> str:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, hasher.hash, password)


async def verify(password: str, hash: str) -> bool:
    loop = asyncio.get_running_loop()
    try:
        await loop.run_in_executor(None, hasher.verify, hash, password)
        return True
    except VerifyMismatchError:
        return False
