#!/usr/bin/env python

import json
import sys
import time
sys.path.append('..')

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from collector.packages.driver import get_random_user_agent, quit_driver


def create_products_listing_pages_files(create_products_listing_pages_brands,
                                        driver_dict,
                                        brands_page_dict,
                                        products_listing_pages_folder_path):
    """Creates the products-listing pages files.

    Args:
        create_products_listing_pages_brands (function): function used to create the products-listing
                                                         pages brands.
        driver_dict (dict): dictionary with information of the driver.
        brands_page_dict (dict): dictionary with information from the products-listing brands page.
        products_listing_pages_folder_path (str): path of the directory in which the files 
                                                  will be created.
    """
        
    # Get a random user agent
    driver_dict['options'].add_argument(f'user-agent={get_random_user_agent()}')

    # Set the driver
    if driver_dict['headless']:
        driver_dict['options'].add_argument("--headless")
        
    service = Service(executable_path=driver_dict['driver_path'])
    driver = webdriver.Chrome(service=service, options=driver_dict['options'])
    
    # Create the products-listing pages brands
    create_products_listing_pages_brands(
        driver=driver,
        brands_page_dict=brands_page_dict,
        products_listing_pages_folder_path=products_listing_pages_folder_path)
    
    # Quit the driver
    quit_driver(driver=driver, delete_cookies=driver_dict['delete_cookies'])


def generate_products_listing_pages_dicts(from_brands, 
                                          brands,
                                          from_categories, 
                                          categories,  
                                          from_search_keywords, 
                                          search_keywords):
    """Generates the list of products-listing pages dictionaries.
    
    Args:
        from_brands (bool): whether to include product-listing pages from brands.
        brands (list): list of brand products-listing pages.
        from_categories (bool): whether to include product-listing pages from categories.
        categories (list): list of category products-listing pages.
        from_search_keywords (bool): whether to include product-listing pages from searches.
        search_keywords (list): list of search products-listing pages.
        
    Returns:
        list[dict], List of products-listing pages dictionaries.
    """

    products_listing_page_dicts = []

    if from_brands:
        if brands:
            for brand in brands:
                products_listing_page_dicts.append({
                    'origin': 'brand',
                    'product_brand': brand[0],
                    'url': brand[-1],
                })
    
    if from_categories:
        if categories:
            for category in categories:
                products_listing_page_dicts.append({
                    'origin': 'category',
                    'category': category[0],
                    'sub_category': category[1],
                    'sub_sub_category': category[2],
                    'url': category[-1],
                }) 
        
    if from_search_keywords:
        if search_keywords:
            for search_keyword in search_keywords:
                products_listing_page_dicts.append({
                    'origin': 'search',
                    'search_term': search_keyword[0],
                    'url': search_keyword[-1],
                }) 

    return products_listing_page_dicts


def get_products_listing_pages_dicts_to_collect(brands, 
                                                categories, 
                                                search_keywords, 
                                                args):
    """Gets the products-listing pages dictionaries to collect from the parsed arguments.
    
    Args:
        brands (list): list of brand products-listing pages.
        categories (list): list of category products-listing pages.
        search_keywords (list): list of search products-listing pages.
        args (dict): parsed arguments.
        
    Returns:
        list[dict], List of products-listing pages dictionaries.
    """

    if args.products_listing_page_url:
        products_listing_pages_dicts = [{
            'origin': 'parser',
            'url': args.products_listing_page_url,
        }]
    else:
        products_listing_pages_dicts = \
            generate_products_listing_pages_dicts(from_brands=args.from_brands,
                                                  brands=brands,
                                                  from_categories=args.from_categories,
                                                  categories=categories,
                                                  from_search_keywords=args.from_search_keywords,
                                                  search_keywords=search_keywords)
    
    return products_listing_pages_dicts


def collect_urls(save_products_listing_page_data,
                 driver_dict, 
                 source_dict,
                 products_listing_pages_dicts, 
                 new_urls_folder_path):
    """Collects the new URLs.

    Args:
        save_products_listing_page_data (function): function to save products-listing page data.
        driver_dict (dict): dictionary with information of the driver.
        source_dict (dict): dictionary with information from the source.
        products_listing_pages_dicts (list[dict]): list of products-listing pages dictionaries.
        new_urls_folder_path (str): path of the directory in which the URLs will be saved.
    """

    for products_listing_page_dict in products_listing_pages_dicts:
        # Get a random user agent
        driver_dict['options'].add_argument(f'user-agent={get_random_user_agent()}')
        
        # Set the driver
        if driver_dict['headless']:
            driver_dict['options'].add_argument("--headless")
            
        service = Service(executable_path=driver_dict['driver_path'])
        driver = webdriver.Chrome(service=service, options=driver_dict['options'])

        # Collect and save new URLs data
        save_products_listing_page_data(driver=driver, 
                                        products_listing_page_dict=products_listing_page_dict,
                                        source_dict=source_dict,
                                        new_urls_folder_path=new_urls_folder_path)
        
        # Quit the driver
        quit_driver(driver=driver, delete_cookies=driver_dict['delete_cookies'])


