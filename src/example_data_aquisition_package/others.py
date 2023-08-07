#!/usr/bin/env python

import argparse
import json
from json import JSONDecodeError
import more_itertools
import time
import os
import sys
import glob
import random
sys.path.append('..')


def get_random_user_agent():
    """Generates random user agent."""

    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5563.64 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.53',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36 Edg/96.0.1054.34',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.40',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36 Edg/96.0.1054.34',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.53',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    ]

    return random.choice(user_agents)


def get_driver_dict(driver_path, options, args):
    """Gets the driver parameters dictionary.
    
    Args:
        driver_path (str): path to the driver.
        options (dict): options of the driver.
        args (dict): parsed arguments.

    Returns:
        dict, Driver parameters dictionary.
    """

    return {
        'driver_path': driver_path,
        'options': options,
        'headless': args.headless,
        'delete_cookies': args.delete_cookies,
    }


def convert_n_reviews_to_int(n_reviews):
    """Converts the `n_reviews` to int.
    
    Args:
        n_reviews: value of reviews count.
        
    Return:
        int, Reviews count in integer.
    """

    if isinstance(n_reviews, int):
        return n_reviews
    elif isinstance(n_reviews, float):
        return int(n_reviews)
    else:
        try:
            # Remove non-numeric characters
            n_reviews = ''.join(filter(str.isdigit, n_reviews))  
            return int(n_reviews)
        except Exception as e:
            print(f"[LOG] [EXCEPTION]\n{e}")
            return 0


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

    print("[LOG] There are {} urls to collect.".format(n_urls_to_collect))
    print("[LOG] There are {} ({} %) urls with the status YES.".format(n_status_yes, int(100 * n_status_yes / n_urls_to_collect)))
    print("[LOG] There are {} ({} %) urls with the status NO.".format(n_status_no, int(100 * n_status_no / n_urls_to_collect)))
    print("[LOG] There are {} ({} %) urls with the status ONCE.".format(n_status_once, int(100 * n_status_once / n_urls_to_collect)))
    print("[LOG] There are {} ({} %) urls with the status ISSUE.".format(n_status_issue,  int(100 * n_status_issue / n_urls_to_collect)))


def check_reviews_limit(n_reviews, n_max_reviews):
    """Compare number of reviews loaded/saved to the limit 'n_reviews_max'.
    
    Args:
        n_reviews: value of reviews count.
        n_reviews_max: limit of reviews to load/save.
        
    Return:
        Bool, if the limit has been exceeded or not.
    """

    if n_reviews >= n_max_reviews:

        print("[LOG] Reviews limit reached.")
        return True
    else:
        return False


def generate_urls_to_collect(source_dict, 
                             filtered_urls_dicts_object_name, 
                             urls_to_collect_folder_path, 
                             urls_to_collect_anchor_folder_path, 
                             n_parts):
    """Generated URLs to collect files.

    Args:
        source_dict (dict): dictionary with information from the source.
        filtered_urls_folder_path (str): path to the 'filtered_urls'.
        urls_to_collect_folder_path (str): path to the 'urls_to_collect' folder.
        urls_to_collect_anchor_folder_path (str): path to the 'urls_to_collect_anchor' folder.
        n_parts (int): Number of partitions for the urls to collect files.
    """

    # Get the most recent file in 'filtered_urls' folder
    most_recent_filtered_urls_dicts_object_name = filtered_urls_dicts_object_name
    
    # Load the filtered URLs
    with open(os.path.join(most_recent_filtered_urls_dicts_object_name),
              encoding='utf-8') as file_to_open:
        filtered_urls_dicts = json.load(file_to_open)
    print(f"[LOG] There are {len(filtered_urls_dicts)} filtered URLs.")

    # Generate the URLs to collect
    urls_to_collect_dicts = \
        generate_urls_to_collect_dicts(filtered_urls_dicts=filtered_urls_dicts)
    for partition in more_itertools.divide(n_parts, urls_to_collect_dicts):
        # Save URLs to collect in 'urls_to_collect' folder
        save_data(data=list(partition),
                saved_data_type='urls_to_collect',
                source=source_dict['source'],
                path=urls_to_collect_folder_path)

        # Save URLs to collect in 'urls_to_collect_anchor' folder
        save_data(data=list(partition),
                saved_data_type='urls_to_collect_anchor',
                source=source_dict['source'],
                path=urls_to_collect_anchor_folder_path,)
        
        # Add 1 second tempo for the unicity naming
        time.sleep(1)

        print(f"[LOG] {len(list(partition))} URLs to collect file have been saved "
            "in 'urls_to_collect' and 'urls_to_collect_anchor' folders.")
    
    if n_parts == 1:
        print("[LOG] The URLs to collect file have been aggregated.")
    elif n_parts > 1:
        print("[LOG] The URLs to collect files have been aggregated.")


