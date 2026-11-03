"""Run the chatrdc agent on loopback only."""

import uvicorn


def main() -> None:
    uvicorn.run(
        "agent.main:app",
        host="127.0.0.1",
        port=8765,
        access_log=False,
        proxy_headers=False,
        reload=False,
    )


if __name__ == "__main__":
    main()
