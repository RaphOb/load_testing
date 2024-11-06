import httpx
import asyncio
import time

timeout = httpx.Timeout(250.0, read=None)
limits = httpx.Limits(max_keepalive_connections=1000, max_connections=1000)


async def make_request_get(
    client: httpx.AsyncClient,
    url_: str,
    headers_: dict,
    params_: dict,
):
    """Effectue une requête HTTP asynchrone."""
    response = await client.request(
        "GET", url_, headers=headers_, params=params_, timeout=timeout
    )
    return response


async def make_request_post(
    client: httpx.AsyncClient,
    url_: str,
    headers_: dict,
    params_: dict,
    data: dict,
):
    """Effectue une requête HTTP asynchrone."""
    response = await client.request(
        "POST", url_, headers=headers_, params=params_, timeout=timeout, json=data
    )
    return response


async def main(
    url_: str,
    headers_: dict,
    params_: dict,
    n_requests_: int,
    delay_: float,
    n_concur_: int,
    data: dict,
):
    """Effectue n_requests requêtes asynchrones."""
    time_total = time.perf_counter()
    res = 0
    total_success_count = 0
    async with httpx.AsyncClient(limits=limits) as client:
        for i in range(0, n_requests_, n_concur_):
            req_ = min(n_concur, n_requests - i)
            start_time = time.perf_counter()
            tasks = [
                asyncio.create_task(
                    make_request_post(
                        client, url_, headers_, params_, {"data": "prout"}
                    )
                )
                for _ in range(req_)
            ]
            res += len(tasks)
            responses = await asyncio.gather(*tasks)
            end_time = time.perf_counter()

            # Analyse des résultats
            success_count = 0
            for response in responses:
                if response.status_code == 200:
                    success_count += 1
                    total_success_count += 1
                elif response.status_code == 429:
                    print(response.content)
            elapsed_time = end_time - start_time

            print(f"Nombre de requêtes : {req_}")
            print(f"Nb requêtes lancée: {res}")
            print(f"Temps écoulé : {elapsed_time:.2f} secondes")
            print(f"Taux de réussite : {success_count / req_:.2%}")
            print(f"Requêtes par seconde : {req_ / elapsed_time:.2f}")
            print(f"Requête ok par seconde : {success_count / elapsed_time:.2f}")
        end_total = time.perf_counter()
        print(f"Temps total : {end_total - time_total:.2f} secondes")
        assert n_requests_ == res
        print(f"Nombre de requêtes total : {res}")
        print(f"Total Requêtes par seconde : {res / (end_total - time_total):.2f}")
        print(
            f"Total Requête ok par seconde : {total_success_count / (end_total - time_total):.2f}"
        )
        print(
            f"Temps total par requete : {(end_total - time_total) / n_requests_:.2f} secondes"
        )


if __name__ == "__main__":
    # Paramètres de test
    env = "local"
    uat_url = "https://todo_uat"
    dev_url = "https://todo_dev"
    local = "http://127.0.0.1:8000"
    base_url = dev_url if env == "dev" else uat_url if env == "uat" else local
    url = f"{base_url}/test"
    headers = {
        "Authorization": "BEARER todo",
        "accept": "application/json",
    }
    params = {}
    body = {
        "deliveryAttempt": 5,
        "message": {
            "attributes": {"key": "value"},
            "data": "SGVsbG8gQ2xvdWQgUHViL1N1YiEgSGVyZSBpcyBteSBtZXNzYWdlIQ==",
            "messageId": "2070443601311540",
            "message_id": "2070443601311540",
            "orderingKey": "key",
            "publishTime": "2021-02-26T19:13:55.749Z",
            "publish_time": "2021-02-26T19:13:55.749Z",
        },
        "subscription": "projects/myproject/subscriptions/mysubscription",
    }
    n_concur = 50
    n_requests = 1000
    delay = 0.00

    # Lancement du test
    asyncio.run(main(url, headers, params, n_requests, delay, n_concur, data=body))
