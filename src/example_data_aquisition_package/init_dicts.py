# !/usr/bin/env python

import time


def init_url_dict(source_dict):
    """Initializes the dictionary with the new URL data.

    Args:
        source_dict (dict): dictionary with information from the source.

    Returns:
       dict, Dictionary with the new URL data.
    """

    url_dict = {
        'id': None,
        'product_name': None, 
        'product_brand' : None,
        'product_type' : None,
        'product_price': None, 
        'mean_rating': None, 
        'n_reviews': None, 
        'code_source': None,
        'url': None,
        'products_listing_page_origin': None,
        'products_listing_page_url': None, 
        'products_listing_page_product_brand': None,
        'products_listing_page_search_term': None,
        'products_listing_page_category': None,
        'products_listing_page_sub_category': None,
        'products_listing_page_sub_sub_category': None, 
        'source': source_dict['source'],
        'country': source_dict['country'],
        'language': source_dict['language'],
        'collect_date': str(time.strftime('%Y-%m-%d')), 
    }

    return url_dict


def init_product_dict(source_dict):
    """Initializes the dictionary with the product data.

    Args:
        source_dict (dict): dictionary with information from the source.

    Returns:
        dict, Dictionary with the product data.
    """

    product_dict = {
        'product_application_ld_json': None,
        'product_name': None,  
        'product_brand': None,   
        'code_source': None, 
        'product_price': None, 
        'n_reviews': 0, 
        'mean_rating': None, 
        'product_details': None,
        'product_composition': None,
        #'code_sku': None,
        'url': None, 
        'source': source_dict['source'], 
        'country': source_dict['country'],  
        'language': source_dict['language'],  
        'collect_date': str(time.strftime('%Y-%m-%d')),
    }

    return product_dict


def init_review_dict(source_dict):
    """Initializes the dictionary with the review data.

    Returns:
        dict: Dictionary with the review data.
    """

    review_dict = {
        'id': None,
        # Product
        'product_name': None, # (str)
        'product_sub_name': None, # (str)
        'product_brand': None, # (str)
        'product_brand_line': None, # (str)
        'product_attribute_dict': None, # (dict)
        # URL
        'url': None,
        # Categories
        'category': None, # (str)
        'sub_category': None, # (str)
        'sub_sub_category': None, # (str)
        'sub_sub_sub_category': None, # (str)
        # Codes
        'code_asin': None, # (str)
        'code_ean': None, # (str)
        'code_gtin': None, # (str)
        'code_sku': None, # (str)
        'code_source': None, # (str)
        # Writer
        'writer_information': None, # (str)
        'writer_information_dict': None, # (dict)
        'writer_location': None, # (str)
        'writer_pseudo': None, # (str)
        'writer_recommendation': None, # (str)
        'writer_sex': None, # (str)
        # Review
        'review_rating': None, # (str)
        'review_other_rating': None, # (str)
        'review_other_rating_dict': None, # (dict)
        'review_date': None, # (str)
        'review_title': None, # (str)
        'review_text': None, # (str)
        'review_text_strength': None, # (str)
        'review_text_weakness': None, # (str)
        # Labels
        'syndication': None, # (str)
        'utility': None, # (str)
        'utility_yes': None, # (str)
        'utility_no': None, # (str)
        'verified_purchase': None, # (str)
        # Source
        'source': source_dict['source'], # (str)
        'country': source_dict['country'], # (str)
        'language': source_dict['language'], # (str)
        # Collecte
        'collect_date': str(time.strftime('%Y-%m-%d')), # (str)
    }

    return review_dict
