import requests
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

def create_session():
    """Cria uma sessão com uma política de retry configurada."""
    session = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=2,
        status_forcelist=[429, 500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session