def quit_driver(driver, delete_cookies):
    """Quit the driver.

    Args:
        driver (WebDriver): selenium webdriver.
        delete_cookies (bool): to delete cookies or not.
    """
    try:
        driver.quit()
        if delete_cookies:
            driver.delete_all_cookies()
    except Exception as e:
        print(f"[LOG] [EXCEPTION]\n{e}")


def get_rating_from_colors(colors):
    """Evaluates the rating value based on the number of occurrences 
    of the color "#3cbeaf" in a list of colors.

    Args:
        colors (list): list of color codes in string 
                       format, such as "#3cbeaf" or "#E6E6E6".

    Returns:
        int, The rating value corresponding to the number of consecutive 
             occurrences of the color "#3cbeaf" in the list.
             The rating value starts at 1 and increases by 1 for 
             each group of consecutive "#3cbeaf" colors.
    """

    return colors.count("#3cbeaf")


def save_data(data, saved_data_type, source, path):
    """Saves the collected `data`.

    Args:
        data (object): data to save.
        saved_data_type (str): 'url_new', 'products' or 'reviews'.
        source (str): name of the source.
        path (str): path where the data will be saved.
    """

    with open(os.path.join(path, time.strftime('%Y_%m_%d_%H_%M_%S') + '_' + \
                                 saved_data_type + '_' + source + '.json'), 
              'w+', encoding='utf-8') as file_to_dump:
        json.dump(data, file_to_dump, indent=4, ensure_ascii=False)


def save_products_listing_pages_brands(data, path):
    """Saves collected names and URLs from brand listing page
    
    Args:
        data (list): data to save
        path (str): path where the data will be saved.
    """

    str_to_dump = "BRANDS = [" 
    for elt in data:
        str_to_dump += f"{elt},\n"
    str_to_dump += "]"

    # TODO -> open(path + '\BRANDS.py', 'w+', encoding='utf-8') 
    # -> faire un chemin relatif + nommé le fichier brands.py
    with open(path + '/brands_test.py', 'w+', encoding='utf-8') as brands:  
        brands.write(str_to_dump)


def remove_duplicates(dicts, key):
    """Removes duplicates from a list of dictionaries based on a specified key.

    Args:
        dicts (list[dict]): list of dictionaries.
        key (str): key to use for comparing duplicates.

    Returns:
        list[dict], List of dictionaries with duplicates removed based on the specified key.
    """

    unique_keys = set()
    removed_duplicates_dicts = []

    for d in dicts:
        if d[key] not in unique_keys:
            unique_keys.add(d[key])
            removed_duplicates_dicts.append(d)

    return removed_duplicates_dicts


def get_most_recent_json_file(folder_path):
    """Returns path to the most recent json file in a the specified folder.

    Args:
        folder_path (str): path of folder containing json files.

    Returns:
        str, most recently created json file path.
    """
    
    most_recent_json_file = \
        sorted(glob.glob(os.path.join(folder_path, '*.json')))[-1]
    return most_recent_json_file


def remove_elements_with_keywords(dicts, keys, keywords):
    """Removes elements from a list of dictionaries if a specific key contains a specific word.

    Args:
        dicts (list[dict]): a list of dictionaries.
        keys (list): list of keys to check for the keyword.
        keywords (list): list of words to look for in the value of the key.

    Returns:
        list[dict], List of dictionaries with elements removed based on the 
                    presence of the keywords.
    """

    results = []
    for d in dicts:
        keep = True
        for key in keys:
            if key not in d:
                continue
            value = str(d[key]).lower().strip()
            for keyword in keywords:
                if str(keyword).lower().strip() in value:
                    keep = False
                    break
            if not keep:
                break
        if keep:
            results.append(d)

    return results


