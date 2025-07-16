import unittest

from bs4 import BeautifulSoup

from lottery.lottery import extract_numbers_filtred,extract_numbers,extract_data, extract_lottery_name,return_numbers_of,write_game_in_csv

class TestDataExtractions(unittest.TestCase):
    html = '''
    <span class="dezenas dezenas_lfacil">12</span>
    <span class="dezenas dezenas_lfacil">7</span>
    <span class="dezenas dezenas_lfacil">1</span>
    <span class="dezenas dezenas_lfacil">17</span>
    <span class="dezenas dezenas_lfacil">24</span>
    <span class="dezenas dezenas_lfacil">8</span>
    <span class="dezenas dezenas_lfacil">14</span>
    <span class="dezenas dezenas_lfacil">21</span>
    <span class="dezenas dezenas_lfacil">12</span>
    <span class="dezenas dezenas_lfacil">12</span>
    <span class="dezenas dezenas_lfacil">12</span>
    <span class="dezenas dezenas_lfacil">17</span>
    <span class="dezenas dezenas_lfacil">17</span>
    <span class="dezenas dezenas_lfacil">17</span>
    '''
    
    soup = BeautifulSoup(html, 'html.parser')
    spans = soup.find_all('span', class_='dezenas dezenas_lfacil')
    
    
    def test_return_extract_numbers_filtred_correctly(self):
        num_filtred = [1,2,3,4,5,6,1,3,4,5,6,2,3,4,3,5,6,5,6,5,6,5,6]
        numbers_filtred_result = extract_numbers_filtred(num_filtred,6,2002,2004)
        self.assertEqual(numbers_filtred_result,[5,6])

    def test_return_extract_numbers_correctly(self, spans=spans):
        numbers_result = extract_numbers(spans)
        self.assertEqual(numbers_result, [12, 7, 1, 17, 24, 8, 14, 21, 12, 12, 12, 17, 17,17])

    def test_return_extract_data(self, soup= soup):
        data_results = extract_data(soup,'dezenas dezenas_lfacil')
        self.assertEqual(data_results, [12, 7, 1, 17, 24, 8, 14, 21, 12, 12, 12, 17, 17, 17])

    def test_return_extract_lottery_name(self):
        lottery_name_result = extract_lottery_name('dezenas dezenas_mega')
        self.assertEqual(lottery_name_result, 'mega-sena')

if __name__ == '__main__':
    unittest.main()
