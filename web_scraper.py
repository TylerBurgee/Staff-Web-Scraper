"""
Author: Tyler J. Burgee
Date: 13 February 2023
Course: CIS 321 - Data & File Structure
"""

# IMPORT MODULES
from bs4 import BeautifulSoup
import pandas as pd
import requests
import csv
import re

class ShepherdEmployeeWebScraper:
    """
    Class to define a ShepherdEmployeeWebScraper object

    Use : to obtain staff information from various departments at Shepherd.edu

    Attributes
    ----------
    url : str
        The url of the department faculty webpage to be scraped
    filename : str
        The filename to be used when saving employee data to a CSV file
    headers : dict
        Specifies the type of data to be scraped from the webpage
    page : object
        Data received from a get request sent to the webpage server
    soup : object
        HTML file parser
    employee_list : list
        The employees retrieved from the webpage
    fieldnames : list
        The names of the fields that will be retreived from the webpage

    Methods
    -------
    add_employee(data: list)
        Adds a new employee to employee list
    save_to_csv(filename: str)
        Saves employee list to a .csv file,
        prints saved data to console
    get_employee_data()
        Parses HTML text,
        returns a list of employee names, titles, and emails
    get_elements_by_class(element: str, element_class: str)
        Returns an iterable object of webpage elements
        with the given class name
    """

    def __init__(self, url: str, filename: str) -> None:
        """Defines the constructor for a ShepherdEmployeeWebScraper object"""
        self.url = url
        self.filename = filename

        self.headers = {'mime': 'text/html'}
        self.page = requests.get(self.url, headers=self.headers)
        self.soup = BeautifulSoup(self.page.content, "html.parser")

        self.employee_list = []
        self.field_names = ["Name", "Title", "Email"]

    def __str__(self) -> str:
        """Returns the string representation of a ShepherdEmployeeWebScraper object"""
        return str(self.employee_list)

    def add_employee(self, data: list) -> None:
        """Adds a new employee to employee list"""
        name = data[0]
        title = data[1]
        email = data[2]
        if "@shepherd.edu" not in email:
            email = None

        employee = {
            self.field_names[0] : name,
            self.field_names[1] : title,
            self.field_names[2] : email
        }
        self.employee_list.append(employee)

    def save_to_csv(self) -> None:
        """Prints employee list to console"""
        staff = pd.DataFrame(self.employee_list)
        staff.to_csv(self.filename)
        print("CSV File Created with the Following Data:\n")
        print(staff)

    def get_employee_data(self, employee_tables: object) -> list:
        """
        Parses HTML text,
        returns a list of employee names, titles, and emails
        """
        employee_data = []
        for employee in employee_tables:
            employee_name = employee.find_all("h2")
            employee_info = employee.find_all("td")

            data = []
            # GET EMPLOYEE NAME
            data.append(employee_name[0].text.strip())
            for line in employee_info:
                # GET EMPLOYEE TITLE AND EMAIL
                if len(data) <= 2:
                    data.append(line.text.strip().split("\t")[0])
                else:
                    break
            employee_data.append(data)

        return employee_data

    def get_elements_by_class(self, element: str, element_class: str) -> object:
        """Returns a list of elements with the given class name"""
        results = self.soup.find_all(element, {"class": element_class})

        return results

if __name__ == "__main__":
    shepherd_departments = ["cme", "biology", "theater", "facilities"]

    while True:
        # GET USER INPUT
        department = input("Enter Shepherd Department:\n" +
                           "Options - cme, biology, theater, facilities, or QUIT\n> ")
        if department.casefold() in shepherd_departments:
            # INSTANTIATE ShepherdEmployeeWebScraper OBJECT
            url = "https://www.shepherd.edu/{}/staff".format(department)
            filename = "employee_list_{}.csv".format(department)
            web_scraper = ShepherdEmployeeWebScraper(url, filename)

            # GET ALL TABLES CONTAINING EMPLOYEE INFORMATION
            employee_tables = web_scraper.get_elements_by_class("table", "table")

            # ISOLATE EMPLOYEE DATA FROM TABLES
            employees = web_scraper.get_employee_data(employee_tables)

            # ADD EMPLOYEES TO EMPLOYEE LIST
            for employee in employees:
                web_scraper.add_employee(employee)

            # GENERATE CSV FILE FROM DATA IN EMPLOYEE LIST
            web_scraper.save_to_csv()

        elif department.casefold() == "quit":
            break
        else:
            print("Illegal Input. Try Again.\n")
