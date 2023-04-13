# Your name: Paige Wiaduck
# Your student id: 6603 9062
# Your email: pwiaduck@uich.edu
# List who you have worked with on this homework:

import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def load_rest_data(db):
    """
    This function accepts the file name of a database as a parameter and returns a nested
    dictionary. Each outer key of the dictionary is the name of each restaurant in the database, 
    and each inner key is a dictionary, where the key:value pairs should be the category, 
    building, and rating for the restaurant.
    """

    dict = {}
    con = sqlite3.connect(db)

    cur = con.cursor()

    for row in cur.execute("SELECT restaurants.name, categories.category, buildings.building, restaurants.rating FROM restaurants JOIN categories ON restaurants.category_id = categories.id JOIN buildings ON restaurants.building_id = buildings.id"):
        # print(row)
        restaurant = row[0]
        category = row[1]
        building = row[2]
        rating = row[3]

        dict[restaurant] = {}
        dict[restaurant]["category"] = category
        dict[restaurant]["building"] = building
        dict[restaurant]["rating"] = rating

    con.close()
    
    return dict

def plot_rest_categories(db):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the count of number of restaurants in each category.
    """
    num_places = []
    dict = {}
    con = sqlite3.connect(db)

    cur = con.cursor()
    
    category_types = cur.execute("SELECT category FROM categories")
                  
    lst = cur.execute("SELECT categories.category, COUNT(restaurants.category_id) FROM categories JOIN restaurants ON restaurants.category_id = categories.id GROUP BY category")
    for row in lst:
        # print(row)
        type = row[0]
        num = row[1]

        dict[type] = num

    restaurants = list(dict.keys())
    values = list(dict.values())

    plt.figure(1, figsize=(15,5))
    plt.rcParams.update({'font.size': 8})
    
    plt.barh(restaurants, values)
    
    plt.title("Restaurant categories")
    # plt.show()

    con.close() 

    return dict

    

def find_rest_in_building(building_num, db):
    '''
    This function accepts the building number and the filename of the database as parameters and returns a list of 
    restaurant names. You need to find all the restaurant names which are in the specific building. The restaurants 
    should be sorted by their rating from highest to lowest.
    '''
    
    con = sqlite3.connect(db)
    cur = con.cursor()

    places_lst = []
    places = cur.execute("SELECT restaurants.name, restaurants.rating FROM restaurants JOIN buildings ON restaurants.building_id = buildings.id WHERE buildings.building = ?", ((building_num, )))
    for row in places:
        places_lst.append(row)
    
    sorted_lst = (sorted(places_lst, key = lambda x: x[1], reverse = True)) 
    
    building_restaurants = []
    for tup in sorted_lst:
        building_restaurants.append(tup[0])

    return building_restaurants



#EXTRA CREDIT
def get_highest_rating(db): #Do this through DB as well
    """
    This function return a list of two tuples. The first tuple contains the highest-rated restaurant category 
    and the average rating of the restaurants in that category, and the second tuple contains the building number 
    which has the highest rating of restaurants and its average rating.

    This function should also plot two barcharts in one figure. The first bar chart displays the categories 
    along the y-axis and their ratings along the x-axis in descending order (by rating).
    The second bar chart displays the buildings along the y-axis and their ratings along the x-axis 
    in descending order (by rating).
    """
    pass

#Try calling your functions here
def main():
    pass

class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.highest_rating = [('Deli', 4.6), (1335, 4.8)]

    def test_load_rest_data(self):
        rest_data = load_rest_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, dict)
        self.assertEqual(rest_data['M-36 Coffee Roasters Cafe'], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_plot_rest_categories(self):
        cat_data = plot_rest_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_find_rest_in_building(self):
        restaurant_list = find_rest_in_building(1140, 'South_U_Restaurants.db')
        self.assertIsInstance(restaurant_list, list)
        self.assertEqual(len(restaurant_list), 3)
        self.assertEqual(restaurant_list[0], 'BTB Burrito')

    def test_get_highest_rating(self):
        highest_rating = get_highest_rating('South_U_Restaurants.db')
        self.assertEqual(highest_rating, self.highest_rating)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