def select_elements_with_keywords(dicts, keys, keywords):
    """Selects elements from a list of dictionaries if a specific key contains a specific word.

    Args:
        dicts (list[dict]): A list of dictionaries.
        keys (list): List of keys to check for the keyword.
        keywords (list): List of words to look for in the value of the key.

    Returns:
        list[dict], List of dictionaries with elements selected based on the 
                    presence of the keywords.
    """

    results = []
    for d in dicts:
        keep = False
        for key in keys:
            if key not in d:
                continue
            value = str(d[key]).lower().strip()
            for keyword in keywords:
                if str(keyword).lower().strip() in value:
                    keep = True
                    break
            if keep:
                break
        if keep:
            results.append(d)

    return results


def generate_urls_to_collect_dicts(filtered_urls_dicts):
    """Generates a list of product urls to collect dictionaries
    from a list of new product urls dictionaries.

    Args:
        filtered_urls_dicts (list[dict]): lst of dictionaries containing new product urls.

    Returns:
        list[dict], List of dictionaries containing the product urls, 
                    their category, and whether they have been collected.
    """

    urls_to_collect_dicts = [
        {
            'url': u['url'], 
            'collected': 'no'
        }
        for u in filtered_urls_dicts
    ]
    
    return urls_to_collect_dicts


def aggregate_products_files(source, products_data_folder_path, merged_products_data_folder_path):
    """Aggregates the collected products files.
    
    Args:
        source (str): name of the source.
        products_data_folder_path (str): path to the products data files folder.
        merged_products_data_folder_path (str): path to the merged products folder.

    """
    
    products_files = []
    
    # For each json file, it opens the content of the file
    for products_file in glob.glob(os.path.join(products_data_folder_path, '*.json')):
        try:
            with open(products_file, 'r', encoding='utf8') as f:
                open_product_file = json.load(f)
                products_files.append(open_product_file)
        except JSONDecodeError:
            pass

    merged_products_file_name = os.path.join(
        merged_products_data_folder_path, f"{time.strftime('%Y_%m_%d_%H_%M_%S')}_merged_products_{source}.json")
    
    with open(merged_products_file_name, 'w', encoding='utf-8') as file_to_dump:
        json.dump(products_files, file_to_dump, indent=4, ensure_ascii=False)
    
    print("[LOG] The products files have been merged.")
    print(f"[LOG] There are {len(products_files)} merged products.")


def aggregate_reviews_files(source, reviews_data_folder_path, merged_reviews_data_folder_path):
    """Aggregates the collected reviews files.
    
    Args:
        source (str): name of the source.
        reviews_data_folder_path (str): path to the reviews data files folder.
        merged_reviews_data_folder_path (str): path to the merged reviews folder.
    """

    reviews_files = []

    # For each json file, it opens the content of the file
    for reviews_file in glob.glob(os.path.join(reviews_data_folder_path, '*.json')):
        try:
            with open(reviews_file, 'r', encoding='utf8') as f:
                reviews_dicts = json.load(f)
                reviews_files.extend(reviews_dicts)
        except JSONDecodeError:
            pass

    merged_reviews_file_name = os.path.join(
        merged_reviews_data_folder_path, f"{time.strftime('%Y_%m_%d_%H_%M_%S')}_merged_reviews_{source}.json")
    
    with open(merged_reviews_file_name, 'w', encoding='utf-8') as file_to_dump:
        json.dump(reviews_files, file_to_dump, indent=4, ensure_ascii=False)

    print("[LOG] The reviews files have been merged.")
    print(f"[LOG] There are {len(reviews_files)} merged reviews.")


def display_collected_data(data_dict):
    """Takes the dictionary of any type of data collected (URL, review or product)
    and displays random values of the dictionary.

    Args:
    data_dict (dict): The dictionary containing any type of data.
    """

    # This list contains the keys of the data dictionary that are not important for display
    unuseful_keys = ['id', 'source', 'language', 'industry', 'collect_date', 'country', 'url']

    # Verifies if the data collected is a dictionary or a list of dictionaries
    if not isinstance(data_dict, dict):
        # If it is a list then we take a random dictionary in the list and
        # display a random item from it
        data_dict = random.choice(data_dict)

    random_key = random.choice(list(data_dict.keys()))
    # If the random key obtained is in the non_priority then we keep looking
    # for another random key
    while random_key in unuseful_keys:
        random_key = random.choice(list(data_dict.keys()))
    print(f"[LOG] [DISPLAY COLLECTED DATA] {random_key} : {data_dict[random_key]}")

