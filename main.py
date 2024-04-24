import httpx
import asyncio
import time

timeout = httpx.Timeout(100.0, read=None)


async def make_request(
    client: httpx.AsyncClient,
    url_: str,
    headers_: dict,
    params_: dict,
):
    """Effectue une requête HTTP asynchrone."""
    response = await client.request(
        "GET", url_, headers=headers_, params=params_, timeout=timeout
    )
    return response.status_code


async def main(
    url_: str,
    headers_: dict,
    params_: dict,
    n_requests_: int,
    delay_: float,
    n_concur_: int,
):
    """Effectue n_requests requêtes asynchrones."""
    time_total = time.perf_counter()
    res = 0
    async with httpx.AsyncClient() as client:
        for i in range(0, n_requests_, n_concur_):
            req_ = min(n_concur, n_requests - i)
            start_time = time.perf_counter()
            tasks = [
                asyncio.create_task(make_request(client, url_, headers_, params_))
                for _ in range(req_)
            ]
            res += len(tasks)
            responses = await asyncio.gather(*tasks)
            end_time = time.perf_counter()

            # Analyse des résultats
            success_count = 0
            for response in responses:
                if response == 200:
                    success_count += 1
            elapsed_time = end_time - start_time

            print(f"Nombre de requêtes : {req_}")
            print(f"Nb requêtes lancée: {res}")
            print(f"Temps écoulé : {elapsed_time:.2f} secondes")
            print(f"Taux de réussite : {success_count / req_:.2%}")
            print(f"Requêtes par seconde : {req_ / elapsed_time:.2f}")
        end_total = time.perf_counter()
        print(f"Temps total : {end_total - time_total:.2f} secondes")
        assert n_requests_ == res
        print(f"Nombre de requêtes total : {res}")
        print(f"Total Requêtes par seconde : {res / (end_total - time_total):.2f}")
        print(
            f"Temps total par requete : {(end_total - time_total) / n_requests_:.2f} secondes"
        )


if __name__ == "__main__":
    # Paramètres de test
    env = "uat"
    uat_url = "https://todo_uat"
    dev_url = "https://todo_dev"
    local = "http://127.0.0.1:8000"
    base_url = dev_url if env == "dev" else uat_url if env == "uat" else local
    url = f"{base_url}/todo"
    headers = {
        "Authorization": "BEARER todo",
        "accept": "application/json",
    }
    params = {}

    n_concur = 500
    n_requests = 2000
    delay = 0.00

    # Lancement du test
    asyncio.run(main(url, headers, params, n_requests, delay, n_concur))
