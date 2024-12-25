from composition_root import CompositionRoot
import uvicorn
import ssl
import os
from dotenv import load_dotenv

load_dotenv()

cr = CompositionRoot()

app = cr.get_app()

# ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
# ssl_context.load_cert_chain(
#     os.getenv("CERT_PATH"),
#     keyfile=os.getenv("KEY_PATH")
# )

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
