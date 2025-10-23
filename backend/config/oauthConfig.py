from authlib.integrations.starlette_client import OAuth

from config.envConfig import settings

oauth = OAuth()
oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_id=settings.google_client_id,
    client_secret=settings.google_client_secret,
    client_kwargs={
        "scope": "openid email profile",
    },
)

oauth.register(
    name="microsoft",
    client_id=settings.ms_client_id,
    client_secret=settings.ms_client_secret,
    server_metadata_url=f"https://login.microsoftonline.com/{settings.ms_tenant_id}/v2.0/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)
