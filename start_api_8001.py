#!/usr/bin/env python3
import uvicorn

if __name__ == "__main__":
    uvicorn.run("main_new:app", host="0.0.0.0", port=8001, reload=False)