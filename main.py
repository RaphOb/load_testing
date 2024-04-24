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
    uat_url = "https://uat.api.veolia.com/hub-api/v1"
    dev_url = "https://dev.api.veolia.com/hub-api/v1"
    local = "http://127.0.0.1:8000"
    base_url = dev_url if env == "dev" else uat_url if env == "uat" else local
    # url = "http://127.0.0.1:8000/api/kpi_values/synthesis/campaign/5128eacf-a2e3-4a3a-b532-feb9a106b423/roadmap/d419d570-721a-45a2-8d28-0d8fd119f95e"
    # url = "http://127.0.0.1:8000/api/kpi_values/synthesis/campaign/test/5128eacf-a2e3-4a3a-b532-feb9a106b423/roadmap/d419d570-721a-45a2-8d28-0d8fd119f95e"
    # url = f"{base_url}/api/users/timothee.galpin@veolia.com.test-google-a.com"
    url = f"{base_url}/api/users/autocomplete/evola"
    # url = f"{base_url}/auto_complete"
    # url = f"{base_url}/api/health"
    headers = {
        "Authorization": "BEARER j4eHCQbq8PmoYc7tD2QtgvEwJWGT",
        "x-hubapi-jwt": "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjA4YmY1YzM3NzJkZDRlN2E3MjdhMTAxYmY1MjBmNjU3NWNhYzMyNmYiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiIzMjU1NTk0MDU1OS5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsImF1ZCI6IjMyNTU1OTQwNTU5LmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwic3ViIjoiMTAyMzkxMTE2ODQ3Mzc1NTIwNTE2IiwiaGQiOiJ2ZW9saWEuY29tIiwiZW1haWwiOiJyYXBoYWVsLm9iYWRpYS5leHQuYWRtQHZlb2xpYS5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiYXRfaGFzaCI6Ikg5SjFHUzdMSDNkXzRVM19TUndMZmciLCJpYXQiOjE3MTAzNjE0MzYsImV4cCI6MTcxMDM2NTAzNn0.iJas-6xvBIN9g0no1wMY7y4Y1qciTieKD35D8pGbu2IorlBm6q-NWqK0cqs5rsWidxtkyFXRsGnRAYkzroz4kMA5VwsliesZguiyDKtNgEHBX3nOJkKS-dv_zHRjpKmpC6-Go6w3W0mqWJ3fal9W2RKsqT7Q8ZZXODiPh6CguIpJfxD8xT9ZqV9MGqkq8YFjeLpaVMQQYWvJFsoYjfVkolyOM-ImMHe4oY3O0oCQCI_E3suaewur5iEiPxAIKuRVu9UA02md7KNfQ-WhWTwfe170d6DbmvxACNAawFnfdLefJPLft7rQOG_hZ2_tpYX9hF8AOL-xm7KegJ2duqRA6w",
        "accept": "application/json",
        "x-data-origin": "cache",
    }
    # params = {"q": "test"}
    params = {}

    n_concur = 500
    n_requests = 2000
    delay = 0.01

    # Lancement du test
    asyncio.run(main(url, headers, params, n_requests, delay, n_concur))
