# Focus
Scraper design to collect course information from California community colleges. The data is outputted to a .csv in a well-formatted and organized manner. Implemeneted in Python.

**Dependencies**

- [Blinker, Dependency for Selenium-Wire](https://pypi.org/project/blinker/)
- [Selenium](https://pypi.org/project/selenium/)
- [Selenium-Wire](https://pypi.org/project/selenium-wire/)

**Drivers**

- [Gecko](https://pypi.org/project/blinker/)
- [Chrome](https://googlechromelabs.github.io/chrome-for-testing/)

## Options:
- If you wish to see how the program captures the requests from the server, you can remove the **Options** module, in addition to removing the options object passed to the driver. After removal, you will see Charlotte run as a live browser.
- If you wish to run the program on a different college website, we recommend making sure it is a Catalogue-based. Furthermore, you may possibly need to change certain element names within the program in order for Charlotte to detect them.
