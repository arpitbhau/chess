import asyncio
import secrets

async def handle_client(reader, writer):
    addr = writer.get_extra_info("peername")
    print(f"[+] Client connected: {addr}")

    # Generate a 64-character random hex seed
    seed = secrets.token_hex(32)

    # Send response to the client
    response = f"200 OK\nSeed: {seed}\n"
    writer.write(response.encode())
    await writer.drain()

    # Keep the connection open until the client disconnects
    try:
        while True:
            data = await reader.readline()
            if not data:
                print(f"[-] Client {addr} disconnected")
                break

            message = data.decode().strip()
            print(f"[{addr}] -> {message}")

            if message.upper() == "FIN":
                writer.write(b"200 Connection closed\n")
                await writer.drain()
                break

            # Echo or handle message as needed
            writer.write(f"Echo: {message}\n".encode())
            await writer.drain()

    except Exception as e:
        print(f"[!] Error with {addr}: {e}")

    finally:
        writer.close()
        await writer.wait_closed()
        print(f"[x] Connection closed for {addr}")


async def main():
    server = await asyncio.start_server(handle_client, "0.0.0.0", 4444)
    print("🏁 Asyncio seed server running on port 65432")

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
