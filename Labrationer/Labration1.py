# Labration 1
# Verktyg för att lösa flerstegs-API
 
import requests
 
 
def get_url(url):
    #GET request från en url
    response = requests.get(url)
    return response.json()

def post_url(url, headers=None, data=None):
    # POST request från en url
    try:
        response = requests.post(url, headers=headers, json=data, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as error:
        print(f"HTTP-fel: {error}")
    except requests.exceptions.ConnectionError as error:
        print(f"Kunde inte ansluta till servern: {error}")
    except requests.exceptions.RequestException as error:
        print(f"Ett nätverksfel uppstod som vi inte förutsåg: {error}")
    except Exception as error:
        print(f"Ett fel som inte har med nätverket att göra uppstod: {error}")
    return None

if __name__ =="__main__":
    api_base = "http://10.3.10.104:3000"

    token_response = post_url(api_base+"/api/token")
    if token_response and "token" in token_response:
        token_value = token_response["token"]
        print(f"\nToken: {token_value}")

        # --- STEG 2: Verifiera ---
        headers = {"Authorization": f"Bearer {token_value}"}
        token_verify = post_url(api_base + "/api/verify", headers=headers)

        if token_verify and "secret" in token_verify:
            secret_value = token_verify["secret"]
            print(f"Verifiering lyckades! Secret: {secret_value}")

            # --- STEG 3: Skicka Flagga ---
            flag_data = {"token": token_value, "secret": secret_value}
            flag_response = post_url(api_base + "/api/flag", headers=headers, data=flag_data)

            if flag_response:
                print("Flag response:", flag_response)
        else:
            print("Kunde inte hämta 'secret' från verifieringen.")
    else:
        print("Kunde inte genomföra steg 1. Kontrollera anslutningen eller API-nycklar.")