def collect_page(save_product_page_data,
                 driver_dict, 
                 source_dict,
                 product_page_dict,
                 n_max_reviews, 
                 min_date_year,
                 products_folder_path, 
                 reviews_folder_path):
    """Collect product data and reviews data from product page.

    Args:
        save_product_page_data (function): function to save product page data.
        driver_dict (dict): dictionary with information of the driver.
        source_dict (dict): dictionary with information from the source.
        product_page_dict (str): product page dict.
        n_max_reviews (int): max number of reviews to collect.
        min_date_year (int): oldest review year to collect.
        products_folder_path (str): path to the 'products' folder.
        reviews_folder_path (str): path to the 'reviews' folder.
    """

    # Set the driver
    if driver_dict['headless']:
        driver_dict['options'].add_argument("--headless")

    service = Service(executable_path=driver_dict['driver_path'])
    driver = webdriver.Chrome(service=service, options=driver_dict['options'])

    # Collect the product and reviews data
    save_product_page_data(driver=driver, 
                           product_page_dict=product_page_dict, 
                           source_dict=source_dict, 
                           n_max_reviews=n_max_reviews,
                           min_date_year=min_date_year,
                           products_folder_path=products_folder_path, 
                           reviews_folder_path=reviews_folder_path)
    
    # Quit the driver
    quit_driver(driver=driver, delete_cookies=driver_dict['delete_cookies'])


