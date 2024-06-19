import datetime
from datetime import timedelta
import yfinance as yf



def get_price_12_months_ago(ticker_symbol):
    """ 
        float: O preço de fechamento da ação há 12 meses.
    """
    ticker = yf.Ticker(ticker_symbol)
    end_date = datetime.datetime.now()
    start_date = end_date - timedelta(days=365)
    try:
        historical_data = ticker.history(start=start_date, end=end_date)
        price_12_months_ago = historical_data['Close'].iloc[0]
        return price_12_months_ago
    except (IndexError, KeyError) as e:
        print(f"Erro ao obter o preço para {ticker_symbol}: {e}")
        return None


def get_cotacao(ticker_symbol):
    """  
        float: O preço de fechamento atual da ação.
    """
    ticker = yf.Ticker(ticker_symbol)
    try:
        cotacao = ticker.history(period="1d")['Close'].iloc[0]
        return cotacao
    except (IndexError, KeyError) as e:
        print(f"Erro ao obter o preço para {ticker_symbol}: {e}")
        return None


def calcular_preco_teto(dividendo_anual, media_dividendo):
    """
    Calcula o preço teto com base no dividendo anual e na média de dividendos. 
    Returns:
        float: Preço teto calculado.
    """
    return dividendo_anual / media_dividendo


def calcular_margem_seguranca(preco_teto_calculado, cotacao_atual):
    """
    Returns:
        float: Margem de segurança percentual.
    """
    return (preco_teto_calculado - cotacao_atual) / cotacao_atual * 100


def calcular_valorizacao(cotacao_atual, cotacao_12_meses):
    """   
        float: Valorização percentual.
    """
    return (cotacao_atual - cotacao_12_meses) / cotacao_12_meses * 100


def main():
    """
    Função principal para obter dados de entrada do usuário e calcular o preço teto, margem de segurança e valorização.
    """
    ticker_acao = input("Digite o ticker que deseja buscar no formato ex: TAEE11.SA: ")
    cotacao_atual = get_cotacao(ticker_acao)
    cotacao_12_meses = get_price_12_months_ago(ticker_acao)

    if cotacao_atual and cotacao_12_meses:
        try:
            media_dividendo = float(input(
                "Digite a média de dividendo anual dos últimos anos. Exemplo: se for 10% você coloca 0.10: "
            ))
            dividendo_anual = float(input(
                "Digite qual é a média paga por ano. Exemplo: 2.20: "
            ))
            preco_teto_pessoal = float(input(
                "Digite o seu preço teto pessoal: "
            ))

            preco_teto_calculado = calcular_preco_teto(dividendo_anual, media_dividendo)
            margem_seguranca = calcular_margem_seguranca(preco_teto_calculado, cotacao_atual)
            margem_pessoal = calcular_margem_seguranca(preco_teto_pessoal, cotacao_atual)
            valorizacao = calcular_valorizacao(cotacao_atual, cotacao_12_meses)

            print(f"\nA cotação atual de {ticker_acao} é: R${cotacao_atual:.2f}")
            if preco_teto_calculado > preco_teto_pessoal:
                print("O preço teto está abaixo do preço pessoal. \nSugestão: Comprar")
            else:
                print("O preço teto está acima do preço pessoal. \nSugestão: Vender ou manter na carteira")

            print(f"O preço teto para {ticker_acao} é: R${preco_teto_calculado:.2f}")
            print(f"\nA margem de segurança do {ticker_acao} é: {margem_seguranca:.2f}%")
            print(f"A margem de segurança pessoal do {ticker_acao} é: {margem_pessoal:.2f}%")
            print(f"\nA cotação de {ticker_acao} há 12 meses era: R${cotacao_12_meses:.2f}")
            print(f"A valorização de {ticker_acao} nos últimos 12 meses foi: {valorizacao:.2f}%")

        except ValueError as e:
            print(f"Erro: Certifique-se de que todos os valores inseridos sejam números no formato correto. Detalhes do erro: {e}")
    else:
        print("Não foi possível obter a cotação atual ou o preço de 12 meses atrás.")


if __name__ == "__main__":
    main()
