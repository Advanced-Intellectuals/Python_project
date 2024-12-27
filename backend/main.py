from composition_root import CompositionRoot
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

cr = CompositionRoot()

app = cr.get_app()

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000, ssl_certfile=os.getenv(
        "CERT_PATH"), ssl_keyfile=os.getenv("KEY_PATH"))