def collect_pages(save_product_page_data, 
                  driver_dict, 
                  source_dict, 
                  urls_to_collect_dicts_object_name, 
                  urls_to_collect_status, 
                  n_max_reviews, 
                  min_date_year, 
                  products_folder_path, 
                  reviews_folder_path):
    """Collects the data from URLs to collect.

    Args:
        save_product_page_data (function): Function used for saving product page data.
        driver_dict (dict): Dictionary with information of the driver.
        source_dict (dict): Dictionary with information from the source.
        urls_to_collect_dicts_object_name (str): URLs to collect object name.
        urls_to_collect_status (str): Status of the URLs to collect.
        n_max_reviews (int): Max number of reviews to collect.
        min_date_year (int): Oldest review year to collect.
        products_folder_path (str): Path to the 'products' folder.
        reviews_folder_path (str): Path to the 'reviews' folder.

    The function performs the following steps:
    1. Loads the most recent URLs to collect object name.
    2. Iterates through the URLs to collect data and performs the following steps:
       a. Collects and saves the product and reviews data.
       b. Checks the collected product data and sets the URL status accordingly based on specific conditions.
    3. Handles errors during data collection and sets the URL status as 'issue'.
    4. Writes the updated URLs to collect dictionary back to the file.

    The function is expected to be used for data collection and status management of URLs.
    """

    # Load the most recent URLs to collect object name
    urls_to_collect_dicts = json.load(
        open(urls_to_collect_dicts_object_name, 'r', encoding='utf-8'))

    for url_to_collect_dict in urls_to_collect_dicts:
        if url_to_collect_dict['collected'] == urls_to_collect_status:

            # Get a random user agent
            driver_dict['options'].add_argument(f'user-agent={get_random_user_agent()}')

            # Set the driver
            if driver_dict['headless']:
                driver_dict['options'].add_argument("--headless")

            service = Service(executable_path=driver_dict['driver_path'])
            driver = webdriver.Chrome(service=service, options=driver_dict['options'])
            print(f"[LOG] Time: {time.strftime('%H:%M:%S')}")

            try:
                # Collect and save the product and reviews data
                # --------------------------------------------------------
                product_dict, n_saved_reviews = save_product_page_data(
                    driver=driver,
                    product_page_dict=url_to_collect_dict,
                    source_dict=source_dict,
                    products_folder_path=products_folder_path,
                    reviews_folder_path=reviews_folder_path,
                    n_max_reviews=n_max_reviews,
                    min_date_year=min_date_year)

                # Change the status of the URL to collect
                # --------------------------------------------------------
                # Step 1
                # ** What: product data has been collected
                # ** How: 'product_dict' is not empty
                if product_dict:

                    # Step 2
                    # ** What: product data contains the mandatory fields
                    # ** How: the fields 'product_name' and 'product_brand' aren't None
                    if product_dict['product_name'] is not None and \
                       product_dict['product_brand'] is not None:

                        # Step 3
                        # ** What: product data has the field 'n_reviews'
                        # The number of reviews for the product is displayed on the product page
                        # and has been saved
                        # ** How: the field 'n_reviews' is in the 'product_dict' and the value
                        # is not None
                        if product_dict.get('n_reviews') and \
                           product_dict['n_reviews'] is not None:
                                
                                # Step 5
                                # ** What: the number of reviews for the product is displayed on the product page
                                # and has been saved in the field 'n_reviews' in the correct integer type
                                # ** How: the field 'n_reviews' in 'product_dict' is an integer
                                if isinstance(product_dict['n_reviews'], int):
                                
                                    # Step 6
                                    # ** What: the number of reviews on the product page has been saved
                                    # in the correct integer type and the product has reviews to collect
                                    # ** How: the field 'n_reviews' is strictly higher than 0
                                    if product_dict['n_reviews'] > 0:

                                        # Step 10
                                        # ** What: some reviews have been saved
                                        # ** How: `n_saved_reviews` is strictly higher than 0
                                        if n_saved_reviews > 0:

                                            # Step 11
                                            # ** What: the number of saved reviews is higher or equal to the number of displayed 
                                            # reviews on the product page
                                            # All the reviews available on the product page have been collected
                                            # ** How: `n_saved_reviews` is higher or equal than the field 'n_reviews' in the 'product_dict'
                                            # ** URL status: the current URL is saved as 'yes'
                                            if n_saved_reviews >= product_dict['n_reviews']:
                                                url_to_collect_dict['collected'] = 'yes'
                                                print("[LOG] [Step 11] All the reviews have been collected for the product.\n"
                                                      "[LOG] [Step 11] The current URL is saved as 'yes'.")

                                            # Step 11 (if not)
                                            # ** What: the number of saved reviews is lower than the number of displayed 
                                            # reviews on the product page
                                            # Not all the reviews available on the product page have been collected
                                            # ** How: `n_saved_reviews` is strictly lower than the field 'n_reviews' in the 'product_dict'
                                            # ** URL status: the current URL is saved as 'once'
                                            else:
                                                url_to_collect_dict['collected'] = 'once'
                                                print("[LOG] [Step 11 (if not)] Not all the reviews have been collected for the product.\n"
                                                      "[LOG] [Step 11 (if not)] Or the product has ratings without text.\n"
                                                      "[LOG] [Step 11 (if not)] The current URL is saved as 'once'.")                                      

                                        # Step 10 (if not)
                                        # ** What: no reviews have been saved
                                        # The product page displayed the product has reviews and the field
                                        # 'n_reviews' in the 'product_dict' has been correctly saved as a strictly
                                        # positive integer
                                        # There has been an issue with the reviews data collection
                                        # ** URL status: the current URL is saved as 'issue'
                                        else:
                                            url_to_collect_dict['collected'] = 'issue'
                                            print("[LOG] [Step 10 (if not)] There has been an issue with the current URL.\n"
                                                  "[LOG] [Step 10 (if not)] The current URL is saved as 'issue'.")

                                    # Step 6 (elif)
                                    # ** What: the number of reviews on the product page has been saved
                                    # in the correct integer type but the product hasn't any reviews to collect
                                    # ** How: the field 'n_reviews' is equal to 0 
                                    elif product_dict['n_reviews'] == 0:

                                        # Step 7
                                        # ** What: some reviews have been saved 
                                        # The number of saved reviews can't be compared with the number of reviews 
                                        # for the product because the information is displayed on the product page 
                                        # but has been saved as a null integer
                                        # There has been a problem with the product data collection
                                        # ** URL status: the current URL is saved as 'issue'
                                        if n_saved_reviews > 0:
                                            url_to_collect_dict['collected'] = 'issue'
                                            print("[LOG] [Step 7] There has been an issue with the current URL.\n"
                                                  "[LOG] [Step 7] The current URL is saved as 'issue'.")
                                            
                                        # Step 7 (if not)
                                        # ** What: no reviews have been saved
                                        # There aren't any saved reviews but the number of displayed reviews isn't correctly saved
                                        # There has been a problem with the product data collection
                                        # There has been a problem with the reviews data collecttion because 
                                        # the product is supposed to have reviews                                        
                                        # The current URL is saved as 'issue'
                                        else:
                                            url_to_collect_dict['collected'] = 'issue'
                                            print("[LOG] [Step 7 (if not)] There has been an issue with the current URL.\n"
                                                  "[LOG] [Step 7 (if not)] The current URL is saved as 'issue'.")
                                                                                
                                    # Step 6 (else)
                                    # ** What: The number of reviews on the product page has been saved
                                    # in the correct integer type but the product hasn't any reviews to collect
                                    # ** How: the field 'n_reviews' is lower than 0 
                                    else:

                                        # Step 8
                                        # ** What: some reviews have been saved 
                                        # The number of saved reviews can't be compared with the number of reviews 
                                        # for the product because the information is displayed on the product page 
                                        # but hasn't been saved correctly as a positive or null integer
                                        # It is impossible to know if all the reviews have been saved
                                        # ** How: `n_saved_reviews` is higher than 0
                                        # ** URL status: The current URL is saved as 'once'
                                        if n_saved_reviews > 0:
                                            url_to_collect_dict['collected'] = 'once'
                                            print("[LOG] [Step 8] Not all the reviews have been collected for the product.\n"
                                                  "[LOG] [Step 8] The current URL is saved as 'once'.") 

                                        # Step 9 (if not)
                                        # What: no reviews have been saved
                                        # There aren't any saved reviews but the number of displayed reviews is 
                                        # accessible on the product page and has been saved in the correct integer format
                                        # There has been a problem with the product data collection because 
                                        # the number of reviews is not in the correct positive or null integer format
                                        # There has been a problem with the reviews data collecttion because 
                                        # the product is supposed to have reviews
                                        # ** How: `n_saved_reviews` is equal to 0
                                        # ** URL status: The current URL is saved as 'issue'
                                        else:
                                            url_to_collect_dict['collected'] = 'issue'
                                            print("[LOG] [Step 9 (if not)] There has been an issue with the current URL.\n"
                                                  "[LOG] [Step 9 (if not)] The current URL is saved as 'issue'.")

                                # Step 5 (if not)
                                # ** What: the number of reviews for the product is displayed on the product page
                                # and has been saved in the field 'n_reviews' but the type isn't correct
                                # There has been a problem with the product data collection or the conversion of the
                                # field 'n_reviews' to integer                                
                                # How: the field 'n_reviews' in 'product_dict' isn't an integer         
                                else:

                                    # Step 12
                                    # ** What: some reviews have been saved 
                                    # The number of saved reviews can't be compare with the number of reviews for 
                                    # the product because the information is displayed on the product page 
                                    # but hasn't been saved correctly in the type integer
                                    # It is impossible to know if all the reviews have been saved
                                    # ** How: `n_saved_reviews` is higher than 0
                                    # ** URL status: The current URL is saved as 'once'
                                    if n_saved_reviews > 0:
                                        url_to_collect_dict['collected'] = 'once'
                                        print("[LOG] [Step 12] Not all the reviews have been collected for the product.\n"
                                              "[LOG] [Step 12] The current URL is saved as 'once'.")

                                    # Step 12 (if not)
                                    # What: no reviews have been saved
                                    # There aren't any saved reviews but the number of displayed reviews is accessible 
                                    # on the product page
                                    # There has been a problem with the product data collection because the number 
                                    # of reviews hasn't been in the correct integer type
                                    # And product is supposed to have reviews, so the number of saved reviews should be
                                    # higher than 0
                                    # ** How: `n_saved_reviews` is equal to 0
                                    # ** URL status: The current URL is saved as 'issue'
                                    else:
                                        url_to_collect_dict['collected'] = 'issue'
                                        print("[LOG] [Step 12 (if not)] There has been an issue with the current URL.\n"
                                              "[LOG] [Step 12 (if not)] The current URL is saved as 'issue'.")     
                                                                                                    
                        # Step 3 (if not)
                        # ** What: product data doesn't contain the field 'n_reviews' or hasn't been able
                        # to point to the information in the product page
                        # The number of reviews for the product isn't displayed on the product page or hasn't been
                        # successfully saved
                        # ** How: the field 'n_reviews' isn't in the 'product_dict'
                        else:
                            
                            # Step 4
                            # ** What: some reviews have been saved 
                            # The number of saved reviews can't be compared with the number of 
                            # reviews for the product because the information isn't displayed 
                            # on the product page
                            # It is impossible to know if all the reviews have been saved
                            # ** How: `n_saved_reviews` is higher than 0
                            # ** URL status: The current URL is saved as 'once'
                            if n_saved_reviews > 0:
                                url_to_collect_dict['collected'] = 'once'
                                print("[LOG] [Step 4] Not all the reviews have been collected for the product.\n"
                                      "[LOG] [Step 4] The current URL is saved as 'once'.")
                                
                            # Step 4 (if not)
                            # What: no reviews have been saved
                            # There aren't any saved reviews and the number of displayed reviews isn't 
                            # accessible on the product page
                            # The product hasn't any reviews
                            # ** How: `n_saved_reviews` is equal to 0
                            # ** URL status: The current URL is saved as 'yes'
                            else:
                                url_to_collect_dict['collected'] = 'yes'
                                print("[LOG] [Step 4 (if not)] All the reviews have been collected for the product.\n"
                                      "[LOG] [Step 4 (if not)] The current URL is saved as 'yes'.")
                                
                    # Step 2 (if not)
                    # ** What: product data doesn't contain the mandatory fields
                    # The fields 'product_name' and 'product_brand' are both None
                    # There has been a problem with the product data collection
                    # ** How: one of the fields 'product_name' or 'product_brand' is None
                    # ** URL status: the current URL is saved as 'issue'
                    else:
                        url_to_collect_dict['collected'] = 'issue'
                        print("[LOG] [Step 2 (if not)] There has been an issue with the current URL.\n"
                              "[LOG] [Step 2 (if not)] The current URL is saved as 'issue'.")
                        
                # Step 1 (if not)
                # ** What: product data hasn't been collected
                # There has been a problem with the product data collection
                # ** How: 'product_dict' is empty
                # ** URL status: the current URL is saved as a 'issue'
                else:
                    url_to_collect_dict['collected'] = 'issue'
                    print("[LOG] [Step 1 (if not)] There has been an issue with the current URL.\n"
                          "[LOG] [Step 1 (if not)] The current URL is saved as 'issue'.")
                    
            # Errors
            # --------------------------------------------------------
            # The collect for the current URL has raised an error so the current URL is saved as a 'issue'
            except:
                url_to_collect_dict['collected'] = 'issue'
                print("[LOG] [Errors] There has been an issue with the current URL.\n"
                      "[LOG] [Errors] The current URL is saved as 'issue'.")

            finally:
                with open(urls_to_collect_dicts_object_name, 
                          'w', encoding='utf-8') as file_to_dump:
                    json.dump(urls_to_collect_dicts, file_to_dump, indent=4, ensure_ascii=False)
    
            # Quit the driver
            quit_driver(driver=driver, delete_cookies=driver_dict['delete_cookies'])


