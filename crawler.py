from selenium.webdriver.firefox.options import Options
from multiprocessing.dummy import Pool as ThreadPool
from selenium.webdriver import Firefox
from bs4 import BeautifulSoup
import platform
import time
import csv

def get_categorys(url, driver):
    # procura por categorias de produtos a partir da url
    # retorna uma lista de categorias
    categorys = []
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    first_ul = soup.find("ul", "submenu__list")
    links_a = first_ul.find_all("a")
    for link in links_a:
        categorys.append(link["href"])
    return categorys

def get_products(url, driver, page, data):
    # Procura por produtos, página por página, a partir da url de entrada
    # Retorna uma lista de listas: [produto, url do produto]
    computed_url ="{}?PS=50#{}".format(url, str(page))
    driver.get(computed_url)
    time.sleep(3)
    driver.refresh()
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    links = soup.find_all("div", "shelf-default__item")
    for link in links:
        a = link.find("a")
        data.append([a["href"], link.get("title")])
    if len(links) == 50:
        page += 1
        return get_products(url, driver, page, data)
    return data

def make_n_drivers(n):
    # Retorna uma lista de n drivers
    options = Options()
    options.add_argument('-headless')
    drivers_list = []
    path = "./geckodriver"
    if platform.system() == "Windows":
        path = path + ".exe"
    for _ in range(0,n):
        drivers_list.append(Firefox(executable_path=r"./geckodriver", options=options))
    return drivers_list

def pooling(url):
    # Gerencia as threads e os drivers.
    # Retorna os produtos encontrados
    driver = drivers_list.pop(0)
    products = get_products(url, driver, 1, [])
    drivers_list.append(driver)
    return products

def close_drivers(drivers_list):
    for driver in drivers_list:
        driver.quit()

if __name__ == "__main__":
    print("iniciando drivers e criando threads...")
    drivers = 4
    pool = ThreadPool(drivers)
    drivers_list = make_n_drivers(drivers)
    categorys = get_categorys("https://www.epocacosmeticos.com.br/", drivers_list[0])
    print("iniciando pool do crawler; total de threads/drivers = " + str(drivers))
    print("tempo estimado: 30 minutos")
    results = pool.map(pooling, categorys)
    pool.close()
    pool.join()
    print("Todas categorias foram scaneadas; fechando drivers de maneira segura. (pode levar alguns minutos")
    close_drivers(drivers_list)
    print("Escrevendo resultados em products.csv")
    total = 0
    with open("products.csv", "w", encoding='utf-8', newline="") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for category in results:
            total += len(category)
            for product in category:
                writer.writerow([product[1], product[0]])
    print("Escrita finalizada. foram encontrados {} produtos".format(total))
