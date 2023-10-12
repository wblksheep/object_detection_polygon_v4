import asyncio
import datetime

async def say_hello(delay, to):
    start_time = datetime.datetime.now()
    print(f"{start_time}: Waiting for {delay} seconds to say hello to {to}")
    await asyncio.sleep(delay)
    end_time = datetime.datetime.now()
    print(f"{end_time}: Hello, {to}! (Elapsed: {end_time - start_time})")

async def main():
    await asyncio.gather(
        say_hello(1, 'Alice'),
        say_hello(2, 'Bob'),
        say_hello(3, 'Charlie')
    )

# 运行主异步函数
asyncio.run(main())
