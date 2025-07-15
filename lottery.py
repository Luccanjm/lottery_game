import requests
import time
import csv
import random
import concurrent.futures
from bs4 import BeautifulSoup
from collections import Counter

# global headers to be used for requests
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}

def extract_numbers_filtred(all_numbers_filtred,times_that_appear,selected_year,actual_year):

    all_numbers_frequencies = Counter(all_numbers_filtred) # Number : Quantity

    numbers_higher_than = {}

    for number,quantity in  all_numbers_frequencies.items():
        if quantity >= times_that_appear:
            numbers_higher_than[number] = quantity

    selected_numbers = list(numbers_higher_than.keys())

    if (selected_year - 1 ) == actual_year:
        print(f'Números que aparecem mais de {times_that_appear} vezes em todos os anos selecionados: {selected_numbers}')

    return selected_numbers

def extract_numbers(spans):
    numbers = []
    for span in spans:
        number = int(span.get_text())
        numbers.append(number)
    return numbers

def extract_data(soup,class_str):
    spans = soup.find_all('span', attrs={'class': f'{class_str}'})
    numbers = extract_numbers(spans)
    return numbers

def extract_lottery_name(class_str):
    lottery_str = class_str.split('_')[1]

    match lottery_str:
        case 'lfacil':
            return 'lotofacil'
        case 'mega':
            return 'mega-sena'
        case 'dupla':
            return 'dupla-sena'
        case 'quina':
            return 'quina'
    return None

def return_numbers_of(selected_year,class_str,times_that_appear):
    start_time = time.time()
    actual_year = 2025
    all_numbers_filtred = []
    lottery_name = extract_lottery_name(class_str)

    while selected_year <= actual_year:
        url = f'https://asloterias.com.br/resultados-da-{lottery_name}-{selected_year}'
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        numbers = extract_data(soup,class_str)
        selected_year += 1

        for number in numbers:
            all_numbers_filtred.append(number)

    numbers_extracted = extract_numbers_filtred(all_numbers_filtred, times_that_appear, selected_year, actual_year)

    end_time = time.time()
    print('Total time taken: ', end_time - start_time)
    return numbers_extracted

megasena_class = 'dezenas dezenas_mega'
quina_class = 'dezenas dezenas_quina'
dupla_class = 'dezenas dezenas_dupla'
lotofacil_class = 'dezenas dezenas_lfacil'

def write_game_in_csv():

    with open('jogos.csv', "a+",newline= '',encoding='utf8') as fp:
        writer = csv.writer(fp)
        file_have_row = fp.tell() > 0

        if not file_have_row:
            writer.writerow(["Lottery_name", "Game_numbers"])

        lotteries_dict = {"lotofacil": dict(selected_year=2003, class_str=f'{lotofacil_class}', times_that_appear=1676),
                          "megasena": dict(selected_year=1996, class_str=f'{megasena_class}', times_that_appear=309),
                          "quina": dict(selected_year=1994, class_str=f'{quina_class}', times_that_appear=308),
                          "dupla": dict(selected_year=2006, class_str=f'{dupla_class}', times_that_appear=610)}

        try:
            if fp.writable():
                for key,value in lotteries_dict.items():
                    game_result = return_numbers_of(value['selected_year'],value['class_str'], value['times_that_appear'])
                    writer.writerow([f'{key.upper()}',game_result])
            else:
                print("Arquivo não está no modo de escrita!")
        except Exception as e:
            print(f'Error: {e}')

if __name__ == '__main__':
    write_game_in_csv()