from html import escape

import flyte
import pyfiglet

env = flyte.TaskEnvironment(
    name="deploy-demo",
    image=flyte.Image.from_base(
        image_uri="europe-west1-docker.pkg.dev/nav-data-images-prod/nav-union-images/flyte:3.14-base"
    )
    .clone(
        registry="europe-west1-docker.pkg.dev/nav-data-images-prod/nav-union-images",
        name="flyte",
        extendable=True,
    )
    .with_env_vars(
        {
            "UV_KEYRING_PROVIDER": "subprocess",
        }
    )
    .with_uv_project(
        pyproject_file="pyproject.toml",
        index_url=(
            "https://oauth2accesstoken@"
            "europe-west1-python.pkg.dev/nav-data-images-prod/pypi/simple/"
        ),
    ),
)


@env.task(entrypoint=True, report=True)
async def main() -> str:
    message = "Shipped!"
    banner = pyfiglet.figlet_format(message, font="small")

    await flyte.report.log.aio(
        f"""
        <div style="padding: 32px; background: #101827; color: #e5e7eb;
                    border-radius: 12px;">
          <p style="color: #34d399; font-family: sans-serif;">
            GITHUB &rarr; DEPLOY &rarr; FLYTE
          </p>
          <pre style="white-space: pre; overflow-x: auto;
                      font-family: monospace; font-size: 18px;
                      line-height: 1.2;">{escape(banner)}</pre>
          <p style="font-family: sans-serif;">
            Generated with pyfiglet inside the deployed task.
          </p>
        </div>
        """,
        do_flush=True,
    )

    return f"Generated report: {message}"
