#============================= LINK 8 ============================#
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from bs4 import BeautifulSoup

def start_driver(url):
    driver = webdriver.Chrome()
    driver.get(url)
    return driver

def extract_data(driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table = soup.find('table', {'class': 'contenedor_centrado', 'id': 'grdReporte'})
    data = []
    if table:
        rows = table.find_all('tr')[1:]
        for row in rows:
            cols = row.find_all('td')
            if len(cols) > 0:
                record = {
                    'Fec. Resolución': cols[0].get_text(strip=True),
                    'Nro. Resolución': cols[1].get_text(strip=True),
                    'Sancionado': cols[2].get_text(strip=True),
                    'Sumilla': cols[3].get_text(strip=True),
                    'Tipo': cols[4].get_text(strip=True),
                    'Monto S/.': cols[5].get_text(strip=True),
                    'Con Recurso': cols[6].get_text(strip=True),
                    'N° Res. Resolutiva': cols[7].get_text(strip=True),
                    'Fecha Res. Resolutiva': cols[8].get_text(strip=True),
                }
                data.append(record)
    return data

def visit_links(driver):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'MainContent_grdReporte'))
    )
    table = driver.find_element(By.ID, 'MainContent_grdReporte')
    links = table.find_elements(By.CLASS_NAME, 'HiperSubrayado')
    all_data = []
    main_window = driver.current_window_handle
    for index, link in enumerate(links):
        try:
            driver.execute_script("arguments[0].scrollIntoView();", link)
            WebDriverWait(driver, 15).until(EC.element_to_be_clickable(link)).click()
            WebDriverWait(driver, 15).until(EC.number_of_windows_to_be(2))
            new_window = [window for window in driver.window_handles if window != main_window][0]
            driver.switch_to.window(new_window)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'table'))
            )
            extracted_data = extract_data(driver)
            if extracted_data:
                all_data.extend(extracted_data)
            driver.close()
            driver.switch_to.window(main_window)
        except TimeoutException:
            if len(driver.window_handles) > 1:
                driver.switch_to.window(main_window)
        except NoSuchElementException:
            if len(driver.window_handles) > 1:
                driver.switch_to.window(main_window)
        except Exception as e:
            if len(driver.window_handles) > 1:
                driver.switch_to.window(main_window)
    return all_data

def main():
    url = 'https://www.smv.gob.pe/ServicioSancionesImpuestas/frm_SancionesEmpresas?data=6D9FF7643381613ADE8EEBB66B8E0CF2C6CC64BCC4'
    driver = start_driver(url)
    extracted_data = visit_links(driver)
    if extracted_data:
        with open('extracted_data.json', 'w', encoding='utf-8') as json_file:
            json.dump(extracted_data, json_file, ensure_ascii=False, indent=2)
    driver.quit()

if __name__ == "__main__":
    main()