def evaluate_collect_progression(urls_to_collect_object_name):
    """Evaluate the collect progression by displaying each key's number of occurences.
    
    Args:
        urls_to_collect_folder_path: urls_to_collect folder path.
        url_to_collect_file_name: url to collect file name to evaluate.    
    """

    # Load the most recent URLs
    most_recent_urls_to_collect_dicts_object_name = urls_to_collect_object_name
    urls_to_collect_dicts = json.load(
        open(most_recent_urls_to_collect_dicts_object_name, 'r', encoding='utf-8'))

    # Get the number of urls to collect
    n_urls_to_collect = len(urls_to_collect_dicts)

    # Get the number of urls 'yes', 'once', 'issue' and 'no'.
    n_status_yes = 0
    n_status_no = 0
    n_status_once = 0
    n_status_issue = 0
    for urls_to_collect_dict in urls_to_collect_dicts:
        url_status = urls_to_collect_dict['collected']
        if url_status == 'yes':
            n_status_yes += 1
        elif url_status == 'no':
            n_status_no += 1
        elif url_status == 'once':
            n_status_once += 1
        elif url_status == 'issue':
            n_status_issue += 1

    # Define the width for alignment
    field_width_n_status = 5
    field_width_p_status = 3

    print(f"[LOG] For the URLs to collect object name:\n{urls_to_collect_object_name}")
    print(f"[LOG] There are {n_urls_to_collect} URLs to collect.")
    print(f"[LOG] {str(n_status_yes).ljust(field_width_n_status)} "
          f"({str(int(100 * n_status_yes / n_urls_to_collect)).ljust(field_width_p_status)} %) "
           "URLs with the status YES.")
    print(f"[LOG] {str(n_status_no).ljust(field_width_n_status)} "
          f"({str(int(100 * n_status_no / n_urls_to_collect)).ljust(field_width_p_status)} %) "
           "URLs with the status NO.")
    print(f"[LOG] {str(n_status_once).ljust(field_width_n_status)} "
          f"({str(int(100 * n_status_once / n_urls_to_collect)).ljust(field_width_p_status)} %) "
           "URLs with the status ONCE.")
    print(f"[LOG] {str(n_status_issue).ljust(field_width_n_status)} "
          f"({str(int(100 * n_status_issue / n_urls_to_collect)).ljust(field_width_p_status)} %) "
           "URLs with the status ISSUE.")
