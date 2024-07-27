# DjangoProject

This project is a website which allows users to to manage their stock portfolio and view real time updates of their investments worth and a graph displaying up to date trends. Additonally I trained an Llama model to attempt to predict stock prices for certain ETFs. The trained model can be found here: https://huggingface.co/sknorr/StockSight. Additonally, this project allows users to add stocks to their portfolio through a REST API Post. An example of this can be seen below:

# Python Script to obtain a token and post a stock
    import requests

    def obtain_token(base_url, username, password):
        url = f"{base_url}/api/token/"
        payload = {
            'username': username,
            'password': password
        }
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()['access']

    def add_stock(base_url, token, stock_tag, shares):
        url = f"{base_url}/api/add-stock/"
        payload = {
            'stock_tag': stock_tag,
            'shares': shares
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()

    if __name__ == "__main__":
        base_url = "http://localhost:8000"  # Change this to your base URL
        username = "your_username"  # Replace with your username
        password = "your_password"  # Replace with your password
        stock_tag = "AAPL"  # Replace with the stock tag you want to add
        shares = 10  # Replace with the number of shares

        try:
            # Obtain the token
            token = obtain_token(base_url, username, password)
            print("Token obtained successfully:", token)

            # Add the stock
            response = add_stock(base_url, token, stock_tag, shares)
            print("Stock added successfully:", response)
        except requests.exceptions.RequestException as e:
            print("An error occurred:", e)
